from typing import Any, Literal, Self, TypeAlias

from nptyping import Shape
from pettingzoo.classic.connect_four_v3 import raw_env as ConnectFourRaw  # type: ignore[import-untyped]
from pettingzoo.utils import agent_selector  # type: ignore[import-untyped]

from litrl.env.typing import MaskedObs, MultiAgentEnv

Board: TypeAlias = list[list[int]]
FlatBoard: TypeAlias = list[int]
ConnectFourActType: TypeAlias = int
ConnectFourObsShape: TypeAlias = Shape["7, 6"]
ConnectFourMaskShape: TypeAlias = Shape["7"]
ConnectFourMaskedObs: TypeAlias = MaskedObs[ConnectFourObsShape, ConnectFourMaskShape]
ConnectFourAgentID: TypeAlias = Literal["player_0", "player_1"]


def flatten_board(board: Board) -> FlatBoard:
    return [item for row in board for item in row]


class ConnectFour(ConnectFourRaw, MultiAgentEnv[ConnectFourMaskedObs, ConnectFourActType, ConnectFourAgentID]):  # type: ignore[misc]
    """PettingZoo ConnectFour has multiple issues (reproducibility, typing) that we fix here."""

    def __init__(self, render_mode: str | None = None, screen_scaling: int = 9) -> None:
        super().__init__(render_mode=render_mode, screen_scaling=screen_scaling)
        self._agent_selector: agent_selector
        self.agent_selection: ConnectFourAgentID
        self.board: FlatBoard
        self.possible_agents: list[ConnectFourAgentID]

    @property
    def unwrapped(self) -> Self:  # type: ignore[override]
        """Wrappers override this function to return the underlying raw environment."""
        return self

    def reset(
        self,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        super().reset(seed=seed, options=options)  # type: ignore[no-any-call]
        for agent_id in self.possible_agents:
            self.action_space(agent=agent_id).seed(seed=seed)  # type: ignore[no-any-call]
