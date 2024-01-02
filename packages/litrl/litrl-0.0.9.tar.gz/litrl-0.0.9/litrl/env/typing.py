import warnings
from abc import ABC
from typing import Generic, Self, TypedDict, TypeVar

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from nptyping import Shape

from typing import Any

from gymnasium.spaces import Space
from pettingzoo.utils import agent_selector  # type: ignore[import-untyped]

ActType = TypeVar("ActType")
ObsType = TypeVar("ObsType")
MaskType = TypeVar("MaskType")
ObsType_co = TypeVar("ObsType_co", covariant=True)
EnvType = TypeVar("EnvType")
ObsShape = TypeVar("ObsShape", bound=Shape)
MaskShape = TypeVar("MaskShape")
AgentID = TypeVar("AgentID")


class MaskedObs(TypedDict, Generic[ObsType, MaskType]):
    obs: ObsType  # NDArray[ObsShape, Float64]
    action_mask: MaskType  # NDArray[Shape[MaskShape], Int64]


class MaskedInfo(TypedDict, Generic[MaskType]):
    action_mask: MaskType  # NDArray[MaskShape, Int64]


class MultiAgentEnv(ABC, Generic[ObsType_co, ActType, AgentID]):
    """PettingZoo environments are not very mature yet and yield unexpected bugs.

    LitRL environments follow the gym/pettingzoo API as closely as possible,
    but we ensure the environments are stable by converting them to a MultiAgentEnv class.
    """

    agent_selection: AgentID
    unwrapped: Self
    truncations: dict[str, int]
    terminations: dict[str, int]
    infos: dict[str, Any]
    _cumulative_rewards: dict[str, float]
    rewards: dict[str, float]
    _agent_selector: agent_selector

    def step(self, action: ActType) -> None:
        raise NotImplementedError

    def last(self) -> tuple[ObsType_co, float, bool, bool, dict[str, Any]]:
        raise NotImplementedError

    def observe(self, agent: AgentID) -> ObsType_co:
        raise NotImplementedError

    def action_space(self, agent: AgentID) -> Space[ActType]:
        raise NotImplementedError

    def reset(
        self,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        raise NotImplementedError
