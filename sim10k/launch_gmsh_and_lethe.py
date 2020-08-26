import os
import sys
import numpy as np
sys.path.insert(1, '/home/bibeauv/scratch/sim10k')
import MixerSim as MS

lethe = '/home/bibeauv/scratch/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d'
gmsh = 'gmsh'

MS.launch_gmsh(gmsh=gmsh,
               max_mesh_length=0.04,
               min_max=0.1,
               decrease=0.01)

geo_path = os.getcwd()

path, dirs, files = next(os.walk(geo_path))
for d in np.linspace(1, len(dirs), len(dirs), dtype=int):
    os.chdir(geo_path + '/mixer_' + str(d))
    os.system(lethe + ' mixer.prm')