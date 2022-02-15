import os
import sys
sys.path.insert(1, '/home/bibeauv/scratch/sim100k')
import MixerSim as MS

MS.launch_gmsh('gmsh',min_mesh_length=0.003,min_max=10)

lethe = '/home/bibeauv/scratch/soft/lethe/inst/bin/gls_navier_stokes_3d'

os.system(lethe + ' mixer.prm')
