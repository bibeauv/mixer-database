import os
import numpy as np
from jinja2 import Template
import pandas

# ---------------------------------------------------------------------------------
# METHODS

def create_data_folders(mesh_length, enable):
    if enable == True:
        os.system('rm -r mixer_*')
        path = os.getcwd()
        i = 1
        for ml in mesh_length:
            # Read the mixer.geo file
            fic_geo = open('mixer.geo','r')
            cte_geo = fic_geo.read()
            template = Template(cte_geo)
            mesh = template.render(mesh_length = ml,
                                min_mesh_length = ml/10)
            fic_geo.close()

            # Create folder
            os.mkdir(path + '/mixer_' + str(i))

            # Copy mixer.prm file
            os.system('cp mixer.prm ' + path + '/mixer_' + str(i))

            # Go to folder
            os.chdir(path + '/mixer_' + str(i))

            # Write the mixer.geo file
            wr_geo = open('mixer.geo','w')
            wr_geo.write(mesh)
            wr_geo.close()

            i = i + 1
            os.chdir('../')

    return

def launch_gmsh_and_lethe(mesh_length, lethe_executable, enable):
    this_path = os.getcwd()

    if enable == True:
        for d in np.linspace(1,len(mesh_length),len(mesh_length),dtype=int):
            os.chdir(this_path + '/mixer_' + str(d))
            # Launch gmsh
            os.system('gmsh -3 mixer.geo -v 0 -o mixer.msh')
            # Launch Lethe
            print('/////////////////////// Launching mixer_' + str(d) + ' ///////////////////////')
            os.system(lethe_executable + ' mixer.prm')

        os.chdir('../')
    
    return

def get_torque(mesh_length):
    this_path = os.getcwd()

    torque_vec = []
    for d in np.linspace(1,len(mesh_length),len(mesh_length),dtype=int):
        os.chdir(this_path + '/mixer_' + str(d))
        try:
            with open("torque.00.dat","r") as fic_torque:
                lines = fic_torque.readlines()
            fic_torque.close()
        
            torque = lines[-1]
            torque = torque.split(" ")
            torque = torque[3]
            torque_vec.insert(len(torque_vec), float(torque))

        except:
            pass

    return torque_vec

# END METHODS
# ---------------------------------------------------------------------------------

mesh_length = np.linspace(0.1, 0.03, 8).tolist()

create_data_folders(mesh_length, False)

lethe = '/home/bibeauv/soft/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d'
launch_gmsh_and_lethe(mesh_length, lethe, False)

torque = get_torque(mesh_length)

err_rel = []
for t in np.arange(0, len(torque)):
    err = np.abs(torque[t] - torque[-1])/torque[-1]*100
    err_rel.insert(len(err_rel), err)

d = {'Mesh Lenght': mesh_length, 'Torque': torque, 'Erreur': err_rel}
df = pandas.DataFrame(data=d)

print(df)