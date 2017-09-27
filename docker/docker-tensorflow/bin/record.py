import argparse
import datetime
import logging
from contextlib import suppress
from pathlib import Path  # requires python 3.5+

import gym
import numpy as np
from gym.utils.play import play

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument('-g', '--game_name', default='Breakout-v0', type=str,
                    help='Name of the game (environment).', dest='game_name')
parser.add_argument('-r', '--record_dir', default='TMP/samples', type=str,
                    help='Records will be saved to this directory.', dest='record_dir')
parser.add_argument('-z', '--zoom', default=2, type=int,
                    help='Make screen edge this many times bigger.', dest='zoom')
parser.add_argument('-f', '--fps', default=30, type=int,
                    help='Maximum number of steps of the environment to execute every second. Defaults to 30.',
                    dest='fps')


def callback(obs_t, obs_tp1, action, rew, done, _):
    global recording, obs_ts, obs_tp1s, actions, rewards

    if recording:
        obs_ts.append(obs_t)
        obs_tp1s.append(obs_tp1)
        actions.append(action)
        rewards.append(rew)
    else:
        if not np.array_equal(obs_t, obs_tp1):
            recording = True

    if done:
        dump_current_gameplay()
        obs_ts = []
        obs_tp1s = []
        actions = []
        rewards = []
        recording = False


def dump_current_gameplay():
    if obs_ts:
        np.savez_compressed(
            '{}/{}_{}'.format(args.record_dir, args.game_name,
                              str(datetime.datetime.now()).split('.')[0].replace(' ', '_')), obs_ts=obs_ts,
            obs_tp1s=obs_tp1s, actions=actions, rewards=rewards)


if __name__ == '__main__':
    args = parser.parse_args()
    env = gym.make(args.game_name)

    Path(args.record_dir).mkdir(parents=True, exist_ok=True)

    obs_ts = []
    obs_tp1s = []
    actions = []
    rewards = []

    recording = False

    with suppress(KeyboardInterrupt):
        play(env, zoom=args.zoom, fps=args.fps, callback=callback)

    dump_current_gameplay()
