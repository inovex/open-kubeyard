import logging

import numpy as np
import tensorflow as tf
from scipy import signal

from .config import Config
from .environment import GymEnvironment
from .network import A3CNetwork

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class Agent(object):
    """
    An agent has its own model (instance of the network) and its own environment.
    1. The agent reads the parameters from the global network and updates its own model.
    2. Computes gradients locally, based on a batch of input data (collected by interaction with the environment) and
        the parameter values that read in step 1.
    3. After each x steps the agent sends the gradients for each variable to the appropriate PS (parameter server) task,
        and applies the gradients to their respective variable, using an update rule that is determined by the
        optimization algorithm (e.g. RMSPROP).
    """

    def __init__(self, id_, env: GymEnvironment, play_mode: bool = False, summary_writer: tf.summary.FileWriter = None,
                 lstm: bool = False):
        """

        Args:
            id_: Index of the worker thread that is running this agent.
            env: An AtariEnvironment object (see 'environment.py') that wraps over an OpenAI Gym Atari environment.
            summary_writer: A TensorFlow object that writes summaries. Not necessary in play mode.
            lstm: Set to True to use LSTM network architecture.
        """
        if not play_mode and summary_writer is None:
            raise ValueError('Parameter "summary_writer" is necessary for training!')

        self.id_ = id_
        self.env = env
        self.summary_writer = summary_writer
        self.use_lstm = lstm
        self.steps_since_last_summary = 0
        self.eps_since_last_summary = 0

        if play_mode:
            with tf.variable_scope('global'):  # only global vars were saved.
                self.local_network = A3CNetwork([Config.IMAGE_HEIGHT, Config.IMAGE_WIDTH, Config.STACKED_FRAMES],
                                                len(self.env.actions), lstm)
        else:
            worker_device = '/job:worker/task:{}/cpu:0'.format(id_)

            with tf.device(tf.train.replica_device_setter(ps_tasks=1, worker_device=worker_device)):
                with tf.variable_scope('global'):
                    self.global_network = A3CNetwork([Config.IMAGE_HEIGHT, Config.IMAGE_WIDTH, Config.STACKED_FRAMES],
                                                     len(self.env.actions), lstm)
                    self.global_step = tf.get_variable('global_step', [], tf.int32,
                                                       tf.constant_initializer(0, tf.int32),
                                                       trainable=False)

            with tf.device(worker_device):
                with tf.variable_scope('local'):
                    self.local_network = A3CNetwork([Config.IMAGE_HEIGHT, Config.IMAGE_WIDTH, Config.STACKED_FRAMES],
                                                    len(self.env.actions), lstm)
                    self.local_network.global_step = self.global_step

                self.action = tf.placeholder(tf.int32, [None], 'Action')
                self.advantage = tf.placeholder(tf.float32, [None], 'Advantage')
                self.discounted_reward = tf.placeholder(tf.float32, [None], 'Discounted_Reward')

                if Config.LEARNING_RATE_START == Config.LEARNING_RATE_END:
                    self.learning_rate = Config.LEARNING_RATE_START
                else:
                    self.learning_rate = tf.train.polynomial_decay(Config.LEARNING_RATE_START, self.global_step,
                                                                   Config.ANNEALING_STEPS,
                                                                   Config.LEARNING_RATE_END)

                # Estimate the policy loss using the cross-entropy loss function.
                action_logits = self.local_network.action_logits
                policy_loss = tf.reduce_sum(
                    self.advantage * tf.nn.sparse_softmax_cross_entropy_with_logits(logits=action_logits,
                                                                                    labels=self.action))

                # Regularize the policy loss by adding uncertainty (subtracting entropy). High entropy means
                # the agent is uncertain (meaning, it assigns similar probabilities to multiple actions).
                # Low entropy means the agent is sure of which action it should perform next.
                entropy = -tf.reduce_sum(tf.nn.softmax(action_logits) * tf.nn.log_softmax(action_logits))
                policy_loss -= Config.BETA * entropy

                # Estimate the value loss using the sum of squared errors.
                value_loss = tf.nn.l2_loss(self.local_network.value - self.discounted_reward)

                # Estimate the final loss.
                self.loss = policy_loss + 0.5 * value_loss

                # Fetch the gradients of the local network.
                gradients = tf.gradients(self.loss, self.local_network.parameters)

                # Collect summary
                batch_size = tf.to_float(tf.shape(self.local_network.input)[0])
                tf.summary.scalar('model/loss', self.loss / batch_size)
                tf.summary.scalar('model/policy_loss', policy_loss / batch_size)
                tf.summary.scalar('model/value_loss', value_loss / batch_size)
                tf.summary.scalar('model/entropy', entropy / batch_size)
                tf.summary.image('model/state',
                                 tf.expand_dims(tf.transpose(self.local_network.input, [3, 1, 2, 0])[:, :, :, 0], 3),
                                 max_outputs=Config.STACKED_FRAMES)
                tf.summary.scalar('model/var_global_norm', tf.global_norm(self.local_network.parameters))
                tf.summary.scalar('model/grad_global_norm', tf.global_norm(gradients))
                tf.summary.scalar('model/learning_rate', self.learning_rate)
                self.summary_op = tf.summary.merge_all()

                if Config.CLIP_GRADIENTS:
                    gradients = tf.clip_by_global_norm(gradients, Config.CLIP_NORM)[0]

                # copy weights from the parameter server to the local model
                self.sync_local_network = tf.group(*[local_p.assign(global_p)
                                                     for local_p, global_p in zip(self.local_network.parameters,
                                                                                  self.global_network.parameters)])

                grads_and_vars = list(zip(gradients, self.global_network.parameters))
                inc_step = self.global_step.assign_add(tf.shape(self.local_network.input)[0])

                if Config.OPTIMIZER == 'RMSprop':
                    # no shared RMSProp i.e. average term g is not shared across workers
                    opt = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate,
                                                    decay=Config.RMSPROP_DECAY,
                                                    momentum=Config.RMSPROP_MOMENTUM,
                                                    epsilon=Config.OPT_EPSILON)
                elif Config.OPTIMIZER == 'Adam':
                    # each worker has a different set of adam optimizer parameters
                    opt = tf.train.AdamOptimizer(learning_rate=self.learning_rate,
                                                 beta1=Config.ADAM_BETA1,
                                                 beta2=Config.ADAM_BETA2,
                                                 epsilon=Config.OPT_EPSILON)
                else:
                    raise ValueError('No valid optimizer configured! Valid values are ["RMSprop", "Adam"]')

                self.train_op = tf.group(opt.apply_gradients(grads_and_vars), inc_step)

    def _get_experiences(self):
        states = []
        actions = []
        rewards = []
        values = []

        terminal = False
        t_local = 0
        new_state = self.env.get_state()  # avoid 'Local variable 'new_state' might be referenced before assignment'
        lstm_state = self.local_network.get_initial_lstm_state() if self.use_lstm else None

        while not terminal and t_local < Config.TIME_MAX:
            state = self.env.get_state()
            action, value, lstm_state = self.local_network.sample_action(state, lstm_state)
            new_state, reward, terminal = self.env.step(action)

            # Store this experience.
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            values.append(value)

            t_local += 1

        # Estimate discounted rewards.
        clipped_rewards = np.clip(rewards, Config.REWARD_MIN, Config.REWARD_MAX)
        next_value = 0 if terminal else self.local_network.estimate_value(new_state, lstm_state)
        discounted_rewards = self.apply_discount(np.append(clipped_rewards, next_value), Config.DISCOUNT)[:-1]

        # Estimate advantages.
        values = np.array(values + [next_value])
        # this formula for the advantage comes from "Generalized Advantage Estimation": https://arxiv.org/abs/1506.02438
        advantages = self.apply_discount(clipped_rewards + Config.DISCOUNT * values[1:] - values[:-1], Config.DISCOUNT)

        return np.array(states), np.array(actions), advantages, discounted_rewards, terminal

    def train(self, sess: tf.Session):
        """
        Performs a single learning step.

        Args:
            sess: A TensorFlow session.
        Returns:
            new global step
        """
        sess.run(self.sync_local_network)

        states, actions, advantages, discounted_rewards, terminal = self._get_experiences()

        feed_dict = {self.local_network.input: states,
                     self.action: actions,
                     self.advantage: advantages,
                     self.discounted_reward: discounted_rewards}
        if self.use_lstm:
            feed_dict[self.local_network.lstm_state] = self.local_network.get_initial_lstm_state()

        # Occasionally write summaries.
        if self.id_ == 0 and self.steps_since_last_summary >= Config.SAVE_SUMMARIES_FREQUENCY:
            if Config.TIMELINE:  # Runtime statistics
                run_metadata = tf.RunMetadata()
                global_step, summary = sess.run([self.train_op, self.global_step, self.summary_op], feed_dict,
                                                options=tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE),
                                                run_metadata=run_metadata)[1:]
                self.summary_writer.add_run_metadata(run_metadata, 'step{}'.format(global_step), global_step)
            else:
                global_step, summary = sess.run([self.train_op, self.global_step, self.summary_op], feed_dict)[1:]
            self.summary_writer.add_summary(summary, global_step)
            self.steps_since_last_summary = 0
        else:
            global_step = sess.run([self.train_op, self.global_step], feed_dict)[-1]
            self.steps_since_last_summary += 1

        if terminal:  # Episode ended
            if self.eps_since_last_summary >= Config.SAVE_EPISODE_SUMMARIES_FREQUENCY:
                ep_reward, ep_length, ep_run_time = self.env.get_statistics()
                LOGGER.info('Episode ended. Training step {:,} of {:,}. Total reward: {}.'.format(global_step,
                                                                                                  Config.STEPS_MAX,
                                                                                                  ep_reward))
                summary = tf.Summary()
                summary.value.add(tag='environment/episode_length', simple_value=ep_length)
                summary.value.add(tag='environment/episode_reward', simple_value=ep_reward)
                summary.value.add(tag='environment/fps', simple_value=ep_length / ep_run_time)

                self.summary_writer.add_summary(summary, self.global_step.eval())
                self.eps_since_last_summary = 0
            else:
                self.eps_since_last_summary += 1

            self.env.reset()

        return global_step

    def play(self):
        """
        Performs a single playing step.

        Returns:
            None
        """
        action = self.local_network.best_action(self.env.get_state())
        terminal = self.env.step(action)[-1]
        if terminal:
            ep_reward, ep_length, ep_run_time = self.env.get_statistics()
            LOGGER.info('Episode finished. Total reward: {}. Length: {}. FPS: {:.02f}'.format(ep_reward, ep_length,
                                                                                              ep_length / ep_run_time))
            self.env.reset()

    def test(self, episodes):
        """
        Evaluate the performance of the trained agent.

        Test result keys:
            - **episodes**: number of tested episodes
            - **best_episode**: episode in which the maximum reward was gained
            - **worst_episode**: episode in which the minimum reward was gained
            - **max_reward**: maximum reward gained in one episode
            - **min_reward**: minimum reward gained in one episode
            - **avg_reward**: average reward gained

        Returns:
            dict: Test result.
        """
        eps = 0
        rewards = []
        try:
            while eps < episodes:
                action = self.local_network.best_action(self.env.get_state())
                terminal = self.env.step(action)[-1]
                if terminal:
                    rewards.append(self.env.get_statistics()[0])
                    eps += 1
                    self.env.reset()
        except KeyboardInterrupt:
            if eps < 1:
                return 0, 0, 0, 0, 0

        rewards = np.array(rewards)
        best_episode = np.argmax(rewards)
        worst_episode = np.argmin(rewards)

        return {
            'episodes': eps,
            'rewards': rewards,
            'best_episode': best_episode,
            'worst_episode': worst_episode,
            'max_reward': rewards[best_episode],
            'min_reward': rewards[worst_episode],
            'avg_reward': np.average(rewards)
        }

    @staticmethod
    def apply_discount(rewards, discount):
        """Discounts the specified rewards exponentially.
        Given rewards = [r0, r1, r2, r3] and discount = 0.99, the result is:
            [r0 + 0.99 * (r1 + 0.99 * (r2 + 0.99 * r3)),
             r1 + 0.99 * (r2 + 0.99 * r3),
             r2 + 0.99 * r3,
             r3]
        Example: rewards = [10, 20, 30, 40] and discount = 0.99 -> [98.01496, 88.904, 69.6, 40].
        Returns:
            The discounted rewards.
        """
        return signal.lfilter([1], [1, -discount], rewards[::-1])[::-1]
