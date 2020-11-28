import multiprocessing
import os
from math import atanh
from random import shuffle
from typing import List

import neat
from neat import config, genome, nn
from neat.population import Population

import visualize
from dataset import load_dataset
from neuralnet import NeuralNet
from request import Request


class Evolution:
    """
        Base class for overall evolution
    """

    def __init__(self, point: Population = None, generations=500):
        """
            `point`: checkpoint to be restored from
        """

        self.p = point
        self.data = []
        self.generations = generations
        if not (point == None):
            self.nn = self.__get_model__()
        else:
            self.nn = None

    def train(self, config_path: str):
        """
            Initializes training for every genome
        """
        self.data: List[Request] = load_dataset()
        shuffle(self.data)
        if not self.p:
            self.p = self.__initialize__(config_path)

        return self.p.run(self.__eval_genome__, self.generations)

    def predict(self, input: Request):
        """
            Gets prediction of Neural Network
            - input: `Request`
            Raises exception if `self.nn` is `None`
        """

        data = self.__extract_data__(input)[:5]

        if self.nn != None:
            return self.nn.activate(data)
        else:
            raise RuntimeError("Neural Network not provided")

    @staticmethod
    def load(checkpoint: str, session: str = '.'):
        """
            Loads checkpoint with the prefix of `neat-chekpoint-`
            - checkpoint: desired checkpoint id
            - session: session directory (defaults to current directory)
        """
        point: Population = neat.Checkpointer.restore_checkpoint(
            f'{str(session)}/neat-checkpoint-{str(checkpoint)}')

        return Evolution(point)

    def __eval_genome__(self, genomes, config: config):
        """
            Evaluates gurrent genome
            For `multiprocessing` or `parallelprocessing`
        """

        nets = []
        ge = []
        firewall: List[NeuralNet] = []
        data = self.data
        shuffle(data)

        for genome_id, genome in genomes:
            genome: genome = genome
            genome.fitness = 0
            net = nn.FeedForwardNetwork.create(genome, config)
            ge.append(genome)
            nets.append(net)
            firewall.append(NeuralNet(net))

        for x, net in enumerate(firewall):
            extracted = self.__extract_data__(data[x])

            score: float = net.predict(extracted[:5], extracted[5])

            if score < 0.8:
                ge[x].fitness -= atanh(score)
                firewall.pop(x)
                nets.pop(x)
                ge.pop(x)
            else:
                ge[x].fitness += atanh(score)

    def __initialize__(self, config_path: str):
        """
            Initializes population
        """

        config = self.__get_config__(config_path)
        p: Population = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.StatisticsReporter())
        p.add_reporter(neat.Checkpointer(
            generation_interval=5, time_interval_seconds=10000))

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
        
        self.data: List[Request] = load_dataset()
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")

        winner = self.p.run(self.__eval_genome__, 1)
        node_names = {-1: "method", -2: "headers", -3: "protocol", -
                      4: "body", -5: "query", 0: "Is not a hack", 1: "Is a hack"}
        visualize.draw_net(config_path, winner, True, node_names=node_names)

        return neat.nn.FeedForwardNetwork.create(winner, self.__get_config__(config_path))

    def __extract_data__(self, data: Request):
        """
            Extract data from request
        """

        def get_method(m: str):
            """
                Gets HTTP method number
            """

            methods = ["get", "head", "post", "put",
                       "delete", "connect", "options", "trace"]

            return methods.index(m.lower())

        headers = data.headers
        is_hack = data.is_hack
        method = data.method
        body = data.body
        query = data.query

        method_num = get_method(method.lower())
        protocol = data.protocol

        protocol_num = float(protocol[5:])

        return [method_num, headers.content_length, protocol_num, body, query, is_hack]


class EvolutionMultiProcessing(Evolution):
    """
        Base class for overall evolution with multiprocessing
    """

    def __init__(self, point: Population = None, generations=500):
        """
            `point`: checkpoint to be restored from
        """

        super().__init__(point, generations)

    def train(self, config_path: str):
        """
            Initializes training for every genome
        """
        self.data: List[Request] = load_dataset()
        shuffle(self.data)
        if not self.p:
            self.p = self.__initialize__(config_path)

        pe = neat.ThreadedEvaluator(
            multiprocessing.cpu_count() - 1, self.__eval_genome__)
        return self.p.run(pe.evaluate, self.generations)

    @staticmethod
    def load(checkpoint: str, session: str = '.'):
        """
            Loads checkpoint with the prefix of `neat-chekpoint-`
            - checkpoint: desired checkpoint id
            - session: session directory (defaults to current directory)
        """
        point: Population = neat.Checkpointer.restore_checkpoint(
            f'{str(session)}/neat-checkpoint-{str(checkpoint)}')

        return EvolutionMultiProcessing(point)

    def __eval_genome__(self, genome: genome, config: config):
        """
            Evaluates gurrent genome
            For `multiprocessing` or `parallelprocessing`
        """

        data = self.data
        shuffle(data)

        net = nn.FeedForwardNetwork.create(genome, config)
        firewall = NeuralNet(net)
        error = 0.0

        for d in data:
            extracted = self.__extract_data__(d)

            score: float = firewall.predict(extracted[:4], extracted[4])

            if score < 0.5:
                error -= score
            else:
                error += score

        return error

    def __get_model__(self):
        """
            Load the model from `config.txt`
        """

        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        pe = neat.ParallelEvaluator(
            multiprocessing.cpu_count(), self.__eval_genome__)
        winner = self.p.run(pe.evaluate, 1)
        return neat.nn.FeedForwardNetwork.create(winner, self.__get_config__(config_path))
