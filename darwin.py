from node import Node
import random
from edge import Edge
from edge_history import EdgeHistory
import math

class Genome :

    def __init(self, inputs, outputs, crossover):
        self.genes = []
        self.nodes = []
        self.inputs = inputs
        self.outputs = outputs
        self.layers = 2
        self.nextNode = 0
        self.network = []

        if(crossover):
            return

        for i in range(self.inputs):
            self.nodes.append(Node(i))
            self.nextNode+=1
            self.nodes[i].layer = 0


        for i in range(self.outputs):
            self.nodes.append(Node(i+self.inputs))
            self.nodes[i+self.inputs].layer = 1
            self.nextNode +=1

        self.nodes.append(Node(self.nextNode))
        self.biasNode = self.nextNode
        self.nextNode+=1
        self.nodes[self.biasNode].layer = 0

    
    def connectNodes(self):
        for node in self.nodes:
            node.outputConnections = []

        for gene in self.genes:
            gene.fromNode.outputConnections.append(gene)

    def addNode(self, edgeHistory):
        if len(self.genes) == 0 :
            self.addEdge(edgeHistory)
            return
        
        randomEdge = random.choice(self.genes)

        while  self.genes != 1 and randomEdge.fromNode == self.nodes[self.biasNode] :
            randomEdge = random.choice(self.genes)

        randomEdge.enabled = False

        newNodeNum = self.nextNode
        self.nodes.append(Node(newNodeNum))
        self.nextNode+=1

        connectionInnovationNumber = self.getInnovationNumber(edgeHistory, randomEdge.fromNode, self.getNode(newNodeNum))
        self.genes.append(Edge(randomEdge.fromNode, self.getNode(newNodeNum), 1, connectionInnovationNumber))


        connectionInnovationNumber = self.getInnovationNumber(edgeHistory, self.getNode(newNodeNum), randomEdge.toNode)
        self.genes.append(Edge(self.getNode(newNodeNum), randomEdge.toNode, randomEdge.weight, connectionInnovationNumber))
        self.getNode(newNodeNum).layer = randomEdge.fromNode.layer + 1

        connectionInnovationNumber = self.getInnovationNumber(edgeHistory, self.nodes[self.biasNode], self.getNode(newNodeNum))
        self.genes.append(Edge(self.nodes[self.biasNode], self.getNode(newNodeNum), 0, connectionInnovationNumber))

        if self.getNode(newNodeNum).layer == randomEdge.toNode.layer :
            for i in range(len(self.nodes) - 1):
                if self.nodes[i].layer >= self.getNode(newNodeNum).layer :
                    self.nodes[i].layer += 1
        
            self.layers+=1
        
        self.connectNodes()

    def addEdge(self, edgeHistory):
        if self.isFullyConnected():
            print("the neural network is fully connected")
            return
        
        firstRandomNode = random.choice(self.nodes)
        secondRandomNode = random.choice(self.nodes)

        while self.badEdge(firstRandomNode, secondRandomNode):
            firstRandomNode = random.choice(self.nodes)
            secondRandomNode = random.choice(self.nodes)

        if firstRandomNode.layer > secondRandomNode.layer :
            temp = secondRandomNode
            secondRandomNode = firstRandomNode
            firstRandomNode = secondRandomNode
        
        connectionInnovationNumber = self.getInnovationNumber(edgeHistory, firstRandomNode, secondRandomNode)
        self.genes.append(Edge(firstRandomNode, secondRandomNode, random.uniform(-1, 1), connectionInnovationNumber))
        self.connectNodes()

    def badEdge(self, firstNode, secondNode):
        if firstNode.layer == secondNode.layer : return True
        if firstNode.isConnectedTo(secondNode) : return True
        return False

    def getNode(self, number):
        for node in self.nodes:
            if node.number == number:
                return node
        return None

    
    def generateNetwork(self):
        self.connectNodes()
        self.network = []

        for i in range(self.layers):
            for node in self.nodes:
                if node.layer == i:
                    self.network.append(node)

    def feedForward(self, inputValues):
        for i in range(self.inputs):
            self.nodes[i].outputValue = inputValues[i]

        self.nodes[self.biasNode].outputValue = 1

        for node in self.network:
            node.engage()

        outputs = []
        for i in range(self.outputs):
            outputs[i] = self.nodes[self.inputs+i].outputValue

        return outputs

    def crossover(self, parent2):
        child = Genome(self.inputs, self.outputs, True)
        child.genes = []
        child.nodes = []
        child.layers = self.layers
        child.nextNode = self.nextNode
        child.biasNode = self.biasNode
        childGenes = []
        isEnabled = []

        for gene in self.genes :
            setEnabled = True

            parent2gene = self.matchingGene(parent2, gene.innovation)
            if(parent2gene != -1):
                if not gene.enabled or not parent2.genes[parent2gene].enabled :
                    if random.Random() < 0.75:
                        setEnabled = False
                    rand = random.Random()
                    if rand < 0.5 :
                        childGenes.append(gene)
                    else :
                        childGenes.append(parent2.genes[parent2gene])
                else :
                    childGenes.append(gene)
                    setEnabled = gene.enabled
            isEnabled.append(setEnabled)
        
        for i in range(len(childGenes)):
            child.genes.append(childGenes[i].clone(child.getNode(childGenes[i].fromNode.number), child.getNode(childGenes[i].toNode.number)))
            child.genes[i].enabled = isEnabled[i]

        child.connectNodes()
        return child

    def matchingGene(self, parent2, innovation):
        for i in range(len(parent2.gene)):
            if parent2.genes[i].innovation == innovation:
                return i
        return -1

    def mutate(self, edgeHistory):
        if len(self.genes) == 0 :
            self.addEdge(edgeHistory)

        rand = random.random()
        if(rand < 0.8):
            for gene in self.genes:
                gene.mutateWeight()
        
        rand = random.random()
        if rand < 0.05 :
            self.addEdge(edgeHistory)

        rand = random.random()
        if rand < 0.01 :
            self.addNode(edgeHistory)

    def fullyConnect(self, edgeHistory):
        for i in range(self.inputs):
            for j in range(self.outputs):
                connectionInnovationNumber = self.getInnovationNumber(edgeHistory, self.nodes[i], self.nodes[len(self.nodes - j -2)])
                self.genes.append(Edge(self.nodes[i], self.nodes[len(self.nodes)-j-2], random.uniform(-1, 1), connectionInnovationNumber))

        connectionInnovationNumber = self.getInnovationNumber(edgeHistory, self.nodes[self.biasNode], self.nodes[len(self.nodes)-2])
        self.genes.append(Edge(self.nodes[self.biasNode], self.nodes[len(self.nodes)-j-2], random.uniform(-1, 1), connectionInnovationNumber))

        self.connectNodes()

    def getInnovationNumber(self, edgeHistory, from_, to):
        pass
        # TODO implement method
        isNew = True
        for history in edgeHistory:
            if history.matches(self, from_, to):
                isNew = False
                connectionInnovationNumber = history.innovation
                break
        
        if isNew :
            innoNumbers = []
            for gene in self.genes :
                innoNumbers.append(gene.innovation)

            edgeHistory.append(EdgeHistory(from_.number, to.number, connectionInnovationNumber, innoNumbers))

        return connectionInnovationNumber        

    def isFullyConnected(self):
        maxConnections = 0
        nodesInLayers = []
        for i in range(self.layers):
            nodesInLayers[i] = 0

        for i in range(self.layers - 1):
            nodesInFront = 0
            for j in range(self.layers):
                nodesInFront += nodesInLayers[j]
            
            maxConnections += nodesInLayers[i]*nodesInFront

        
        if maxConnections <= len(self.genes):
            return True
        
        return False


    def clone(self):
        clone = Genome(self.inputs, self.outputs, True)

        for node in self.nodes:
            clone.nodes.append(node.clone())
        
        for gene in self.genes:
            clone.genes.append(gene.clone(clone.getNode(gene.fromNode.number), clone.getNode(gene.toNode.number)))

        clone.layers = self.layers
        clone.nextNode = self.nextNode
        clone.biasNode = self.biasNode
        clone.connectNodes()

        return clone


   