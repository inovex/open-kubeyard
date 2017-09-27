from itertools import repeat
from pathlib import Path  # requires python 3.5+
from queue import deque
from timeit import default_timer as timer
from typing import Tuple

import gym
import numpy as np
from PIL import Image
from gym import wrappers


class GymEnvironment(object):
    def __init__(self,
                 env_id: str,
                 visualize: bool = False,
                 preprocessing: bool = True,
                 frame_height: int = 84,
                 frame_width: int = 84,
                 crop_top: int = 32,
                 crop_bottom: int = 16,
                 grayscale: bool = True,
                 history_length: int = 4,
                 monitor_dir: str = None) -> None:
        """
        Small OpenAI Gym wrapper to enable preprocessing of observations
        and use of multiple observations as state.

        Args:
            env_id: ID of the Gym environment, e.g. Breakout-v0
            visualize: Show emulator?
            preprocessing: Use preprocessing?
            frame_height: Height of the preprocessed observation image.
            frame_width: Width of the preprocessed observation image.
            crop_top: Number of pixels the observation image is cropped from top by preprocessing (before resize).
            crop_bottom: Number of pixels the observation image is cropped from bottom by preprocessing (before resize).
            grayscale: Use grayscale image?
            history_length: How many frames building a state?
                1 only the current observation is used as a state,
                x last x-1 observations plus the current one build a state.
            monitor_dir: Directory to store videos of the agent playing. Pass None to disable monitoring.
        """
        assert crop_top >= 0 and crop_bottom >= 0
        assert frame_width > 0 and frame_height > 0
        assert history_length > 0

        self.env = gym.make(env_id)
        if monitor_dir:
            self.env = wrappers.Monitor(self.env, monitor_dir, video_callable=lambda episode_id: True)

        self.visualize = visualize
        self.preprocessing = preprocessing

        self.frame_size = (frame_width, frame_height)
        self.crop = (crop_top if crop_top > 0 else None, crop_bottom * -1 if crop_bottom > 0 else None)
        self.grayscale = grayscale

        self.history_length = history_length

        if self.env.spec.id == 'Pong-v0' or self.env.spec.id == 'Breakout-v0':
            # Gym returns 6 possible actions for breakout and pong.
            # E.g. Breakout 0=no-op, 1=fire, 2=right, 3=left, 4=right_fire, 5=left_fire
            # Pick from a simplified fire, right, left action space. (first time fire starts game then no-op)
            self.actions = [1, 2, 3]
        else:
            self.actions = range(self.env.action_space.n)

        # Screen buffer of size history_length to be able
        # to build state arrays of shape[width, height, {3}, history_length]
        self._history = None
        self.episode_reward = self.episode_length = self.episode_t_start = self.episode_run_time = 0

        self.state = self.reset()

    @staticmethod
    def get_num_actions(env_id: str) -> int:
        """
        Gets the available number of actions for the environment with given id.
        Args:
            env_id:

        Returns:
            number of actions an agent can choose

        """
        if env_id == 'Pong-v0' or env_id == 'Breakout-v0':
            return 3
        else:
            return gym.make(env_id).action_space.n

    def reset(self) -> np.ndarray:
        """
        Resets the state of the environment and returns a state based on observation.

        Returns:
            np.ndarray: The initial estimate for the state of the environment based on the observation made.

        """
        self._history = deque(maxlen=self.history_length)

        # Reset statistics
        self.episode_reward = 0
        self.episode_length = 0
        self.episode_t_start = timer()
        self.episode_run_time = 0

        obs = self.env.reset()

        if self.preprocessing:
            obs = GymEnvironment.preprocess_frame(obs, self.crop, self.frame_size, self.grayscale)

        self._history.extend(repeat(obs, self.history_length))
        self.state = np.moveaxis(np.array(self._history), 0, -1)  # get array of shape (frame_size, {3}, history_length)

        return self.state

    def step(self, action_index: int) -> Tuple[np.ndarray, float, bool]:
        """
        Run one timestep of the environment's dynamics.
        Accepts an action index and returns a tuple (state, reward, done)

        Args:
            action_index: The index of an action that will be executed in this timestep.

        Returns:
            3-element tuple containing:

            - **state**: estimate of the environment state
            - **reward**: amount of reward returned after previous action
            - **done**: whether the episode has ended, in witch case further step() calls will return
              undefined results, so call reset() to reset this environments state.
        """
        if self.visualize:
            self.env.render()

        obs, reward, done, _ = self.env.step(self.actions[action_index])

        if self.preprocessing:
            obs = GymEnvironment.preprocess_frame(obs, self.crop, self.frame_size, self.grayscale)

        self._history.popleft()
        self._history.append(obs)
        self.state = np.moveaxis(np.array(self._history), 0, -1)

        # Collect statistics
        self.episode_reward += reward
        self.episode_length += 1
        self.episode_run_time = timer() - self.episode_t_start

        return self.state, reward, done

    def render(self) -> None:
        """Render to the current display or terminal."""
        self.env.render()

    def sample_action(self):
        """Samples a random action."""
        return self.env.action_space.sample()

    def get_state(self) -> np.ndarray:
        """Gets the current state."""
        return self.state

    def get_statistics(self) -> Tuple[float, int, float]:
        """Gets statistic of current episode.

        Returns:
            3-element tuple containing:

            - **ep_reward**: sum of rewards collected in that episode
            - **ep_length**: total length of that episode
            - **ep_run_time**: total runtime of that episode in seconds.
        """
        return self.episode_reward, self.episode_length, self.episode_run_time

    def save_state_images(self, save_path: str = 'debug/current_state') -> None:
        """
        Stores current state on disk.

        Mainly for debugging purposes.
        Depending on history_length there are multiple images to store for one state.
        Lowest number is the oldest observation.

        Args:
            save_path: path to storage directory. Missing directories will be created.

        Returns:
            None
        """
        assert self.state is not None
        Path(save_path).mkdir(parents=True, exist_ok=True)

        # PIL Image requires values from 0 to 255
        value_correction = 255.0 if self.grayscale else 1

        # save state as images
        for i in range(self.history_length):
            Image.fromarray(self.state[..., i] * value_correction) \
                .convert('RGB') \
                .save('{}/frame_{}.png'.format(save_path, i))

    @staticmethod
    def preprocess_frame(frame, crop: Tuple[int, int], frame_size: Tuple[int, int], grayscale: bool) -> np.ndarray:
        """
        Preprocessing of given observation (image).
            0) Atari frames: 210 x 160 x 3
            1) Crop center (crop top/bottom according to the game. E.g. top/bottom 34 for Pong and Breakout)
            2) Rescale image: E.g. to 84 x 84 x 3
            3) Get image grayscale

        Args:
            frame: observation (image) preprocessing is applied to
            crop: (crop_top, crop_bottom) crop center. *Attention: crop_bottom must be either negative or None!*
            frame_size: size of the output frame
            grayscale: convert to grayscale?

        Returns:
            A frame_height x frame_width (x optional RGB) tensor with float32 values between 0 and 1.

        """
        frame = frame[crop[0]: crop[1], :]

        img = Image.fromarray(frame)
        img = img.resize(frame_size, Image.BOX)  # Image.NEAREST is faster, but ball pixels might get lost

        if grayscale:
            img = img.convert('L')

        return np.asarray(img, dtype=np.float32) / 255.0
