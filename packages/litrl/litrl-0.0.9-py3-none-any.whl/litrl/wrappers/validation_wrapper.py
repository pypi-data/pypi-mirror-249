from datetime import datetime
from typing import Generic

import gymnasium as gym
from dateutil import tz  # type: ignore[import-untyped]
from gymnasium.core import Wrapper, WrapperActType, WrapperObsType
from gymnasium.wrappers.record_episode_statistics import RecordEpisodeStatistics
from gymnasium.wrappers.record_video import RecordVideo

from litrl.env.typing import ActType, ObsType
from litrl.wrappers.static_opponent_wrapper import AgentType, StaticOpponentWrapper


class ValidationWrapper(
    Wrapper[WrapperObsType, WrapperActType, ObsType, ActType],
    Generic[AgentType, WrapperObsType, WrapperActType, ObsType, ActType],
):
    def __init__(
        self,
        env: gym.Env[ObsType, ActType]
        | StaticOpponentWrapper[ObsType, ActType, AgentType],
        render_each_n_episodes: int,
    ):
        self.render_each_n_episodes = render_each_n_episodes

        def episode_trigger(episode: int) -> bool:
            return episode % self.render_each_n_episodes == 0

        super().__init__(
            RecordVideo(
                env=RecordEpisodeStatistics(env),
                video_folder=f"temp/{env}/{datetime.now(tz.UTC)}",
                episode_trigger=episode_trigger,
                disable_logger=True,
            ),
        )
