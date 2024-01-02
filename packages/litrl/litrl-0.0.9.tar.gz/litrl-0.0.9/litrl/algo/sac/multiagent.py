from copy import deepcopy

from loguru import logger

from litrl.algo.sac.agent import SacAgent, SacStochasticAgent
from litrl.algo.sac.model import Sac
from litrl.common.agent import Agent, RandomAgent
from litrl.common.schema import ModelConfigSchema
from litrl.wrappers import StaticOpponentWrapper, ValidationWrapper

REWARD_UPDATE_METRIC = 0.5


class MultiagentConfigSchema(ModelConfigSchema):
    update_opponent_score: float


EnvType = ValidationWrapper | StaticOpponentWrapper


class MaSac(Sac[EnvType, MultiagentConfigSchema]):
    def __init__(
        self,
        cfg: MultiagentConfigSchema,
    ):
        super().__init__(cfg)

    def get_opponent(self, env: EnvType) -> Agent:
        return env.get_wrapper_attr("opponent")

    def is_self_play(self, env: EnvType) -> bool:
        return isinstance(self.get_opponent(env), SacAgent)

    def is_random_opponent(self, env: EnvType) -> bool:
        return isinstance(self.get_opponent(env), RandomAgent)

    def update_actor(self, env: EnvType) -> None:
        if self.is_random_opponent(env):
            logger.info("updating random opponent to SAC agent")
            env.get_wrapper_attr("set_opponent")(
                SacStochasticAgent(deepcopy(self.actor)),
            )
        elif self.is_self_play(env):
            logger.info("Updating the opponent")
            self.get_opponent(env).update(deepcopy(self.actor))

    def update_train_opponent_if_good_training_performance(self) -> None:
        score = self.train_reward_metric.compute()
        if (
            score > REWARD_UPDATE_METRIC
            and self.train_reward_metric._num_vals_seen
            >= self.train_reward_metric.window
        ):
            logger.debug(
                f"Running training {score} > {REWARD_UPDATE_METRIC}, updating training opponent",
            )
            self.update_actor(self.env)
            self.train_reward_metric.reset()

    def update_train_opponent_if_good_val_performance(self) -> None:
        """
        This allows to update the self-play opponent if certain ELO level is reached.
        Similar to concepts of Curriculum Learning.
        """
        if not self.is_self_play(self.val_env) and self.is_self_play(self.env):
            score = self.val_metric.compute()
            if (
                score > self.cfg.update_opponent_score
                and self.val_metric._num_vals_seen >= self.val_metric.window
            ):
                logger.debug(
                    f"Running validation {score} > {self.cfg.update_opponent_score}, updating training opponent",
                )
                self.update_actor(self.env)
                self.val_metric.reset()

    def on_train_epoch_end(self) -> None:
        self.update_train_opponent_if_good_training_performance()
        super().on_train_epoch_end()

    def on_validation_epoch_end(self) -> None:
        super().on_validation_epoch_end()
        # self.update_train_opponent_if_good_val_performance()
