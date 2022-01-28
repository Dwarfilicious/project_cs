# Data analysis from csv file


import csv
import pandas as pd
import matplotlib.pyplot as plt

# data = open('bestand.csv')
# csvreader = csv.reader(data)


# read_csv = pd.read_csv('bestand.csv', header=None)
# print(read_csv)


# df = pd.read_csv('bestand.csv', header=None)

# ax = df.plot(kind = "line")
# ax.legend(["Particles", "Neutrons"])
# plt.xlabel("time")
# plt.ylabel("quantity")
# plt.show()

# plt.show()

# df = pd.DataFrame

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

def amount_particles_reacted(dataframe):
    '''
    Function to calculate reaction speed from a dataframe
    '''

    # determine smallest amount of interactions that take place in an experiment
    find_smallest = []

    for col in dataframe.columns:
        if col[5] == "p":
            run = dataframe[col]
            run = run[0]

            # decrease in amount of particles
            diff = run[0] / 2
            find_smallest.append(diff)
    amount = min(find_smallest)
    return amount

def reaction_time(dataframe, minimum):
    '''
    Function to get average and standard deviations of reaction speed
    '''

    experiments_list = []
    mean_reactiontime = []
    sd_reactiontime = []

    for col in dataframe.columns:
        if col[5] == "p":
            runs = dataframe[col]
            
            
a = amount_particles_reacted(df)
b = 


# # get names of experiments
#     experiment_list = []