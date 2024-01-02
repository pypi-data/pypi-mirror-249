from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from litrl.algo.mcts.edge import Edge
from litrl.algo.mcts.value import ValueStrategy, Winrate

if TYPE_CHECKING:
    from litrl.algo.mcts.typing import AnyNode, MctsActionType

EdgeType = TypeVar("EdgeType", Edge, None)


class Node(Generic[EdgeType], ABC):
    def __init__(
        self,
        parent_edge: EdgeType,
        root_player_turn: bool,
        value_strategy: ValueStrategy = Winrate(),
        exploration_coef: float = 1,
    ):
        self.parent_edge: EdgeType = parent_edge
        self._edges: dict["MctsActionType", Edge] = {}
        self._exploration_coef = exploration_coef
        self._value_strategy = value_strategy
        self.root_player_turn = root_player_turn

    def add_child(self, action: "MctsActionType") -> None:
        edge = Edge(parent=self)
        self._edges[action] = edge
        edge._child = ChildNode(parent_edge=edge)

    @property
    def visits(self) -> float:
        return sum(edge.visits for edge in self._edges.values())

    @property
    def reward_sum(self) -> float:
        return sum(edge.reward_sum for edge in self._edges.values())

    @property
    @abstractmethod
    def parent(self) -> Optional["AnyNode"]:
        raise NotImplementedError

    @property
    def n_children(self) -> int:
        return len(self._edges)

    @property
    def children(self) -> dict["MctsActionType", "ChildNode"]:
        return {action: edge._child for action, edge in self._edges.items()}


class Root(Node[None]):
    def __init__(self) -> None:
        super().__init__(parent_edge=None, root_player_turn=True)

    @property
    def parent(self) -> None:
        return None


class ChildNode(Node["Edge"]):
    def __init__(self, parent_edge: "Edge") -> None:
        super().__init__(
            parent_edge=parent_edge,
            root_player_turn=not parent_edge._parent.root_player_turn,
        )

    @property
    def parent(self) -> "AnyNode":
        return self.parent_edge._parent
