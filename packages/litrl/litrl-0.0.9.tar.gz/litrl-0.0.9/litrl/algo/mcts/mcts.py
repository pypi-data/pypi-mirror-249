import numpy as np

from litrl.algo.mcts.node import Root
from litrl.algo.mcts.typing import MctsEnv
from litrl.env.make import copy

from .mcts_config import MCTSConfig, MCTSConfigBuilder


class MCTS:
    def __init__(
        self,
        env: MctsEnv,
        cfg: MCTSConfig | None = None,
    ) -> None:
        cfg = cfg if cfg is not None else MCTSConfigBuilder().vanilla()
        self._root = Root()
        self._root_env = env
        self._cfg = cfg
        self._np_random = np.random.default_rng(seed=cfg.seed)
        self._simulation_env = copy(self._root_env)
        self._cfg.expansion_strategy.expand(self._simulation_env, self._root)

    def simulate(self) -> None:
        self._simulation_env = copy(self._root_env)
        node = self._cfg.selection_strategy.select_and_step(
            self._simulation_env,
            self._root,
        )
        self._cfg.expansion_strategy.expand(self._simulation_env, node)
        reward = self._cfg.rollout_strategy.rollout(
            self._simulation_env,
            self._root_env.unwrapped.agent_selection,
        )
        self._cfg.backpropagate_strategy.backpropagate(node, reward)

    def get_action(self) -> int:
        for _ in range(self._cfg.simulations):
            self.simulate()

        return self._cfg.recommend_strategy.get_action(self._root)
