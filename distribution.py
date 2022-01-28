import numpy as np
import matplotlib.pyplot as plt

data = []

for i in range(10**6):
    # energy distribution in MeV
    energy = np.random.normal(0.75, 2.2)
    while energy < 0:
        energy = np.random.normal(0.75, 2.2)

    data.append(energy)

plt.hist(data, bins=50, range=[0, 7])
plt.xlabel('E (MeV')
plt.ylabel('frequencies')
plt.show()
