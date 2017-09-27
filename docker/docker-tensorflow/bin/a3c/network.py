import numpy as np
import tensorflow as tf


class A3CNetwork(object):
    def __init__(self, input_shape: list, output_dim: int, use_lstm: bool = False):
        """
        Network structure is defined here.

        Args:
            input_shape (list): The shape of input image [H, W, C]
            output_dim (int): Number of actions
            use_lstm (bool): Use LSTM network architecture (4x CONV -> FC -> LSTM instead of 2x CONV -> FC)
        """
        self.use_lstm = use_lstm
        self.input = tf.placeholder(tf.float32, shape=[None, *input_shape], name='input_states')

        # shared network
        if use_lstm:
            # OpenAi Universe starter agent architecture
            net = self.input
            for i in range(4):
                net = tf.layers.conv2d(net, filters=32, kernel_size=(3, 3), strides=(2, 2), activation=tf.nn.elu,
                                       name='conv{}'.format(i + 1))

            # Flatten the output to feed it into the LSTM layer.
            net_flat = tf.contrib.layers.flatten(net)

            with tf.name_scope('lstm_layer'):
                self.lstm_state = (tf.placeholder(tf.float32, [1, 256]),
                                   tf.placeholder(tf.float32, [1, 256]))

                self.initial_lstm_state = (np.zeros([1, 256], np.float32),
                                           np.zeros([1, 256], np.float32))

                lstm_state = tf.nn.rnn_cell.LSTMStateTuple(*self.lstm_state)
                lstm = tf.nn.rnn_cell.BasicLSTMCell(256)

                # tf.nn.dynamic_rnn expects inputs of shape [batch_size, time, features], but the shape
                # of h_flat is [batch_size, features]. We want the batch_size dimension to be treated as
                # the time dimension, so the input is redundantly expanded to [1, batch_size, features].
                # The LSTM layer will assume it has 1 batch with a time dimension of length batch_size.
                batch_size = tf.shape(net_flat)[:1]  # [:1] is a trick to correctly get the dynamic shape.
                lstm_input = tf.expand_dims(net_flat, [0])
                lstm_output, self.new_lstm_state = tf.nn.dynamic_rnn(lstm, lstm_input, sequence_length=batch_size,
                                                                     initial_state=lstm_state, time_major=False)

                # Delete the fake batch dimension.
                shared_out = tf.squeeze(lstm_output, [0])

        else:
            # Mnih, et al. "Asynchronous Methods for Deep Reinforcement Learning" architecture
            conv1 = tf.layers.conv2d(self.input, filters=16, kernel_size=(8, 8), strides=(4, 4),
                                     activation=tf.nn.relu,
                                     name='conv1')

            conv2 = tf.layers.conv2d(conv1, filters=32, kernel_size=(4, 4), strides=(2, 2),
                                     activation=tf.nn.relu,
                                     name='conv2')

            conv2_flat = tf.contrib.layers.flatten(conv2)
            shared_out = tf.layers.dense(conv2_flat, 256, activation=tf.nn.relu, name='fc')

        # actor part (Policy)
        self.action_logits = tf.layers.dense(shared_out, output_dim, name='action_logits')
        self.action = tf.squeeze(
            tf.multinomial(self.action_logits - tf.reduce_max(self.action_logits, 1, keep_dims=True), 1))
        self.max_action = tf.squeeze(tf.argmax(self.action_logits, 1))

        # critic part (Value)
        self.value = tf.squeeze(tf.layers.dense(shared_out, 1, name='v'))

        self.parameters = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, tf.get_variable_scope().name)

    def get_initial_lstm_state(self):
        """Returns a value that can be used as the inital state of the LSTM unit of the network."""
        return self.initial_lstm_state

    def sample_action(self, state, lstm_state=None):
        """
        Samples an action for the specified state from the learned strategy.

        Args:
            state: State of the environment.
            lstm_state: The state of the long short-term memory unit of the network. Use the
                get_initial_lstm_state method when unknown. Pass None if LSTM network isn't used.

        Returns:
            An action, the value of the specified state and the new state of the LSTM unit.
        """
        sess = tf.get_default_session()
        if lstm_state:
            return sess.run([self.action, self.value, self.new_lstm_state],
                            {self.input: [state], self.lstm_state: lstm_state})
        else:
            return sess.run([self.action, self.value], {self.input: [state]}) + [None]

    def best_action(self, state):
        """
        Gets best action for the specified state from the learned strategy.

        Args:
            state: State of the environment.

        Returns:
            An action.
        """
        sess = tf.get_default_session()
        if self.use_lstm:
            return sess.run(self.max_action, {self.input: [state], self.lstm_state: self.get_initial_lstm_state()})
        else:
            return sess.run(self.max_action, {self.input: [state]})

    def estimate_value(self, state, lstm_state=None):
        """
        Estimates the value of the specified state.

        Args:
            state: State of the environment.
            lstm_state: The state of the long short-term memory unit of the network.
                Pass None if LSTM network isn't used.

        Returns:
            The value of the specified state.
        """
        sess = tf.get_default_session()
        if lstm_state:
            return sess.run(self.value, {self.input: [state], self.lstm_state: lstm_state})
        else:
            return sess.run(self.value, {self.input: [state]})
