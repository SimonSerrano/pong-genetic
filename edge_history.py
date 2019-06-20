

class EdgeHistory:

    def __init__(self, from_, to, innovation, innovationNumbers):
        self.fromNode = from_
        self.toNode = to
        self.innovation = innovation
        self.innovationNumbers = innovationNumbers[:]

    def matches(self, genome, from_, to):
        if len(genome.genes) == len(self.innovationNumbers):
            if from_.number == self.fromNode and to.number == self.toNode:
                for gene in genome.genes:
                    if gene.innovation not in self.innovationNumbers:
                        return False
            
            return True
        
        return False
