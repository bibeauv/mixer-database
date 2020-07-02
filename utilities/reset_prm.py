# ---------- Utility 1 ----------
# Reset the mixer.prm in each mixer file
# ____________________
# Valérie Bibeau, 2020

import os

path = os.getcwd() + "/"

path, dirs, files = next(os.walk(path))

for d in dirs:
    sim_path = path + d
    os.chdir(sim_path)
    os.system('cp ' + path + 'mixer.prm ' + sim_path)
