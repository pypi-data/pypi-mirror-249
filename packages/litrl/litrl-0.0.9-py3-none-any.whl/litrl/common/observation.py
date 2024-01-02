import numpy as np
import torch


def process_obs(obs: np.ndarray) -> torch.Tensor:
    return torch.tensor(obs.flatten(), dtype=torch.float32).unsqueeze(0)
