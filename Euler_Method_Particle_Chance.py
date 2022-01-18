import matplotlib.pyplot as plt
import numpy as np

# Decay equations equals to N_t = N_0 * e ** -lambda * t
# to use these values

# Initiate the values for a certain substance
# Find the decay constant of the substance
# Calculate with the given formula the amount of particles each iteration of time

""" For this instance we take Palladium-231 which has a decay constant of 2.1158 * 10 ** -5. """

# Give the variables

amount_of_particles = 10000
duration = 1000
decay_constant = 2.1158 * 10 ** -5

# Calculate the formula
N_t = []

for time_instance in range(duration):
    N_t.append(amount_of_particles)
    amount_of_particles = amount_of_particles * np.exp(-decay_constant*time_instance)


plt.plot(N_t)
plt.title('Amount of not decayed nuclei for each iteration of time')
plt.xlabel('Time')
plt.ylabel('Nuclei amount')
plt.show()

