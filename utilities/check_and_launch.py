# ---------- Utility script ----------
# Check simulations that failed and launch them again on the cluster
# ____________________
# Valérie Bibeau, 2020

import os
import numpy as np

path = os.getcwd() + "/"

path, dirs, files = next(os.walk(path))
number_of_dirs = len(dirs)

number_of_mixers = np.linspace(1,number_of_dirs,number_of_dirs)

for i in number_of_mixers:
    mixer_path =  "mixer_" + str(int(i))
    sim_path = path + mixer_path
    os.chdir(sim_path)

    try:
        with open("torque.00.dat","r") as fic_torque:
            lines = fic_torque.readlines()
        fic_torque.close()

        if len(lines) != 2:
            raise

    except:
        #os.system('sbatch -J ' + mixer_path + ' launch.sh')
        print(mixer_path + " relaunch!")
