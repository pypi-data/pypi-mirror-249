from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from litrl.algo.mcts.typing import MctsActionType
from litrl.algo.mcts.value import Minmax

if TYPE_CHECKING:
    from litrl.algo.mcts.node import Root


class RecommendStrategy(ABC):
    @abstractmethod
    def get_action(self, node: "Root") -> MctsActionType:
        ...


class VanillaRecommend(RecommendStrategy):
    def get_action(self, node: "Root") -> MctsActionType:
        return max(node._edges, key=lambda action: node._edges[action].visits)


class RecommendWinrate(RecommendStrategy):
    def get_action(self, node: "Root") -> MctsActionType:
        return max(
            node._edges,
            key=lambda action: node._edges[action].reward_sum
            / node._edges[action].visits
            if node._edges[action].visits > 0
            else 0,
        )


class RecommendMinimax(RecommendStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.minmax = Minmax()
        self.fallback_recommend = VanillaRecommend()

    def get_action(self, node: "Root") -> MctsActionType:
        """Pick the action for which the opponent's best play is as bad as possible"""
        optional_scores: dict[MctsActionType, float | None] = {
            action: self.minmax.value(edge) for action, edge in node._edges.items()
        }
        scores: dict[MctsActionType, float] = {
            a: s for a, s in optional_scores.items() if s is not None
        }
        if len(scores) == 0:
            return self.fallback_recommend.get_action(node)
        return max(scores, key=lambda action: scores[action])
