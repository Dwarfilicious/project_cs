# Maksim Kolk

import numpy as np
import matplotlib.pyplot as plt

class Model:
    def __init__(self, prob=0.005, n_atoms=1000, intactcount=1000, decaycount=0):
        self.prob = prob
        self.n_atoms = n_atoms
        self.intactcount= intactcount
        self.decaycount = decaycount
        self.decaylist = []
        self.intactlist = []
    
    def make_atomlist(self):
        self.atomlist = []
        for x in range(self.n_atoms):
            state = "Intact"
            self.atomlist.append(Atom(state))
        return  
    
    def timestep(self):
        for i in range(len(self.atomlist)):
            if np.random.uniform() <= self.prob and self.atomlist[i].state == "Intact":
                self.atomlist[i].state = "Decayed"
                self.decaycount += 1 
                self.intactcount -= 1
        self.decaylist.append(self.decaycount)
        self.intactlist.append(self.intactcount)
        return

class Atom:
    def __init__(self, state):
        self.state = state
        
model = Model()
model.make_atomlist()

for x in range(1000):
    model.timestep()

decaylist = model.decaylist
intactlist = model.intactlist

plt.plot(range(len(intactlist)), intactlist)
plt.show()


