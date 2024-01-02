from pathlib import Path

import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf

from litrl.common.schema import ConfigSchema


def get_omegaconf(overrides: list[str] | None):
    with hydra.initialize_config_dir(
        config_dir=str(Path("config").absolute()),
        version_base="1.3.2",
    ):
        return hydra.compose(config_name="default", overrides=overrides)


def omegaconf_to_schema(cfg: DictConfig) -> ConfigSchema:
    OmegaConf.resolve(cfg)
    logger.info(f"config is \n{OmegaConf.to_yaml(cfg)}")
    return ConfigSchema(**OmegaConf.to_container(cfg))
