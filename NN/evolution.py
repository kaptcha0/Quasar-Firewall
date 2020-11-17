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
    def __init__(self, point=None):
        self.p = point
        self.data = []
        if not (point == None):
            self.nn = self.__get_model__()
        else:
            self.nn = None

    def fitness(self, genome: genome, config: config):
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

    def train(self, config_path: str):
        self.data: List[Request] = load_dataset()
        if not self.p:
            self.p = self.__initialize__(config_path)

        pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), self.fitness)
        self.p.run(pe.evaluate, 100)

    def predict(self, input: Request):
        data = self.__extract_data__(input)[:3]

        if not (self.nn == None):
            return self.nn.activate(data)
        else:
            raise Exception("Neural Network not provided")

    @staticmethod
    def load(checkpoint):
        point = neat.Checkpointer.restore_checkpoint(
            f'neat-checkpoint-{checkpoint}')

        return Evolution(point)

    def __initialize__(self, config_path: str) -> Population:
        config = self.__get_config__(config_path)
        p: Population = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())
        p.add_reporter(neat.Checkpointer())

        return p

    def __get_config__(self, config_path: str):
        return neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                           neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    def __get_model__(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), self.fitness)
        winner = self.p.run(pe.evaluate, 1)
        return neat.nn.FeedForwardNetwork.create(winner, self.__get_config__(config_path))

    def __extract_data__(self, data: Request) -> List[float]:
        headers = data.headers
        is_hack = data.is_hack
        method = data.method

        method_num = self.__get_method__(method.lower())
        protocol = data.protocol

        protocol_num = float(protocol[5:])
        return [method_num, headers.content_length, protocol_num, is_hack]

    def __get_method__(self, m: str):
        methods = ["get", "head", "post", "put",
                   "delete", "connect", "options", "trace"]

        return methods.index(m.lower())


