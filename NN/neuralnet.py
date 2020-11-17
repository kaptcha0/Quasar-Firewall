from math import tanh
from os.path import relpath
from typing import List
from neat.nn.feed_forward import FeedForwardNetwork
import time


class NeuralNet:
    """
        Neural Network class. Makes predictions easier
    """

    def __init__(self, network: FeedForwardNetwork):
        self.net = network

    def predict(self, data: List[float], hack: bool):
        start_time: float = time.time()
        result = self.net.activate(data)
        finish_time = time.time()
        elapsed = finish_time - start_time
        fitness = self.__calc_fitness__(hack, elapsed, result)
        return fitness

    def get_network(self):
        return self.net

    def __calc_fitness__(self, is_hack: bool, compute_time: float, result: List[float]):
        prediction = True if result[1] < result[0] else False
        score = (-1 if (not is_hack and not (prediction == is_hack)) else 1) + \
            tanh(compute_time)
        return tanh(score)


