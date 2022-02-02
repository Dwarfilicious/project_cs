# Data analysis from csv file

import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

columns = []
index = []
runs = []

# skip explanation lines
skip_amount_of_lines = 1

# open csv and put the values from csv in lists
with open('reruns75.csv', 'r') as f:
    line_counter = 0
    for line in f:
        if line_counter > skip_amount_of_lines:
            line = line.strip().split(',')

            # get experiment names for columns
            if str(line[0])[0] == "e":
                columns.append(f"{line[0]}")
                # (str(line[0]))
            
            # get run names for indices
            if str(line[1])[0] == "r":
                index.append(line[1][4:6])
                # line[1]

            # convert run to a list and then append the runs to a list
            else:
                linelist = []
                for value in line:
                    try:
                        linelist.append(int(value))
                    except ValueError:
                        skip = 1
                runs.append(linelist)

        line_counter += 1

# get clean list of indices
index = set(index)
index = list(index)
index_sorted = sorted(index, key=int)

# get clean list of columns
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

# matrix solving algorithm to fill in the correct runs in the correct dataframe cell
while len(indexlist) < len(runs):

    indexlist.append(start)

    # add 1 every other loop
    if check_even % 2 == 0:
        add = 1
    # otherwise add 2 * length of amount of runs list - 1
    else:
        add = (2 * len(index_sorted)) - 1

    # if start exceeds the length, reset the number and update reset
    if start + add < len(runs):
        start = start + add
    else:
        start = restart + 2
        restart += 2

    check_even += 1

# fill in the dataframe
count = 0 
for a in index_sorted:
    for b in newcolumns:
        indic = indexlist[count]
        df.at[a, b] = runs[indic]
        count += 1

def reaction_speed(dataframe, minimum, stop):
    '''
    Function to get average, standard deviations and confidence intervals of reaction speed
    '''

    experiments_list = []
    mean_reaction_speeds = []
    sdev_reaction_speeds = []
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
            reaction_speeds = []

            # iterate through runs and get reaction times
            # stopcount to stop at 30 and get original confidence interval
            stopcount = 0
            for run in runs:

                # stop if we have reached limit
                if stopcount == stop:
                    break
                
                count = 0 
                for datapoint in run:
                    if run[0] - datapoint >= minimum:
                        reaction_speed = minimum / count
                        
                    count += 1

                reaction_speeds.append(reaction_speed)
                stopcount += 1

            # get mean and sd for each experiment
            mean_reaction_speed = np.mean(reaction_speeds)
            sdev_reaction_speed = np.std(reaction_speeds)
            mean_reaction_speeds.append(mean_reaction_speed)
            sdev_reaction_speeds.append(sdev_reaction_speed)

            # confidence intervals - bootstrap? - *v
            lower_bound = np.percentile(reaction_speeds, 2.5)
            upper_bound = np.percentile(reaction_speeds, 97.5)
            lower_bounds_list.append(lower_bound)
            upper_bounds_list.append(upper_bound)

    return lower_bounds_list, upper_bounds_list

# compare old and new CI
lower_og, upper_og = reaction_speed(df, 300, 30)
lower_new, upper_new = reaction_speed(df, 300, 100)
print(f"old confidence interval: {lower_og}, {upper_og}")
print(f"new confidence interval (more runs) {lower_new}, {upper_new}")

