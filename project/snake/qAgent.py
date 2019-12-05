from threading import Thread
from game import Game
from snakeMultiAgentDeepQNetwork import SnakeMultiAgentDeepQNetwork

# First convolution layer.
from pydbm.cnn.layerablecnn.convolution_layer import ConvolutionLayer as ConvolutionLayer1
# Second convolution layer.
from pydbm.cnn.layerablecnn.convolution_layer import ConvolutionLayer as ConvolutionLayer2
# Computation graph in output layer.
from pydbm.synapse.cnn_output_graph import CNNOutputGraph
# Computation graph for first convolution layer.
from pydbm.synapse.cnn_graph import CNNGraph as ConvGraph1
# Computation graph for second convolution layer.
from pydbm.synapse.cnn_graph import CNNGraph as ConvGraph2
# Logistic Function as activation function.
from pydbm.activation.logistic_function import LogisticFunction
# Tanh Function as activation function.
from pydbm.activation.tanh_function import TanhFunction
# ReLu Function as activation function.
from pydbm.activation.relu_function import ReLuFunction
# CNN as a Function Approximator.
from pyqlearning.functionapproximator.cnn_fa import CNNFA

batch_size = 4

# First convolution layer.
conv1 = ConvolutionLayer1(
    # Computation graph for first convolution layer.
    ConvGraph1(
        # Logistic function as activation function.
        activation_function=TanhFunction(),
        # The number of `filter`.
        filter_num=batch_size,
        # The number of channel.
        channel=3,
        # The size of kernel.
        kernel_size=6,
        # The filter scale.
        scale=0.001,
        # The nubmer of stride.
        stride=2,
        # The number of zero-padding.
        pad=2
    )
)
# Second convolution layer.
conv2 = ConvolutionLayer2(
    # Computation graph for second convolution layer.
    ConvGraph2(
        # Logistic function as activation function.
        activation_function=TanhFunction(),
        # The number of `filter`.
        filter_num=batch_size,
        # The number of channel.
        channel=batch_size,
        # The size of kernel.
        kernel_size=3,
        # The filter scale.
        scale=0.001,
        # The nubmer of stride.
        stride=1,
        # The number of zero-padding.
        pad=1
    )
)

# Stack.
layerable_cnn_list=[conv1, conv2]

cnn_output_graph = CNNOutputGraph(TanhFunction(), hidden_dim=400, output_dim=1, scale=0.1)

# CNN as a function approximator.
function_approximator = CNNFA(
    # Batch size.
    batch_size=batch_size,
    # Stacked CNNs.
    layerable_cnn_list=layerable_cnn_list,
    # Computation graph in output layer.
    cnn_output_graph=cnn_output_graph,
    # Learning rate.
    learning_rate=1e-05,
    # is-a `pydbm.loss.interface.computable_loss.ComputableLoss`.
    computable_loss=None,
    # is-a `pydbm.optimization.opt_params.OptParams`.
    opt_params=None,
    # is-a `pydbm.verification.interface.verificatable_result.VerificatableResult`.
    verificatable_result=None,
    # Verbose mode or not.
    verbose_mode=True
)

game = Game()

deep_q_learning = SnakeMultiAgentDeepQNetwork(function_approximator, 4, game, 20)
# Epsilon greedy rate.
deep_q_learning.epsilon_greedy_rate = 0.7
# Learning rate.
deep_q_learning.alpha_value = 1e-05
# Discounting rate.
deep_q_learning.gamma_value = 0.01

for _ in range(10):
    print("LEARNING")
    try:
        game_thread = Thread(target=game.start)
        print("START")
        game_thread.start()

        # Execute learning.
        deep_q_learning.learn(
            # Initial state.
            state_arr=deep_q_learning.extract_now_state(),
            # The number of searching.
            limit=5000
        )

        game_thread.join()

        # Reset time step.
        deep_q_learning.t = 1
    except KeyboardInterrupt:
        print("Interrupt.")
