from typing import Generic, TypeVar

import gymnasium as gym
from gymnasium.wrappers.time_limit import TimeLimit
from pettingzoo import AECEnv
from pydantic import validator
from pydantic.dataclasses import dataclass as pydantic_dataclass

# EnvType = TypeVar("EnvType", gym.Env, AECEnv, gym.Wrapper)  # TODO
EnvType = TypeVar("EnvType")


@pydantic_dataclass
class BufferSchema:
    batch_size: int
    max_size: int


@pydantic_dataclass(config=dict(arbitrary_types_allowed=True))
class ModelConfigSchema(Generic[EnvType]):
    seed: int
    lr: float
    gamma: float
    warm_start_steps: int
    hidden_size: int
    n_hidden_layers: int
    buffer: BufferSchema
    val_env_seed: int
    env: EnvType
    val_env: EnvType
    epsilon: float
    _target_: str = "lightning_rl.algo.dqn.config_schema.ModelConfigSchema"

    @validator("lr")
    def validate_lr(cls, lr: float) -> None:
        if lr < 0:
            raise ValueError(f"'lr' can't be less than 0, got: {lr}")
        return lr


@pydantic_dataclass
class ModelSchema:
    _target_: str
    cfg: ModelConfigSchema


@pydantic_dataclass
class TrainerSchema:
    log_every_n_steps: int
    max_epochs: int


@pydantic_dataclass
class DQNConfigSchema:
    model: ModelSchema
    trainer: TrainerSchema
