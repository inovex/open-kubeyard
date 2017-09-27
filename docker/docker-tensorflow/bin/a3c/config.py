import multiprocessing as mp


class Config:
    #########################################################################
    # Game configuration

    # Name of the game, with version (e.g. Breakout-v0)
    GAME = 'Pong-v0'

    # Show game while training (slows training)
    RENDER = False

    #########################################################################
    # Number of agents and other system settings

    # Number of Agents (Workers in distributed setting)
    AGENTS = mp.cpu_count()

    # Number of parameter servers
    MASTERS = 1

    # Start port. First #MASTERS ports reserved for parameter servers. Followed by #AGENTS ports for workers.
    START_PORT = 12222

    # Set to True to see the trained agent playing the game (ignores RENDER parameter). Set to False for training.
    PLAY_MODE = False

    #########################################################################
    # Algorithm parameters

    # Discount factor
    DISCOUNT = 0.99

    # Tmax
    TIME_MAX = 20

    # Reward Clipping
    REWARD_MIN = -1
    REWARD_MAX = 1

    # Input of the DNN
    STACKED_FRAMES = 4
    IMAGE_WIDTH = 84  # 84 for GPU
    IMAGE_HEIGHT = 84

    # Crop simulator frame before feeding to DNN
    CROP_TOP = 32  # 34/16 fits for Pong and Breakout
    CROP_BOTTOM = 16

    # Total number of training steps and annealing frequency (no effect if START and END learning rate are the same)
    STEPS_MAX = 8e7
    ANNEALING_STEPS = 8e7

    # Entropy regularization hyper-parameter
    BETA = 0.01

    # Learning rate. If START and END are different, learning rate is linearly reduced over ANNEALING_STEPS steps.
    LEARNING_RATE_START = 0.0001
    LEARNING_RATE_END = 0.0001

    # Which optimizer should be used: 'RMSprop' or 'Adam'
    OPTIMIZER = 'RMSprop'

    # RMSprop parameters
    RMSPROP_DECAY = 0.99
    RMSPROP_MOMENTUM = 0.0

    # Adam parameters
    ADAM_BETA1 = 0.9
    ADAM_BETA2 = 0.999

    # It is to prevent 'Division from zero' error (Optimizer hyper-parameter)
    OPT_EPSILON = 1e-3  # other typical values are 1, 0.1 (for Adam 1e-3, RMSprop 0.1)

    # Clip gradients
    CLIP_GRADIENTS = False
    CLIP_NORM = 40.0

    # Use LSTM network architecture
    USE_LSTM = False

    #########################################################################
    # Log and save

    # Number of local training steps between computation of summaries for the event log.
    SAVE_SUMMARIES_FREQUENCY = 1000

    # Number of episodes between computation of episode summaries for the event log (length-, reward of episode, fps).
    # Summaries are saved per worker. Effects console logging output.
    SAVE_EPISODE_SUMMARIES_FREQUENCY = 10

    # Number of seconds between the creation of model checkpoints. Pass 0 to disable checkpoints.
    SAVE_MODEL_SECS = 60

    # Number of most recent checkpoints to keep
    MAX_TO_KEEP = 3

    # Keep also a checkpoint every n hour during training
    KEEP_CHECKPOINT_EVERY_N_HOUR = 1

    # Directory for saving logs (TensorFlow event files)
    LOG_DIR = 'hdfs://listless-panther-hdfs-namenode:9000/tmp/logs/{game}/{step_max}/{network}_{optimizer}_{epsilon}_{clipping}/' \
              '{img_w}x{img_h}_{c_t}_{c_b}_{frames}/{agents}/{lr_start}-{lr_end}/{t_max}' \
        .format(game=GAME,
                step_max=int(
                    STEPS_MAX),
                network='lstm' if USE_LSTM else 'ff',
                optimizer=OPTIMIZER,
                epsilon=OPT_EPSILON,
                clipping=CLIP_NORM if CLIP_GRADIENTS else 'no_clipping',
                img_w=IMAGE_WIDTH,
                img_h=IMAGE_HEIGHT,
                c_t=CROP_TOP,
                c_b=CROP_BOTTOM,
                frames=STACKED_FRAMES,
                agents=AGENTS,
                lr_start=LEARNING_RATE_START,
                lr_end=LEARNING_RATE_END,
                t_max=TIME_MAX)

    # Directory for saving checkpoints. Needed to resume training and later play (including weights).
    CHECKPOINT_DIR = '{}/checkpoint'.format(LOG_DIR)

    # Use the timeline module from tf.python.client to get execution time for each node in the graph.
    TIMELINE = False

    # Enable to find out which devices the operations and tensors are assigned to.
    LOG_DEVICE_PLACEMENT = False

    # Enable to write MetaGraph every time model is saved.
    WRITE_META_GRAPH = False
