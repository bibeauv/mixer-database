import MixerSim as MS
import os
import math

enable_data, enable_job, enable_torque = MS.enable()

MS.generate_data_folders(TD = [2, 5, 2],
                         HT = [1, 1.5, 2],
                         TC = [2, 5, 2], 
                         DW = [3, 6, 2],
                         WHub = [0.75, 0.75, 1],
                         E = [0.1, 0.1, 1],
                         theta = [math.pi/4, math.pi/4, 1],
                         power_Re = [0, 2, 2],
                         multiplier_Re = 2,
                         enable = enable_data)

MS.launch_local(lethe='/home/bibeauv/soft/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d',
                enable=True)

MS.launch_job(enable=enable_job)

MS.get_torque_and_write_data(enable=enable_torque)