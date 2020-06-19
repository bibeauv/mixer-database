# ------------------------------------------------------------------------
# Script python permettant de lancer les simulations :
# Le script parcoure les dossiers, génère le mesh et lance Lethe
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

import os
import time

path = "/home/bibeauv/soft/lethe/mixer-database/script/"

path, dirs, files = next(os.walk(path))

for d in dirs:
    sim_path = path + d
    os.chdir(sim_path)
    
    # Launch gmsh
    os.system('gmsh -3 mixer.geo')

    # Launch Lethe
    # os.system('lethe gls_navier_stokes_3d')