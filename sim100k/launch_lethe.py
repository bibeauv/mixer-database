import os
import sys
sys.path.insert(1, '/home/bibeauv/scratch/sim100k')
import MixerSim as MS

MS.launch_gmsh('/home/bibeauv/scratch/soft/gmsh-4.5.6-Linux64/bin/gmsh',min_mesh_length=0.003,min_max=10,decrease=0.001)

lethe = '/home/bibeauv/scratch/soft/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d'

os.system(lethe + ' mixer.prm')
