import random
import numpy as np

class Edge:
    def __init__(self, from_, to, weight, innovation):
        self.fromNode = from_
        self.toNode = to
        self.weight = weight
        self.enabled = True
        self.innovation = innovation

    

    def mutateWeight(self):
        rand = random.Random()
        if rand < 0.1 :
            self.weight = random.uniform(-1, 1)
        else :
            self.weight += np.random.normal()/50

            if self.weight > 1 :
                self.weight = 1

            if self.weight < -1 :
                self.weight = -1
    
    def clone(self):
        clone = Edge(self.fromNode, self.toNode, self.weight, self.innovation)
        clone.enabled = self.enabled

        return clone