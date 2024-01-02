import os
import uuid
from pathlib import Path

import torch
from huggingface_hub import CommitOperationAdd, HfApi, login, metadata_eval_result
from huggingface_hub.repocard import metadata_save
from lightning import LightningModule, Trainer
from lightning.pytorch.callbacks import ModelCheckpoint
from loguru import logger
from pydantic import RootModel
from requests.exceptions import ConnectionError

from litrl.common.schema import ConfigSchema


class HuggingfaceCallback(ModelCheckpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            login(
                token=os.environ.get("HUGGINGFACE_TOKEN"),
                add_to_git_credential=True,
                new_session=False,
            )
        except ConnectionError as e:
            logger.error(f"Can't connect to huggingface! {e}")
        self.threshold = kwargs.pop("threshold", -1.1)
        self.hf_api = HfApi()
        self.model_id = uuid.uuid4().hex  # TODO match with runid mlflow

    def add_metadata(self, readme_path: Path) -> Path:
        metadata = metadata_eval_result(
            model_pretty_name="mock",
            task_pretty_name="reinforcement-learning",
            task_id="reinforcement-learning",
            metrics_pretty_name="mean_reward",
            metrics_id="mean_reward",
            metrics_value="mock +/- mock",
            dataset_pretty_name="mock",
            dataset_id="mock",
        )
        metadata["tags"] = [
            "reinforcement-learning",
            "connect-four",
            "pytorch",
            "custom-implementation",
            "generic",
        ]
        metadata_save(readme_path, metadata)

    def write_readme(self, readme_path: Path, cfg: ConfigSchema):
        readme = RootModel(cfg)
        with readme_path.open("w", encoding="utf-8") as f:
            f.write(readme)

    def update_model(self, trainer: Trainer, pl_module: LightningModule) -> None:
        if self.best_model_score is None or self.best_model_score < self.threshold:
            logger.debug(f"No model to upload: {self.best_model_score}")
            return

        onnx_path = Path().joinpath("temp", "model.onnx")
        torch.onnx.export(
            pl_module.actor,
            pl_module.obs,
            onnx_path,
            input_names=["input"],
            output_names=["output"],
        )
        # TODO readme, mp4, plot
        # TODO upload config and commit hash
        hf_checkpoint_path = f"models/{self.model_id}/{Path(self.best_model_path).name}"
        hf_onnx_path = f"models/{self.model_id}/model.onnx"
        readme_path = Path().joinpath("temp", f"{uuid.uuid4()}-README.md")
        self.write_readme(readme_path, pl_module.cfg)
        self.add_metadata(readme_path)
        hf_readme_path = f"models/{self.model_id}/README.md"
        logger.info(f"uploading checkpoint to huggingface at {hf_checkpoint_path}")
        logger.info(f"uploading onnx model to huggingface at {hf_onnx_path}")
        operations = [
            CommitOperationAdd(
                path_in_repo=hf_checkpoint_path,
                path_or_fileobj=self.best_model_path,
            ),
            CommitOperationAdd(
                path_in_repo=hf_onnx_path,
                path_or_fileobj=onnx_path,
            ),
            CommitOperationAdd(
                path_in_repo=hf_readme_path,
                path_or_fileobj=readme_path,
            ),
        ]
        self.hf_api.create_commit(
            repo_id="c-gohlke/connect4SAC",
            repo_type="model",
            operations=operations,
            commit_message="Upload my model weights and license",
        )

    def update_dataset(self, trainer: Trainer, pl_module: LightningModule) -> None:
        dataset_path = Path().joinpath("temp", "buffer.pt")
        torch.save(pl_module.buffer, dataset_path)
        hf_dataset_path = (
            f"datasets/{self.model_id}/{Path(self.best_model_path).stem}_buffer.pt"
        )
        logger.info(f"uploading dataset to huggingface at {hf_dataset_path}")
        operations = [
            CommitOperationAdd(
                path_in_repo=hf_dataset_path,
                path_or_fileobj=dataset_path,
            ),
        ]
        self.hf_api.create_commit(
            repo_id="c-gohlke/Connect4SAC",
            repo_type="dataset",
            operations=operations,
            commit_message="Upload dataset",
        )

    def teardown(
        self,
        trainer: Trainer,
        pl_module: LightningModule,
        stage: str,
    ) -> None:
        self.update_model(trainer, pl_module)
        self.update_dataset(trainer, pl_module)
        return super().teardown(trainer, pl_module, stage)
