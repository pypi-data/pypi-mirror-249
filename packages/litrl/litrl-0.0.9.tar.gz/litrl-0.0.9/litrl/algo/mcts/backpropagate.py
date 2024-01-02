from abc import ABC, abstractmethod
from typing import Self

from litrl.algo.mcts.node import ChildNode
from litrl.algo.mcts.typing import AnyNode


class BackpropagateStrategy(ABC):
    @classmethod
    @abstractmethod
    def backpropagate(cls: type[Self], node: AnyNode, reward: float) -> None:
        ...


class VanillaBackpropagate(BackpropagateStrategy):
    @classmethod
    def backpropagate(cls: type[Self], node: AnyNode, reward: float) -> None:
        if not isinstance(node, ChildNode):  # root node
            return
        node.parent_edge.update(reward)
        cls.backpropagate(node.parent, reward)
