import argparse
import logging
import signal
import sys
from contextlib import suppress

import tensorflow as tf

from a3c.agent import Agent
from a3c.config import Config
from a3c.environment import GymEnvironment

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

parser = argparse.ArgumentParser()

# Distributed
parser.add_argument('--ps_hosts', default='0.0.0.0:2222', type=str,
                    help='Comma-separated list of hostname:port pairs', dest='ps_hosts')
parser.add_argument('--worker_hosts', default='0.0.0.0:2223', type=str,
                    help='Comma-separated list of hostname:port pairs', dest='worker_hosts')
parser.add_argument('--job_name', type=str,
                    help='Name of the job: one of "ps" or "worker"', dest='job_name')
parser.add_argument('--task_index', default=0, type=int,
                    help='Index of task within the job', dest='task_index')


# Disables write_meta_graph argument, which freezes entire process and is mostly useless.
class FastSaver(tf.train.Saver):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def save(self,
             sess,
             save_path,
             global_step=None,
             latest_filename=None,
             meta_graph_suffix="meta",
             write_meta_graph=True,
             write_state=True):
        super(FastSaver, self).save(sess, save_path, global_step, latest_filename, meta_graph_suffix, False,
                                    write_state)


def main(args):
    def shutdown_thread(signal_, _):
        LOGGER.warning('Received signal %s: exiting', signal_)
        if args.job_name == 'worker':
            worker_cleanup()
        sys.exit(signal_ + 128)

    def worker_cleanup():
        supervisor.stop()
        if summary_writer:
            summary_writer.flush()
            summary_writer.close()
        env.env.close()
        sys.stdout.flush()

    ps_hosts = args.ps_hosts.split(',')
    worker_hosts = args.worker_hosts.split(',')

    cluster = tf.train.ClusterSpec({'ps': ps_hosts, 'worker': worker_hosts})

    if args.job_name == 'ps':
        config = tf.ConfigProto(device_filters=['/job:ps'])
    elif args.job_name == 'worker':
        config = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=2)
    else:
        raise ValueError('invalid --job_name {}. Valid ones are [ps, worker]'.format(args.job_name))

    server = tf.train.Server(cluster,
                             job_name=args.job_name,
                             task_index=args.task_index,
                             config=config)

    if args.job_name == 'worker':
        # Starts a worker thread that learns how to play the specified Atari game.
        is_chief = (args.task_index == 0)

        if Config.PLAY_MODE:
            summary_writer = None
        else:
            summary_writer = tf.summary.FileWriter('{}/worker-{}'.format(Config.LOG_DIR, args.task_index))

        # Initialize the model.
        env = GymEnvironment(env_id=Config.GAME,
                             visualize=Config.RENDER or Config.PLAY_MODE,
                             preprocessing=True,
                             frame_height=Config.IMAGE_HEIGHT,
                             frame_width=Config.IMAGE_WIDTH,
                             crop_top=Config.CROP_TOP,
                             crop_bottom=Config.CROP_BOTTOM,
                             grayscale=True,
                             history_length=Config.STACKED_FRAMES)
        player = Agent(args.task_index, env, summary_writer=summary_writer, lstm=Config.USE_LSTM)

        # Local copies of the model will not be saved
        model_variables = [var for var in tf.global_variables() if not var.name.startswith('local')]

        saver_class = tf.train.Saver if Config.WRITE_META_GRAPH else FastSaver
        saver = saver_class(model_variables, max_to_keep=Config.MAX_TO_KEEP,
                            keep_checkpoint_every_n_hours=Config.KEEP_CHECKPOINT_EVERY_N_HOUR)

        supervisor = tf.train.Supervisor(ready_op=tf.report_uninitialized_variables(model_variables),
                                         is_chief=is_chief,
                                         init_op=tf.variables_initializer(model_variables),
                                         logdir=Config.CHECKPOINT_DIR,
                                         summary_op=None,
                                         saver=saver,
                                         global_step=player.global_step,
                                         save_model_secs=Config.SAVE_MODEL_SECS,
                                         summary_writer=summary_writer)

        config = tf.ConfigProto(device_filters=['/job:ps',
                                                '/job:worker/task:{}/cpu:0'.format(args.task_index)],
                                log_device_placement=Config.LOG_DEVICE_PLACEMENT)

        LOGGER.info('Starting worker-{} session. This may take a while.'.format(args.task_index))
        with supervisor.managed_session(server.target, config=config) as sess, sess.as_default():
            global_step = sess.run(player.global_step)
            LOGGER.info('Starting training at global step {:,}.'.format(global_step))
            with suppress(KeyboardInterrupt):
                while not supervisor.should_stop() and global_step < Config.STEPS_MAX:
                    global_step = player.train(sess)
        worker_cleanup()
        LOGGER.info('Worker-{} stopped after {:,} global steps.'.format(args.task_index, global_step))

    # Ensure that threads are terminated gracefully.
    signal.signal(signal.SIGHUP, shutdown_thread)
    signal.signal(signal.SIGINT, shutdown_thread)
    signal.signal(signal.SIGTERM, shutdown_thread)

    if args.job_name == 'ps':
        LOGGER.info('PS started.')
        # Keep running. Unfortunately server.join() blocks for ever, which means Ctrl+C doesn't stop process...
        signal.pause()


if __name__ == '__main__':
    main(parser.parse_args())
