import numpy as np
import matplotlib.pyplot as plt
import random

###Plot hoeveelheid vervallen deeltjes niet de hoeveelheid deeltjes op tijdstip x !!!!###

# First make a particle object that has a decay chance
# Second create multiple of those particles in a list
# Third loop over those particles as time iterations
# Fourth, make a counter of all the particles that are decayed each time iteration
# Fifth plot the values of the amount of decayed particles for each iteration

amount_of_particles = 10000
duration = 1000
decay_chance = 0.01

'''Creating the instance for each particle'''


class Particle:

    def __init__(self, decay_chance):
        self.decay_chance = decay_chance

    def is_decay(self):
        if self.decay_chance > random.random():
            return True


# Creating a list of x amount of particles
particle_list = []

for i in range(amount_of_particles):
    particle_list.append(Particle(decay_chance))

# Creating a list of decayed particles for a certain amount of iterations of time
decayed_list = []
time_counter = []
amount_counter = []

for time in range(duration):
    counter = 0
    amount_counter.append(len(particle_list))
    for particle in particle_list:
        if particle.is_decay() == True:
            particle_list.remove(particle)
            decayed_list.append(particle)
            counter += 1
    time_counter.append(counter)


# Plotting the graph


plt.plot(time_counter)
plt.title('Amount of decays for each iteration of time')
plt.xlabel('Time')
plt.ylabel('Decay amount')
plt.show()

plt.plot(amount_counter)
plt.title('Amount of not decayed nuclei for each iteration of time')
plt.xlabel('Time')
plt.ylabel('Nuclei amount')
plt.show()





