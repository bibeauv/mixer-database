# ----------------------------------------------------------------------------
# Script python permettant la recueille des résultats :
# Après la simulation, le script parcoure les dossiers, recueille les
# résultats sur le torque et calcule le nombre de Reynolds.
# Ce script permettra également de construire un fichier contenant
# toutes les informations importantes à la mise en place du réseau de neurone.
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

import os
import sys
import math
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

progress = 1

database_name = "mixer_database_" + str(start) + "-" + str(stop)

open(database_name + ".txt", "w").close()
fic_data = open(database_name + ".txt", "a")
for d in set_dirs:
    sim_path = path + "mixer_" + str(d)
    os.chdir(sim_path)

    fic_data.write("mixer_" + str(d) + "\t")

    fic_tag = open("mixer.txt","r")
    geo_info = fic_tag.read()
    fic_data.write(geo_info)
    geo_info = geo_info.split("\t")
    w = geo_info[-2] # Angular velocity
    D = geo_info[1] # Impeller diameter
    fic_tag.close()

    try:
        with open("torque.00.dat","r") as fic_torque:
            lines = fic_torque.readlines()
        fic_torque.close()
    
        get_torque = lines[-1]
        get_torque = get_torque.split(" ")
        torque = get_torque[3]

        # Calculate Reynolds number and power number
        N = float(w)/2/math.pi
        D = 1/float(D)
        torque = float(torque)
        Re = D*D*N
        Np = 2*math.pi*torque/N/N/D/D/D/D/D

        fic_data.write("Re\t%f\t" % Re)
        fic_data.write("Np\t%f\n" % Np)

    except:
        fic_data.write("!SIMULATION FAILED!\n")
    
    pourcentage = progress/total_mixer
    sys.stdout.write("\rProgress: " + "{:.2%}".format(pourcentage))
    sys.stdout.flush()
    progress += 1

fic_data.close()
sys.stdout.write("\n")