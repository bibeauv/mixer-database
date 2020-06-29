# ------------------------------------------------------------------------
# Script python permettant de lancer les simulations :
# Le script parcoure les dossiers, génère le mesh et lance Lethe
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

from jinja2 import Template
import os
from subprocess import Popen, PIPE
import time
import warnings
warnings.filterwarnings("error")

path = "/home/bibeauv/scratch/"

path, dirs, files = next(os.walk(path))

start_time = time.time()
for d in dirs:
    sim_path = path + d
    os.chdir(sim_path)
    os.system('cp ' + path + 'launch.sh ' + path + d)

    os.system('sbatch launch.sh')