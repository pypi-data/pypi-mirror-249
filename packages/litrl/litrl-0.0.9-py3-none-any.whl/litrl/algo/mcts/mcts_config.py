from dataclasses import dataclass
from typing import Any, Self

from litrl.algo.mcts.backpropagate import BackpropagateStrategy, VanillaBackpropagate
from litrl.algo.mcts.expansion import ExpansionStrategy, VanillaExpansion
from litrl.algo.mcts.recommend import RecommendStrategy, VanillaRecommend
from litrl.algo.mcts.rollout import RolloutStrategy, VanillaRollout
from litrl.algo.mcts.select import SelectionStrategy, VanillaSelection
from litrl.algo.mcts.typing import MctsActionType
from litrl.common.agent import RandomMultiAgent


@dataclass
class MCTSConfig:
    simulations: int = 50
    seed: int = 123
    selection_strategy: SelectionStrategy = VanillaSelection()
    rollout_strategy: RolloutStrategy = VanillaRollout(
        rollout_agent=RandomMultiAgent[Any, Any, MctsActionType, Any](),
    )
    backpropagate_strategy: BackpropagateStrategy = VanillaBackpropagate()
    expansion_strategy: ExpansionStrategy = VanillaExpansion()
    recommend_strategy: RecommendStrategy = VanillaRecommend()
    verbose: bool = False

    def __str__(self) -> str:
        return f"simulations={self.simulations}, rollout_strategy={self.rollout_strategy!s}"


class MCTSConfigBuilder:
    def __init__(self) -> None:
        self._simulations = 50

    def set_simulations(self, simulations: int) -> Self:
        self._simulations = simulations
        return self

    def vanilla(self) -> MCTSConfig:
        return MCTSConfig(simulations=self._simulations)
