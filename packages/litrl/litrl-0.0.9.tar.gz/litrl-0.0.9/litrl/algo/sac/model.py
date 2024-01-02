import random
import warnings
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import gymnasium as gym
import lightning as L
import numpy as np
import numpy.typing as npt
import torch
import torch.nn.functional as F
from gymnasium.spaces import Box, Discrete
from lightning.pytorch.utilities.types import STEP_OUTPUT
from loguru import logger
from tensordict import tensorclass
from torch import nn
from torch.distributions.categorical import Categorical
from torch.optim import Optimizer
from torchmetrics import MeanSquaredError
from torchmetrics.aggregation import RunningMean
from torchrl.data import LazyMemmapStorage, TensorDictReplayBuffer
from torchrl.data.replay_buffers.replay_buffers import TensorDictReplayBuffer
from tqdm.auto import tqdm

from litrl.common.constants import ILLEGAL_LOGIT
from litrl.common.dummy_loader import DummyLoader
from litrl.common.schema import ModelConfigSchema

if TYPE_CHECKING:
    from litrl.wrappers import StaticOpponentWrapper

ObsType = npt.NDArray[np.float64]
Mask = npt.NDArray[np.int8] | None
ProcessedObsType = torch.Tensor
ActionType = np.int64
InfoType = dict

EnvType = TypeVar("EnvType", gym.Env, "StaticOpponentWrapper")


