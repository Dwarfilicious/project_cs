# Data analysis from csv file


import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# len of runs should be 2 * runs * experiments
columns = []
index = []
runs = []

# toggle csv file
# with open('data2 _manually_altered.csv', 'r') as f:
with open('data3.csv', 'r') as f:
    for line in f:
        line = line.strip().split(',')

        if str(line[0])[0] == "e":
            columns.append(f"{line[0]}")
            # (str(line[0]))
        
        if str(line[1])[0] == "r":
            index.append(line[1][4:6])
            # line[1]

        else:
            linelist = []
            for value in line:
                try:
                    linelist.append(int(value))
                except ValueError:
                    skip = 1
            runs.append(linelist)
            
index = set(index)
index = list(index)
index_sorted = sorted(index, key=int)

columns = set(columns)
columns = list(columns)
columns.sort()

newcolumns = []
count = 2

# put particle and neutron in column names
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

# initialize dataframe
df = pd.DataFrame(columns=newcolumns, index=index_sorted)

# put runs in dataframe in correct order
indexlist = []
start = 0
restart = 0
check_even = 2

# matrix solving algorithm
while len(indexlist) < len(runs):

    indexlist.append(start)

    if check_even % 2 == 0:
        add = 1
    else:
        add = (2 * len(index_sorted)) - 1

    if start + add < len(runs):
        start = start + add
    else:
        start = restart + 2
        restart += 2

    check_even += 1

count = 0 
for a in index_sorted:
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

# first_experiment = df.iloc[0]
# halved_count = int(len(df.count()) / 2)


# for i in range(1,halved_count + 1):
#     first_experiment.drop(f"exp {i}neutron" , inplace=True)

# final_particle_count_amounts = []

# # calculating lowest amount of particles in all the lists

# for experiment in first_experiment:
#     final_particle_amount = experiment[0] - experiment[-1]
#     final_particle_count_amounts.append(final_particle_amount)

# lowest_particle_count = min(final_particle_count_amounts)

# list_of_times = []

# for experiment in first_experiment:
#     time_count = 0
#     stop_value = experiment[0] - lowest_particle_count

#     for value in experiment:
#         if value > stop_value:
#             time_count += 1
#         else:
#             continue
#     list_of_times.append(time_count)

# reaction_speed_list = []

# for time_steps in list_of_times:
#         reaction_speed = lowest_particle_count / time_steps
#         reaction_speed_list.append(reaction_speed)

# print(reaction_speed_list)

def amount_particles_reacted(dataframe):
    '''
    Function to calculate reaction speed from a dataframe
    '''

    # determine smallest amount of interactions that take place in an experiment
    find_smallest = []

    for col in dataframe.columns:
        if col[5] == "p" or col[6] == "p":
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
    mean_reaction_times = []
    sdev_reaction_times = []
    lower_bounds_list = []
    upper_bounds_list = []

    # select particle values for each experiment
    # title_count is for collecting experiment numbers
    title_count = 0
    for col in dataframe.columns:
        if col[5] == "p" or col[6] == "p":
            title_count += 1
            experiments_list.append(title_count)

            runs = dataframe[col]

            # get reaction time for each run
            reaction_times = []

            # iterate through runs and get reaction times
            for run in runs:
                count = 0 
                for datapoint in run:
                    if run[0] - datapoint >= minimum:
                        reaction_time = minimum / count
                        
                    count += 1

                reaction_times.append(reaction_time)
        
            # get mean and sd for each experiment
            mean_reaction_time = np.mean(reaction_times)
            sdev_reaction_time = np.std(reaction_times)
            mean_reaction_times.append(mean_reaction_time)
            sdev_reaction_times.append(sdev_reaction_time)

            # confidence intervals - bootstrap? - *v
            lower_bound = np.percentile(reaction_times, 2.5)
            upper_bound = np.percentile(reaction_times, 97.5)
            lower_bounds_list.append(lower_bound)
            upper_bounds_list.append(upper_bound)

    return experiments_list, mean_reaction_times, sdev_reaction_times, lower_bounds_list, upper_bounds_list
            
a = amount_particles_reacted(df)

exps, means, sdevs, lowerlist, upperlist = reaction_time(df, a)

exps = np.array(exps)
means = np.array(means)
sdevs = np.array(sdevs)
lowerlist = np.array(lowerlist)
upperlist = np.array(upperlist)

# plt.plot(exps, means)
# plt.show() - % stck - *        experiment waardes in figuur?

# plot 95CI
fig, ax = plt.subplots()
ax.plot(exps,means)


# toggle for standard dev
ax.fill_between(exps, (lowerlist), (upperlist), color='b', alpha=0.1)
# ax.fill_between(exps, (means - sdevs), (means + sdevs), color='b', alpha=0.1)

# set limits
ax.set_ylim([1, 5])
 
plt.title("mean reaction times for experiments, with 95% confidence intervals")
plt.xlabel("experiments")
plt.ylabel("mean reaction time")
plt.show()

print(df)


# get names of experiments
# experiment_list = []
