import math

class Node:
    def __init__(self, number):
        self.number = number
        self.inputSum = 0
        self.outputValue = 0
        self.outputConnections = []
        self.layer = 0


    def engage(self):
        if self.layer != 0:
            self.outputValue = self.sigmoid(self.inputSum)

        for outputConnection in self.outputConnections:
            if(outputConnection.enabled):
                outputConnection.toNode.inputSum = outputConnection.weight * self.outputValue

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    
    def isConnectedTo(self, node):
        if node.layer == self.layer :
            return False
        
        if node.layer < self.layer :
            for outputConnection in self.outputConnections :
                if outputConnection.toNode == self:
                    return True
        else : 
            for outputConnection in self.outputConnections:
                if outputConnection.toNode == node :
                    return True

        return False

    def clone(self):
        clone = Node(self.number)
        clone.layer = self.layer
        return clone

    