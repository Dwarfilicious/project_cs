# Data analysis from csv file


import csv
import pandas as pd
import matplotlib.pyplot as plt

# data = open('bestand.csv')
# csvreader = csv.reader(data)

#
# read_csv = pd.read_csv('bestand.csv', header=None)
# print(read_csv)


# df = pd.read_csv('bestand.csv', header=None)

# ax = df.plot(kind = "line")
# ax.legend(["Particles", "Neutrons"])
# plt.xlabel("time")
# plt.ylabel("quantity")
# plt.show()

# plt.show()

df = pd.DataFrame

columns = []
index = []
runs = []

with open('bestand.csv', 'r') as f:
    for line in f:
        line = line.strip().split(',')

        if str(line[0])[0] == "e":
            columns.append(f"{line[0]}")
            # (str(line[0]))
        
        if str(line[1])[0] == "r":
            index.append(line[1])
        else:
            linelist = []
            for value in line:
                linelist.append(int(value))
            runs.append(linelist)

index = set(index)
index = list(index)
index.sort()

columns = set(columns)
columns = list(columns)
columns.sort()

newcolumns = []
count = 2

for x in range(len(columns)*2):
    new_words = []

    i = x
    i = int(i / 2) 

    new_words.append(columns[i])
    
    if count % 2 == 0:
        newword = "particle"
    else:
        newword = "neutron"
    new_words.append(newword)

    joined_word = "".join(new_words)

    newcolumns.append(joined_word)

    count += 1


df = pd.DataFrame(columns=newcolumns, index=index)

indexlist = []
start = 0
restart = 0
check_even = 2
# runs = len(newcolumns * len(index))
while len(indexlist) < len(runs):

    indexlist.append(start)

    if check_even % 2 == 0:
        add = 1
    else:
        add = (2 * len(index)) - 1

    if start + add < len(runs):
        start = start + add
    else:
        start = restart + 2
        restart += 2
        # minus 2 * len index - 1

    check_even += 1

# print(indexlist)

count = 0 
for a in index:
    for b in newcolumns:
        indic = indexlist[count]
        df.at[a, b] = runs[indic]
        count += 1

# df.to_csv('df.csv')

# I loop over all the particle lists from all experiments for 1 run , if the data list is an odd number, remove it
# II check one light of the amount of particles from one run, and then check the next. If one run is longer than another
# run then skip it, if its shorter, use that particle run length.
# III now use that length as a point of reference and check how many iterations it took to get to that length.
# For example, if the length is 300 than check for each run how much time it took to get 300 less particles


# clearing the data frames of the neutron counts

first_experiment = df.iloc[0]
halved_count = int(len(df.count()) / 2)


for i in range(1,halved_count + 1):
    first_experiment.drop(f"exp {i}neutron" , inplace=True)

final_particle_count_amounts = []

# calculating lowest amount of particles in all the lists

for experiment in first_experiment:
    final_particle_amount = experiment[0] - experiment[-1]
    final_particle_count_amounts.append(final_particle_amount)

lowest_particle_count = min(final_particle_count_amounts)

list_of_times = []

for experiment in first_experiment:
    time_count = 0
    stop_value = experiment[0] - lowest_particle_count

    for value in experiment:
        if value > stop_value:
            time_count += 1
        else:
            continue
    list_of_times.append(time_count)

reaction_speed_list = []

for time_steps in list_of_times:
        reaction_speed = lowest_particle_count / time_steps
        reaction_speed_list.append(reaction_speed)

print(reaction_speed_list)











