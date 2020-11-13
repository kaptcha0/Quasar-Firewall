from neuralnet import NeuralNet

class Evolution:
    def __init__(self):
        self.nets: NeuralNet = [NeuralNet()]
    
    def fitness(self, network: NeuralNet):
        scores = network.get_scores()
        print(scores)
    
    def train(self):
        for n in self.nets:
            self.fitness(n)