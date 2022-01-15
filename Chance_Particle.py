import numpy as np
import matplotlib.pyplot as plt
import random

'''Creating the instance for each particle'''
class Particle:

    def __init__(self, decay_chance):
        self.decay_chance = decay_chance

    def is_decay(self):
        if self.decay_chance > random.random():
          return True

# creating a list of x amount of particles
particle_list = []

for i in range(10):
    particle_list.append(Particle(0.2))










