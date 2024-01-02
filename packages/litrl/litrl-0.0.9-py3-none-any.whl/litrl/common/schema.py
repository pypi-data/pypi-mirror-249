import inspect
from pathlib import Path
from typing import Any, Generic, Literal, Self, TypeVar, cast

import hydra
from gymnasium import Env
from lightning import LightningModule, Trainer
from lightning.pytorch.callbacks import Callback as LightningCallback
from lightning.pytorch.loggers import Logger as LightningLogger
from loguru import logger
from pydantic import RootModel, field_validator
from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic.dataclasses import is_pydantic_dataclass

InstanceClass = TypeVar("InstanceClass")


@pydantic_dataclass(frozen=True)
class InstantiatorClass(Generic[InstanceClass]):
    _target_: str

    @classmethod
    def is_instantiable(cls: type[Self], obj: type) -> bool:
        if obj == InstantiatorClass or (
            inspect.isclass(object=obj) and issubclass(obj, InstantiatorClass)
        ):
            return True
        return False

    @classmethod
    def process_dict(
        cls,
        key_type: type,
        key: str,
        val: Any,
        info_dict: dict[str, Any],
        *,
        instantiate_children: bool,
    ) -> None:
        if key_type == list and instantiate_children:
            for list_item in val:
                logger.info(f"instantiating list item {list_item}")
        if cls.is_instantiable(obj=key_type):
            schema: InstantiatorClass = key_type(**info_dict[key])
            if instantiate_children:
                schema = schema.instantiate()
            info_dict[key] = schema
        elif is_pydantic_dataclass(key_type):
            sub_info_dict = info_dict[key]
            cls.cast_type(
                pydantic=RootModel(root=val),
                info_dict=sub_info_dict,
                instantiate_children=instantiate_children,
            )
            info_dict[key] = key_type(**sub_info_dict)

    @classmethod
    def cast_type(
        cls: type[Self],
        pydantic: RootModel[Any],
        info_dict: dict[str, Any],
        *,
        instantiate_children: bool,
    ) -> None:
        for key in info_dict:
            val = pydantic.root.__getattribute__(key)
            key_type = type(val)
            if key_type == list:
                objs = []
                for list_item in val:
                    if cls.is_instantiable(type(list_item)):  # type: ignore[misc]
                        objs.append(list_item.instantiate())  # type: ignore[aa]
                    else:
                        objs.append(list_item)  # type: ignore[aa]
                info_dict[key] = objs
            else:
                cls.process_dict(
                    key_type=key_type,
                    key=key,
                    val=val,
                    info_dict=info_dict,
                    instantiate_children=instantiate_children,
                )

    def instantiate(self, *, _recursive_: bool | None = None) -> InstanceClass:
        pydantic_model = RootModel(root=self)
        info_dict: dict[str, Any] = pydantic_model.model_dump(exclude="_target_")  # type: ignore[assignment]
        if _recursive_ is None:
            _recursive_ = cast(bool, info_dict.pop("_recursive_", True))
        self.cast_type(
            pydantic=pydantic_model,
            info_dict=info_dict,
            instantiate_children=_recursive_,
        )
        fabric: type[InstanceClass] = hydra.utils.instantiate(
            config={"_target_": self._target_},
            _partial_=True,
        )
        return fabric(**info_dict)


@pydantic_dataclass(frozen=True)
class MCTSConfigSchema:
    simulations: int


@pydantic_dataclass(frozen=True)
class AgentSchema(InstantiatorClass[Env]):
    pass


@pydantic_dataclass(frozen=True)
class MCTSAgentSchema(InstantiatorClass[Env]):
    cfg: MCTSConfigSchema | None


@pydantic_dataclass(frozen=True)
class EnvSchema(InstantiatorClass[Env]):
    id: str
    opponent: None | AgentSchema | MCTSAgentSchema = None
    val: bool | None = None


@pydantic_dataclass
class BufferSchema:
    batch_size: int
    max_size: int


@pydantic_dataclass(frozen=True)
class ModelConfigSchema:
    seed: int
    lr: float
    gamma: float
    warm_start_steps: int
    hidden_size: int
    n_hidden_layers: int
    buffer: BufferSchema
    epsilon: float
    target_entropy: float
    tau: float
    env_fabric: EnvSchema
    val_env_fabric: EnvSchema

    @field_validator("lr")
    @classmethod
    def validate_lr(cls: type[Self], lr: float) -> float:
        if lr < 0:
            msg = f"'lr' can't be less than 0, got: {lr}"
            raise ValueError(msg)
        return lr


@pydantic_dataclass(frozen=True)
class ModelSchema(InstantiatorClass[LightningModule]):
    _target_: str
    cfg: ModelConfigSchema
    _recursive_: Literal[False] = False


@pydantic_dataclass(frozen=True)
class LoggerSchema(InstantiatorClass[LightningLogger]):
    _target_: str
    log_model: bool
    tags: dict[str, str]


@pydantic_dataclass(frozen=True)
class CallbackSchema(InstantiatorClass[LightningCallback]):
    _target_: str


@pydantic_dataclass(frozen=True)
class TrainerSchema(InstantiatorClass[Trainer]):
    _target_: str
    log_every_n_steps: int
    limit_train_batches: int
    max_epochs: int
    logger: LoggerSchema
    callbacks: list[CallbackSchema]


@pydantic_dataclass
class ConfigSchema:
    model: ModelSchema
    trainer: TrainerSchema
    tags: dict[str, str]
    load_path: None | str
    _recursive_: Literal[False] = False

    @field_validator("load_path")
    @classmethod
    def ensure_exists(cls: type[Self], load_path: str | None = None) -> str | None:
        if not (load_path is None or load_path == "latest" or Path(load_path).exists()):
            msg: str = f"Path {load_path} does not exist"
            raise ValueError(msg)
        return load_path
