from _typeshed import OpenTextMode
from math import atanh
import os
from typing import List
from neat.population import Population
from neuralnet import NeuralNet
from neat import genome, config, nn
import neat, dataset


class Evolution:
    def __init__(self, point=None):
        self.p = point
        if not (point == None):
            self.nn = self.__get_model__()
        else:
            self.nn = None

    def fitness(self, genomes: genome, config: config):
        nets = []
        ge = []
        firewall: List[NeuralNet] = []
        data = dataset.load_dataset()


        for id, genome in genomes:
            genome.fitness = 0
            net = nn.FeedForwardNetwork.create(genome, config)
            ge.append(genome)
            nets.append(net)
            firewall.append(NeuralNet(net))

        for x, net in enumerate(firewall):
            score: float = net.predict(16, False)
            if score < 0.5:
                ge[x].fitness -= atanh(score)
                firewall.pop(x)
                nets.pop(x)
                ge.pop(x)
            else:
                ge[x].fitness += atanh(score)

    def train(self, config_path: str):
        if not self.p:
            self.p = self.__initialize__(config_path)

        self.p.run(self.fitness, 100)

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

    @staticmethod
    def load(checkpoint):
        point = neat.Checkpointer.restore_checkpoint(
            f'neat-checkpoint-{checkpoint}')

        return Evolution(point)

    def __get_model__(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        winner = self.p.run(self.fitness, 1)
        return neat.nn.FeedForwardNetwork.create(winner, self.__get_config__(config_path))

    def predict(self, input: List[float]):
        if input is not List:
            input = [input]

        if not (self.nn == None):
            return self.nn.activate(input)
        else:
            raise Exception("Neural Network not provided")
