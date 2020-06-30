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

path = os.getcwd() + "/"

path, dirs, files = next(os.walk(path))

start_time = time.time()
for d in dirs:
    sim_path = path + d
    os.chdir(sim_path)
    
    # Launch gmsh
    ok = False
    mesh_length = 0.04
    while ok == False and mesh_length > 0:
        os.system('cp mixer.geo mixer_copy.geo')

        fic_geo = open("mixer_copy.geo","r")
        cte_geo = fic_geo.read()
        template = Template(cte_geo)
        mesh = template.render(mesh_length = mesh_length)
        fic_geo.close()

        wr_geo = open("mixer_copy.geo","w")
        wr_geo.write(mesh)
        wr_geo.close()

        p = Popen(['gmsh -3 mixer_copy.geo -o mixer.msh'], stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()

        if stderr != b'':
            mesh_length = mesh_length - 0.01
            os.system('rm mixer_copy.geo')
            print("*Mesh had been refined*")
        else:
            ok = True
            print("---------- Generating mesh of " + d + " is complete ----------")

print("---------- Total time of execution : %s seconds ----------" % (time.time() - start_time))