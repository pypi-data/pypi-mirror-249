from pathlib import Path

import hydra
from lightning import LightningModule, Trainer
from omegaconf import DictConfig

from litrl.common.hydra import omegaconf_to_schema
from litrl.common.mlflow import get_load_path
from litrl.common.schema import ConfigSchema


@hydra.main(config_path="../config", config_name="default", version_base="1.3.2")
def main(omegaconf_cfg: DictConfig) -> None:
    """Enter the project."""
    cfg: ConfigSchema = omegaconf_to_schema(cfg=omegaconf_cfg)
    load_path: Path | None = get_load_path(tags=cfg.tags, load=cfg.load)
    model: LightningModule = cfg.model.instantiate()
    trainer: Trainer = cfg.trainer.instantiate()
    trainer.fit(model=model, ckpt_path=str(object=load_path))


if __name__ == "__main__":
    main()
