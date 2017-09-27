import argparse
import logging
import sys
from contextlib import suppress
from pathlib import Path  # requires python 3.5+
from timeit import default_timer as timer

import matplotlib.pyplot as plt
import tensorflow as tf

from a3c.agent import Agent
from a3c.config import Config
from a3c.environment import GymEnvironment

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument('-gn', '--game_name', default=Config.GAME, type=str,
                    help='Name of the game (environment).', dest='game_name')
parser.add_argument('-cd', '--checkpoint_dir', default=Config.CHECKPOINT_DIR, type=str,
                    help='Path to checkpoint dir.', dest='checkpoint_dir')
parser.add_argument('-ev', '--evaluate', help='Evaluate agent while playing (without visualisation).',
                    action='store_true')
parser.add_argument('-pd', '--plays_dir', default=None, type=str,
                    help='Enables monitoring of plays. Stores video files in this directory.', dest='plays_dir')
parser.add_argument('-l', '--lstm', default=Config.USE_LSTM,
                    help='Trained model has a LSTM network architecture.', action='store_true')
parser.add_argument('-spd', '--save_plot_dir', default=None, type=str,
                    help='Save a plot of evaluation results.', dest='save_plot_dir')


def plot_result(title, result, save_dir):
    plt.title('{} - Evaluation\n max: {} min: {} avg: {:.2f}'.
              format(title, result['max_reward'], result['min_reward'], result['avg_reward']))
    plt.plot(list(range(result['episodes'])), result['rewards'])
    plt.axhline(y=result['avg_reward'], color='gray', linestyle='dashed', linewidth=1)
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.savefig('{}/{}_eval_{}-{}-{:.2f}.png'.format(save_dir, title, result['max_reward'], result['min_reward'],
                                                     result['avg_reward']), bbox_inches='tight', transparent=True)


def main(args):
    if args.plays_dir:
        Path(args.plays_dir).mkdir(parents=True, exist_ok=True)
    if args.save_plot_dir:
        Path(args.save_plot_dir).mkdir(parents=True, exist_ok=True)

    env = GymEnvironment(args.game_name, not args.evaluate, True, Config.IMAGE_HEIGHT, Config.IMAGE_WIDTH,
                         Config.CROP_TOP, Config.CROP_BOTTOM, True, Config.STACKED_FRAMES, args.plays_dir)
    player = Agent(0, env, play_mode=True, lstm=args.lstm)

    with tf.Session() as sess, sess.as_default():
        LOGGER.info('Restore checkpoint...')
        tf.train.Saver().restore(sess, tf.train.latest_checkpoint(args.checkpoint_dir))

        if args.evaluate:
            LOGGER.info('Start evaluation...')
            result = player.test(100)  # calculates 100-episode average reward
            LOGGER.info('Evaluation finished. Episodes tested: {}. Reward (max/min/avg): {}/{}/{}. '
                        'Best episode: {}. Worst episode: {}.'.format(result['episodes'], result['max_reward'],
                                                                      result['min_reward'], result['avg_reward'],
                                                                      result['best_episode'], result['worst_episode']))
            if args.save_plot_dir:
                plot_result(args.game_name, result, args.save_plot_dir)
        else:
            LOGGER.info('Start playing...')
            t_start = timer()
            with suppress(KeyboardInterrupt):
                for _ in range(100000):
                    player.play()

            t_sec = round(timer() - t_start)
            (t_min, t_sec) = divmod(t_sec, 60)
            (t_hour, t_min) = divmod(t_min, 60)
            LOGGER.info('Stop playing. Total playtime: {:02d}:{:02d}:{:02d} (h:m:s)'.format(t_hour, t_min, t_sec))

    env.env.close()
    sys.stdout.flush()


if __name__ == '__main__':
    main(parser.parse_args())
