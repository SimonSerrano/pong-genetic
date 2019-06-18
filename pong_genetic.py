import gym
from brain import NeuralNetwork
from darwin import GeneticRuler


def generate(population):
    ruler = GeneticRuler()
    pop = ruler.create_population(population)
    for fellow in pop:
        env = gym.make("Pong-v0")
        



def main():
    
    POPULATION = 20
    generate(POPULATION)





if __name__ == "__main__":
    main()