# Data analysis from csv file
# d

import csv
import pandas as pd
import matplotlib.pyplot as plt

# data = open('bestand.csv')
# csvreader = csv.reader(data)

df = pd.read_csv('bestand.csv', header=None)
ax = df.plot(kind = "line")
ax.legend(["Particles", "Neutrons"])
plt.xlabel("time")
plt.ylabel("quantity")
plt.show()