import random
from brain import NeuralNetwork
from functools import reduce
from operator import add
from keras.utils.vis_utils import plot_model

class GeneticRuler():

    def __init__(self, random_select=0.1, 
        mutate_chance=0.2):

        self.random_select = random_select
        self.mutate_chance = mutate_chance



    def create_population(self, size):
        pop = []
        for i in range(0, size):
            model = NeuralNetwork()
            model.create_baby()
            pop.append(model)
            plot_model(model.model, to_file='model_graphs/model_plot_'+str(i+1)+'.png', show_shapes=True, show_layer_names=True)

        
        return pop




   