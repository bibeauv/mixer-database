import sys
sys.path.insert(1, '/home/bibeauv/scratch/simLHS')
import math
import MixerSim as MS

MS.generate_data_folders(TD = [2, 5],
                         HT = [1, 1.5],
                         TC = [2, 5], 
                         DW = [3, 6],
                         WHub = 0.75,
                         E = 0.1,
                         theta = math.pi/4,
                         Re = [1, 20],
                         initial_Re = 10,
                         ne = 10,
                         enable = True)
