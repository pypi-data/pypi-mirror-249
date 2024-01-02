from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np
import onnxruntime
import scipy
from huggingface_hub import hf_hub_download

from litrl.algo.sac.model import Actor
from litrl.common.agent import Agent
from litrl.common.observation import process_obs
from litrl.env.typing import MultiAgentEnv


class SacAgent(Agent, ABC):
    def __init__(self, actor: Actor):
        super().__init__()
        self._actor = actor

    def update(self, actor: Actor) -> None:
        self._actor = actor

    @abstractmethod
    def get_action(self, env: MultiAgentEnv) -> int:
        raise NotImplementedError


class SacStochasticAgent(SacAgent):
    def get_action(self, env: MultiAgentEnv) -> int:
        obs = env.observe(env.unwrapped.agent_selection)
        return self._actor.get_action(
            process_obs(obs["observation"]),
            obs["action_mask"],
        )


class OnnxSacAgent(SacAgent, ABC):
    def __init__(self, onnx_path: Path | None = None) -> None:
        if onnx_path is None:
            onnx_path = Path(
                hf_hub_download(repo_id="c-gohlke/connect4SAC", filename="model.onnx"),
            )
        self.onnx_model = onnxruntime.InferenceSession(onnx_path)

    def get_logits(self, env: MultiAgentEnv) -> np.ndarray:
        obs = env.observe(env.unwrapped.agent_selection)
        processed_obs = np.expand_dims(obs["observation"].flatten(), axis=0).astype(
            np.float32,
        )
        onnx_inputs = {self.onnx_model.get_inputs()[0].name: processed_obs}
        logits = np.array(self.onnx_model.run(None, onnx_inputs)).flatten()
        logits[~obs["action_mask"].astype(bool)] = -1e5
        return logits

    @abstractmethod
    def get_action(self, env: MultiAgentEnv) -> int:
        raise NotImplementedError


class OnnxSacDeterministicAgent(OnnxSacAgent):
    def get_action(self, env: MultiAgentEnv) -> int:
        logits = self.get_logits(env)
        action = np.argmax(logits)
        return action


class OnnxSacStochasticAgent(OnnxSacAgent):
    def get_action(self, env: MultiAgentEnv) -> int:
        logits = self.get_logits(env)
        probs = scipy.special.softmax(logits, axis=-1)
        action = np.random.choice(len(probs), p=probs)
        return action
