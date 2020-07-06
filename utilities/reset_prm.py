# ---------- Utility script for the simulation of 6250 ----------
# Reset the mixer.prm in each mixer file
# ____________________
# Valérie Bibeau, 2020

from jinja2 import Template
import os
import sys
import numpy as np

path = os.getcwd() + "/"
path, dirs, files = next(os.walk(path))
number_of_dirs = len(dirs)
step = 10                                                   # Here!

velocity = np.linspace(0.1,500,step)

first = np.arange(1,number_of_dirs,step)

progress = 1
total = number_of_dirs
for i in first:
    group = np.linspace(i,i+step-1,step)
    j = 0
    for v in velocity:
        # Open the parameter file
        fic_prm = open("mixer.prm","r")
        cte_prm = fic_prm.read()
        # Insert the parameters
        template_prm = Template(cte_prm)
        parameters = template_prm.render(omega = v)
        fic_prm.close()

        mixer = "mixer_" + str(int(group[j]))
        sim_path = path + mixer
        os.chdir(sim_path)
        wr_prm = open("mixer.prm","w")
        wr_prm.write(parameters)
        wr_prm.close()

        os.chdir("../")

        j += 1

        pourcentage = progress/total
        sys.stdout.write("\rProgress: " + "{:.2%}".format(pourcentage))
        sys.stdout.flush()
        progress += 1
sys.stdout.write("\n")