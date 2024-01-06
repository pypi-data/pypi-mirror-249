from typing import Optional, Tuple
from gymnasium.core import ActType, ObsType

from popgym.core.env import POPGymEnv
from popgym.core.wrapper import POPGymWrapper


class EpisodeStart(POPGymWrapper):
    """Wrapper that adds an episode_start flag to step

    The episode_start flag will be set for the first step of each episode.
    It will be unset in all other cases.

    Args:
        env: The environment

    Returns:
        A gym environment
    """

    def __init__(self, env: POPGymEnv, null_action: Optional[ActType] = None):
        super().__init__(env)

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        obs, reward, terminated, truncated, info = self.env.step(action)
        return obs, reward, terminated, truncated, False, info

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        return obs, True, info
