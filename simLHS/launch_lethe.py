import os
import sys
sys.path.insert(1, '/home/bibeauv/scratch/simLHS')
import MixerSim as MS

lethe = '/home/bibeauv/scratch/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d'

os.system(lethe + ' mixer.prm')
