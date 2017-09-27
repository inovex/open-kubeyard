import argparse
import logging
from collections import deque
from itertools import repeat

import numpy as np
import tensorflow as tf

from a3c.agent import Agent
from a3c.environment import GymEnvironment
from a3c.network import A3CNetwork

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument('--samples_dir', default='TMP/samples', type=str,
                    help='Record directory path.', dest='samples_dir')
parser.add_argument('--output_dir', default='TMP/batch_trained', type=str,
                    help='Output directory path.', dest='output_dir')


def produce_trainings_data(gameplay):
    obs_ts = gameplay['obs_ts']
    obs_tp1s = gameplay['obs_tp1s']
    actions = gameplay['actions']
    rewards = gameplay['rewards']

    trainings_batches = []

    history_length = 4
    history = deque(maxlen=4)
    si_batch = []
    ac_batch = []
    r_batch = []

    # bootstrap first state
    obs = GymEnvironment.preprocess_frame(obs_ts[0], (32, -16), (84, 84), True)
    history.extend(repeat(obs, history_length))
    state = np.moveaxis(np.array(history), 0, -1)
    si_batch.append(state)
    ac_batch.append(actions[0])
    r_batch.append(rewards[0])

    for obs_t, obs_tp1, action, reward in zip(obs_ts[1:], obs_tp1s[1:], actions[1:], rewards[1:]):
        obs = GymEnvironment.preprocess_frame(obs_t, (32, -16), (84, 84), True)

        history.popleft()
        history.append(obs)
        state = np.moveaxis(np.array(history), 0, -1)

        si_batch.append(state)
        ac_batch.append(action)
        r_batch.append(reward)

        if len(si_batch) >= 20:
            obs = GymEnvironment.preprocess_frame(obs_tp1, (32, -16), (84, 84), True)
            history.popleft()
            history.append(obs)
            new_state = np.moveaxis(np.array(history), 0, -1)

            trainings_batches.append((si_batch, ac_batch, r_batch, new_state))
            si_batch = []
            ac_batch = []
            r_batch = []

    return trainings_batches


def main(args):
    """
    1) Load recorded gameplay
    2) Apply preprocessing
    3) Train model
    4) Export trained model

    Args:
        args: command line arguments.

    Returns:
        None
    """
    # summary_writer = tf.summary.FileWriter('{}/worker-{}'.format('logging', args.task_index))

    network = A3CNetwork([84, 84, 4], 3, False)
    step = tf.get_variable('step', [], tf.int32,
                           tf.constant_initializer(0, tf.int32),
                           trainable=False)

    predicted_action = network.action
    human_action = tf.placeholder(tf.int32, [None], 'Human_Action')
    discounted_reward = tf.placeholder(tf.float32, [None], 'Discounted_Reward')

    policy_loss = tf.nn.l2_loss(tf.cast(predicted_action, tf.float32) - tf.cast(human_action, tf.float32))
    value_loss = tf.nn.l2_loss(network.value - discounted_reward)
    loss = policy_loss + 0.5 * value_loss

    opt = tf.train.AdamOptimizer(learning_rate=0.001)

    batch_size = tf.to_float(tf.shape(network.input)[0])
    tf.summary.scalar('model/loss', loss / batch_size)

    summary_op = tf.summary.merge_all()

    inc_step = step.assign_add(tf.shape(network.input)[0])

    train_op = tf.group(opt.minimize(loss), inc_step)

    record_path = '{}/Breakout-v0_2017-07-14_11:07:15.npz'.format(args.samples_dir)

    with np.load(record_path) as data:
        gameplay = {
            'obs_ts': data['obs_ts'],
            'obs_tp1s': data['obs_tp1s'],
            'actions': data['actions'],
            'rewards': data['rewards']
        }

    trainings_batches = produce_trainings_data(gameplay)

    saver = tf.train.Saver()
    summary_writer = tf.summary.FileWriter('{}'.format(args.output_dir))

    # train
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for i in range(100):
            for si_batch, ac_batch, r_batch, last_state in trainings_batches[1:]:
                clipped_rewards = np.clip(r_batch, -1, 1)
                next_value = network.estimate_value(last_state, None)
                discounted_rewards = Agent.apply_discount(np.append(clipped_rewards, next_value), 0.99)[:-1]

                feed_dict = {network.input: np.asarray(si_batch),
                             human_action: np.asarray(ac_batch),
                             discounted_reward: discounted_rewards}
                step_, summary = sess.run([train_op, step, summary_op], feed_dict)[1:]
                summary_writer.add_summary(summary, global_step=step_)

        saver.save(sess, '{}/human_batch_model'.format(args.output_dir), global_step=step)

    summary_writer.flush()
    summary_writer.close()


if __name__ == '__main__':
    main(parser.parse_args())
