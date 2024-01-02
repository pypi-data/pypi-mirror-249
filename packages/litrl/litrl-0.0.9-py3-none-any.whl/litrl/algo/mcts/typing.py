from typing import Any, TypeAlias

from litrl.algo.mcts.edge import Edge
from litrl.algo.mcts.node import Node
from litrl.env.typing import MultiAgentEnv

MctsActionType: TypeAlias = int
AnyNode: TypeAlias = Node["Edge"] | Node[None]
MctsEnv: TypeAlias = MultiAgentEnv[
    Any,
    Any,
    Any,
]  # don't care about observation type in MCTS
