import sys
sys.path.insert(1, '/home/bibeauv/scratch/simLHS')
import MixerSim as MS

MS.get_torque_and_write_data(first_mixer=0, last_mixer=9999)
