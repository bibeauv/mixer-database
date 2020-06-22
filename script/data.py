# ----------------------------------------------------------------------------
# Script python permettant la recueille des résultats :
# Après la simulation, le script parcoure les dossiers, recueille les
# résultats sur le torque et calcule le nombre de Reynolds.
# Ce script permettra également de construire un fichier contenant
# toutes les informations importantes à la mise en place du réseau de neurone.
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

import os

path = "/home/bibeauv/soft/lethe/mixer-database/script/"

path, dirs, files = next(os.walk(path))

open("mixer_database.txt", "w").close()
fic_data = open("mixer_database.txt","a")
for d in dirs:
    sim_path = path + d
    os.chdir(sim_path)

    fic_tag = open("mixer.txt","r")
    geo_info = fic_tag.read()
    fic_data.write(geo_info)
    fic_tag.close()

    with open("torque.03.dat","r") as fic_torque:
        lines = fic_torque.readlines()
    fic_torque.close()
    
    get_torque = lines[-1]
    get_torque = get_torque.split(" ")
    get_torque = get_torque[3]

    fic_data.write("torque\t%s\n" % get_torque)

fic_data.close()