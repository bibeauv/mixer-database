# ---------- Utility script for the simulation of 6250 ----------
# Reset the mixer.prm in each mixer file
# ____________________
# Valérie Bibeau, 2020

import os

path = os.getcwd() + "/"

path, dirs, files = next(os.walk(path))

for d in dirs:
    sim_path = path + d
    os.chdir(sim_path)
    os.system('rm *.out')
    
    with open("mixer.prm", "r+") as f:
        l = f.readlines()
        f.seek(0)
        for i in l:
            if i != "  set number mesh adapt       = -1\n":
                f.write(i)
        f.truncate
