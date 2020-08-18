# ---------- Utility script ----------
# Check simulations that failed and launch them again on the cluster
# ____________________
# Valérie Bibeau, 2020

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

number_of_mixers = np.linspace(start,stop,total_mixer,dtype=int)

for i in number_of_mixers:
    geo_path = path + '/mixer_' + str(i)
    os.chdir(geo_path)

    path, dirs, files = next(os.walk(geo_path))
    for j in np.linspace(1, len(dirs), len(dirs), dtype=int):
        os.chdir(geo_path + '/mixer_' + str(j))
        try:
            with open("torque.00.dat","r") as fic_torque:
                lines = fic_torque.readlines()
            fic_torque.close()

            if len(lines) != 2:
                raise

            print("mixer_" + str(i) + '-' + str(j) + " is OK!")

        except:
            print("********** " + "mixer_" + str(i) + '-' + str(j) + " will be launched again! **********")
            os.system('cp ../../new_launch.sh .')
            os.system('sbatch -J ' + "mixer_" + str(i) + '-' + str(j) + ' new_launch.sh')
