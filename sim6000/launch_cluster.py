# ------------------------------------------------------------------------
# Script python permettant de lancer les simulations :
# Le script parcoure les dossiers, génère le mesh et lance Lethe
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

import os
import numpy as np

path = os.getcwd() + "/"

path, dirs, files = next(os.walk(path))
number_of_dirs = len(dirs)

print ("Total of folders =", number_of_dirs)
print ("Set the first mixer to simulate :")
start = int(input())
print ("Set the last mixer to simulate :")
stop = int(input())

total_mixer = stop - start + 1

set_dirs = np.linspace(start,stop,total_mixer,dtype=int)

for d in set_dirs:
    mixer_path =  "mixer_" + str(d)
    sim_path = path + mixer_path
    os.chdir(sim_path)
    os.system('cp ' + path + 'launch.sh ' + sim_path)

    os.system('sbatch -J ' + mixer_path + ' launch.sh')