class Critic(nn.Module):
    def __init__(self, obs_features: int, n_actions: int, hidden_size: int) -> None:
        super().__init__()
        self.q1 = nn.Sequential(
            nn.Linear(obs_features, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions),
        )
        self.q2 = nn.Sequential(
            nn.Linear(obs_features, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.min(self.q1(x), self.q2(x))


class Actor(nn.Module):
    def __init__(self, obs_features: int, n_actions: int, hidden_size: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_features, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

    def get_action(self, obs: torch.Tensor, mask: torch.Tensor) -> int:
        logits = self.forward(obs).flatten()
        logits[~mask.astype(bool)] = ILLEGAL_LOGIT
        policy_dist = Categorical(logits=logits)
        action = policy_dist.sample()
        return action.item()


@tensorclass
class Experience:
    obs: torch.Tensor
    mask: torch.Tensor | None
    action: torch.Tensor
    next_obs: torch.Tensor
    reward: torch.Tensor
    terminated: torch.Tensor
    truncated: torch.Tensor


ConfigType = TypeVar("ConfigType", bound="ModelConfigSchema")


class Sac(L.LightningModule, Generic[EnvType, ConfigType]):
    def __init__(
        self,
        cfg: ConfigType,
    ) -> None:
        logger.info(f"Initializing {self.__class__.__name__} model")
        super().__init__()
        self.cfg = cfg
        self.save_hyperparameters()
        self.env = cfg.env_fabric.instantiate()
        self.val_env = cfg.val_env_fabric.instantiate()
        self.seed_all()
        self.obs, info = self.reset(self.env)
        self.mask = info.get("action_mask")
        self.build_network()
        self.buffer = TensorDictReplayBuffer(
            storage=LazyMemmapStorage(max_size=self.cfg.buffer.max_size),
            batch_size=self.cfg.buffer.batch_size,
        )
        self.critic_criterion = MeanSquaredError()
        # fake warning in torchmetrics 1.2.1
        warnings.filterwarnings(
            "ignore",
            message=".*The ``compute`` method of metric MeanMetric was*",
        )
        self.train_reward_metric = RunningMean(window=100)
        self.val_metric = RunningMean(window=5)
        self.net: torch.nn.Module
        self.automatic_optimization = False
        self.log_alpha = torch.tensor(0.0, requires_grad=True)

    def teardown(self, stage: str) -> None:
        self.env.close()
        self.val_env.close()
        super().teardown(stage)

    def seed_all(self) -> None:
        random.seed(self.cfg.seed)
        np.random.seed(self.cfg.seed)
        torch.manual_seed(self.cfg.seed)
        self.env.reset(seed=self.cfg.seed)
        self.val_env.reset(
            seed=self.cfg.seed + 1,
        )  # seeds should be different for train and val

    @property
    def alpha(self) -> float:
        return self.log_alpha.exp().item()

    def build_network(self) -> torch.nn.Sequential:
        obs_features = 1
        n_actions, observation_shape = self.get_shapes()
        for dim in observation_shape:
            obs_features *= dim
        logger.debug(f"obs_features: {obs_features}, n_actions: {n_actions}")

        self.actor = Actor(obs_features, n_actions, self.cfg.hidden_size)
        self.critic = Critic(obs_features, n_actions, self.cfg.hidden_size)
        self.critic_target = deepcopy(self.critic)

    def experience_step(self, action: ActionType) -> torch.Tensor | None:
        next_obs, reward, terminated, truncated, info = self.env_step(self.env, action)
        experience = Experience(
            obs=self.obs,
            mask=torch.tensor(self.mask).unsqueeze(0)
            if self.mask is not None
            else None,
            action=torch.tensor(action, dtype=torch.int64).unsqueeze(0),
            next_obs=next_obs,
            reward=torch.tensor(reward, dtype=torch.float32).unsqueeze(0),
            terminated=torch.tensor(terminated, dtype=torch.int8).unsqueeze(0),
            truncated=torch.tensor(truncated, dtype=torch.int8).unsqueeze(0),
            batch_size=(1,),
        )
        self.buffer.extend(experience)  # pylint: disable=no-member
        if terminated or truncated:
            episode_reward = torch.tensor(info["episode"]["r"].item())
            next_obs, info = self.reset(self.env)
        else:
            episode_reward = None
        self.obs = next_obs
        self.mask = info.get("action_mask")
        return episode_reward

    def env_step(
        self,
        env: EnvType,
        action: ActionType,
    ) -> tuple[ProcessedObsType, float, bool, bool, InfoType]:
        obs, reward, terminated, truncated, info = env.step(action)
        return self.process_obs(obs), reward, terminated, truncated, info

    def get_shapes(self) -> tuple[int, tuple[int, ...]]:
        if not isinstance(self.env.action_space, Discrete):
            raise ValueError(self.env.action_space, "env action_space is not Discrete")
        if not isinstance(self.env.observation_space, Box):
            raise ValueError(
                f"{self.env.observation_space} env observation space is not a Box",
            )
        action_shape = self.env.action_space.n
        observation_shape = self.env.observation_space.shape
        return action_shape, observation_shape

    def acquire_experience(self) -> None:
        if random.random() < self.cfg.epsilon:
            action = self.random_action(self.mask)
        else:
            action = self.actor.get_action(self.obs, self.mask)
        episode_reward = self.experience_step(action)
        if episode_reward is not None:
            self.train_reward_metric.update(episode_reward)
            self.log(
                "episode_reward",
                self.train_reward_metric.compute(),
                prog_bar=True,
            )

    def training_step(self, batch: Experience, _):
        optimizers: tuple[Optimizer, ...] = self.optimizers()
        actor_optimizer, critic_optimizer, alpha_optimizer = optimizers
        self.acquire_experience()

        # CRITIC training
        with torch.no_grad():
            logits = self.actor(batch.next_obs)
            next_q = self.critic_target(batch.next_obs)
            log_prob = F.log_softmax(logits, dim=1)
            action_probs = Categorical(logits=logits).probs
            action_values = next_q - self.alpha * log_prob
            next_q_target = (action_probs * action_values).sum(1)  # weighted averaging
            q_target = (
                batch.reward + (1 - batch.terminated) * self.cfg.gamma * next_q_target
            )

        q1: torch.Tensor = self.critic.q1(batch.obs)
        q1 = q1.gather(1, batch.action.unsqueeze(1)).squeeze(1)

        q2: torch.Tensor = self.critic.q2(batch.obs)
        q2 = q2.gather(1, batch.action.unsqueeze(1)).squeeze(1)

        critic_loss = self.critic_criterion(q1, q_target) + self.critic_criterion(
            q2,
            q_target,
        )
        critic_optimizer.zero_grad()
        self.manual_backward(critic_loss)
        critic_optimizer.step()

        # ACTOR training
        logits = self.actor(batch.obs)
        log_prob = F.log_softmax(logits, dim=1)
        action_probs: torch.Tensor = Categorical(logits=logits).probs
        with torch.no_grad():
            q = self.critic(batch.obs)
        actor_loss = (action_probs * ((self.alpha * log_prob) - q)).mean()
        actor_optimizer.zero_grad()
        self.manual_backward(actor_loss)
        actor_optimizer.step()

        # ALPHA training
        alpha_loss = (
            action_probs.detach()
            * (-self.log_alpha.exp() * (log_prob + self.cfg.target_entropy).detach())
        ).mean()
        alpha_optimizer.zero_grad()
        self.manual_backward(alpha_loss)
        alpha_optimizer.step()

    def configure_optimizers(self):
        actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=self.cfg.lr)
        critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=self.cfg.lr)
        alpha_optimizer = torch.optim.Adam([self.log_alpha], lr=self.cfg.lr)
        return actor_optimizer, critic_optimizer, alpha_optimizer

    def reset(self, env: EnvType) -> tuple[ProcessedObsType, InfoType]:
        obs, info = env.reset()
        return self.process_obs(obs), info

    @torch.no_grad()
    def validation_step(self, batch: Any) -> None:
        """Play against benchmark static opponent"""
        del batch
        obs, info = self.reset(self.val_env)
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = self.actor.get_action(obs, info["action_mask"])
            obs, _, terminated, truncated, info = self.env_step(self.val_env, action)

        return torch.tensor(info["episode"]["r"].item())

    def random_action(self, mask: Mask) -> ActionType:
        return self.env.action_space.sample(mask)

    def train_dataloader(self):
        logger.warning("The dataloader is not loaded from a previous checkpoint")
        for _ in (pbar := tqdm(range(int(self.cfg.warm_start_steps)))):
            pbar.set_description("Warm start, collecting experience with random policy")
            action = self.random_action(self.mask)
            self.experience_step(action)
        return self.buffer

    def val_dataloader(self):
        """Return a dummy dataset that will be ignored"""
        return DummyLoader()

    @staticmethod
    def process_obs(obs: ObsType) -> ProcessedObsType:
        return torch.tensor(obs.flatten(), dtype=torch.float32).unsqueeze(0)

    def polyak_update(
        self,
        source: torch.nn.Module,
        target: torch.nn.Module,
        tau: float,
    ) -> None:
        for source_param, target_param in zip(source.parameters(), target.parameters()):
            target_param.data.copy_(
                tau * source_param.data + (1 - tau) * target_param.data,
            )

    def on_train_batch_end(
        self,
        outputs: STEP_OUTPUT,
        batch: Any,
        batch_idx: int,
    ) -> None:
        self.polyak_update(self.critic, self.critic_target, self.cfg.tau)
        return super().on_train_batch_end(outputs, batch, batch_idx)

    def on_validation_batch_end(
        self,
        outputs: STEP_OUTPUT,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        self.val_metric(outputs)
        running_mean = self.val_metric.compute()
        self.log(
            "val_reward",
            running_mean,
            prog_bar=True,
            batch_size=1,
        )
        return super().on_validation_batch_end(
            outputs,
            batch,
            batch_idx,
            dataloader_idx,
        )
