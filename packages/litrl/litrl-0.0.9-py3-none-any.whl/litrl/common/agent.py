from abc import ABC, abstractmethod
from typing import Generic

from litrl.env.typing import ActType, AgentID, EnvType, MaskedObs, MaskShape, MultiAgentEnv, ObsShape


class Agent(ABC, Generic[EnvType, ActType]):
    @abstractmethod
    def get_action(self, env: EnvType) -> ActType:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__


class RandomMultiAgent(
    Agent[MultiAgentEnv[MaskedObs[ObsShape, MaskShape], ActType, AgentID], ActType],
    Generic[ObsShape, MaskShape, ActType, AgentID],
):
    def get_action(
        self,
        env: MultiAgentEnv[MaskedObs[ObsShape, MaskShape], ActType, AgentID],
    ) -> ActType:
        obs = env.observe(env.unwrapped.agent_selection)
        action_space = env.action_space(env.unwrapped.agent_selection)
        return action_space.sample(obs["action_mask"])
