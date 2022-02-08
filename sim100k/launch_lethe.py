import os
import sys
sys.path.insert(1, '/home/bibeauv/scratch/simLHS')
import MixerSim as MS

MS.launch_gmsh('/home/bibeauv/.local/easybuild/software/2017/avx512/Compiler/gcc7.3/gmsh/4.6.0/bin/gmsh',min_mesh_length=0.003,min_max=10,decrease=0.001)

lethe = '/home/bibeauv/scratch/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d'

os.system(lethe + ' mixer.prm')
