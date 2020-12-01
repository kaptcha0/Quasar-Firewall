import time
from math import tanh
from typing import List

from neat.nn.feed_forward import FeedForwardNetwork


class NeuralNet:
    """
        Neural Network class. Makes predictions easier
    """

    def __init__(self, network: FeedForwardNetwork):
        self.net = network

    def predict(self, data: List[float], hack: bool):
        """
            Predict and calculate fitness of neural net.
            Returns fitness
        """

        start_time: float = time.perf_counter()
        result = self.net.activate(data)[0]
        finish_time = time.perf_counter()

        elapsed = finish_time - start_time
        fitness = self.__calc_fitness__(hack, elapsed, result)
        return fitness

    def get_network(self):
        """
            Returns the actual neural network of type `neat.nn.feed_forward.FeedForwardNetwork`
        """
        return self.net

    def __calc_fitness__(self, is_hack: bool, compute_time: float, result: float):
        prediction = result > 0
        score = float(prediction == is_hack) + tanh(compute_time)
        return score

