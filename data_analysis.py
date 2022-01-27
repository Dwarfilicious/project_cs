# Data analysis from csv file
# d a


import csv
import pandas as pd
import matplotlib.pyplot as plt

# data = open('bestand.csv')
# csvreader = csv.reader(data)

read_csv = pd.read_csv('bestand.csv', header=None)
print(read_csv)

# ax = df.plot(kind = "line")
# ax.legend(["Particles", "Neutrons"])
# plt.xlabel("time")
# plt.ylabel("quantity")
# plt.show()