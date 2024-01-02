from abc import ABC, abstractmethod
from collections.abc import Iterator

from litrl.algo.mcts.typing import MctsActionType, MctsEnv
from litrl.common.agent import Agent, RandomMultiAgent


class RolloutStrategy(ABC):
    @abstractmethod
    def rollout(self, env: MctsEnv, as_player: str) -> float:
        ...


class VanillaRollout(RolloutStrategy):
    def __init__(
        self,
        rollout_agent: Agent[MctsEnv, MctsActionType] | None = None,
    ) -> None:
        super().__init__()
        self.rollout_agent = (
            rollout_agent if rollout_agent is not None else RandomMultiAgent()
        )

    def rollout(self, env: MctsEnv, as_player: str) -> float:
        _, reward, terminated, truncated, _ = env.last()
        while not (terminated or truncated):
            action = self.rollout_agent.get_action(env)
            env.step(action)
            _, reward, terminated, truncated, _ = env.last()

        if env.unwrapped.agent_selection != as_player:
            reward *= (
                -1
            )  # flip the sign. Reward observed from the opponent's perspective
        # use scale from 0 to 1:
        return max(reward, 0)


class HardcodedRolloutAgent(Agent):
    def __init__(self, actions: Iterator[int]) -> None:
        super().__init__()
        self.actions = actions

    def get_action(self, env: MctsEnv) -> int:
        del env
        return next(self.actions)
