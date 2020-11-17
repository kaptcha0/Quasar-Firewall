from math import atanh, tanh
from request import Request
from typing import List
from neat.population import Population
from neuralnet import NeuralNet
from neat import genome, config, nn
from dataset import load_dataset
from random import randint

import neat, os, multiprocessing


class Evolution:
    """
        Base class for overall evolution evolution
    """

    def __init__(self, point:neat.Checkpointer=None):
        """
            `point`: checkpoint to be restored from
        """

        self.p = point
        self.data = []
        if not (point == None):
            self.nn = self.__get_model__()
        else:
            self.nn = None

    def train(self, config_path: str):
        """
            Initializes training for every genome
        """
        self.data: List[Request] = load_dataset()
        if not self.p:
            self.p = self.__initialize__(config_path)

        pe = neat.ThreadedEvaluator(multiprocessing.cpu_count(), self.__eval_genome__)
        return self.p.run(pe.evaluate, 200)

    def predict(self, input: Request):
        """
            Gets prediction of Neural Network
            - input: `Request`
            Raises exception if `self.nn` is `None`
        """

        data = self.__extract_data__(input)[:3]

        if not (self.nn == None):
            return self.nn.activate(data)
        else:
            raise Exception("Neural Network not provided")
    
    @staticmethod
    def load(checkpoint: str):
        """
            Loads checkpoint with the prefix of `neat-chekpoint-`
            - checkpoint: desired checkpoint id
        """
        point = neat.Checkpointer.restore_checkpoint(
            f'neat-checkpoint-{str(checkpoint)}')

        return Evolution(point)

    def __eval_genome__(self, genome: genome, config: config):
        """
            Evaluates gurrent genome
            For `multiprocessing` or `parallelprocessing`
        """

        data = self.data

        net = nn.FeedForwardNetwork.create(genome, config)
        firewall = NeuralNet(net)
        error = 0.0

        for d in data:
            extracted = self.__extract_data__(d)

            score: float = firewall.predict(extracted[:3], extracted[3])
            if score < 0.5:
                error -= tanh(score)
            else:
                error += tanh(score)

        return error

    def __initialize__(self, config_path: str) -> Population:
        """
            Initializes population
        """

        config = self.__get_config__(config_path)
        p: Population = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())
        p.add_reporter(neat.Checkpointer(generation_interval=5, time_interval_seconds=10000))

        return p

    def __get_config__(self, config_path: str):
        """
            Generates and returns `neat.Config`
        """

        return neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                           neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    def __get_model__(self):
        """
            Load the model from `config.txt`
        """
        
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), self.__eval_genome__)
        winner = self.p.run(pe.evaluate, 1)
        return neat.nn.FeedForwardNetwork.create(winner, self.__get_config__(config_path))

    def __extract_data__(self, data: Request) -> List[float]:
        """
            Extract data from request
        """

        headers = data.headers
        is_hack = data.is_hack
        method = data.method

        method_num = self.__get_method__(method.lower())
        protocol = data.protocol

        protocol_num = float(protocol[5:])
        return [method_num, headers.content_length, protocol_num, is_hack]

    def __get_method__(self, m: str):
        """
            Gets HTTP method number
        """

        methods = ["get", "head", "post", "put",
                   "delete", "connect", "options", "trace"]

        return methods.index(m.lower())







