# project_cs
Project Computational Science about nuclear fission.

In order to conduct experiments with these pieces of code, it is important to understand that 
fission.py is only used for data acquisition compiled to a csv file and all analysis is done
with said csv file in a different python file.

To change the parameters that the model works with, it is possible to change the tuples in
the list values_run. Each tuple represents values in the shape (amount of particles, radius of the system)
and the entire list of values is iterated through to acquire data for all parametersets.

When the intention is just to check whether the analysis on acquired data is reproducable,
it is recommended to just run the data_analysis.py file. The data acquisition (fission.py) runs 
many large simulations which would result in a computational time between 12 and 24 hours 
depending on system speed.

data_analysis.py opens data.csv and does the required data manipulation to show a graph 
that should resemble figure_reaction_speed.png.
