import MixerSim as MS
import os
import math

enable_data, enable_job, enable_torque = MS.enable()

MS.generate_data_folders(TD = [2, 5, 4],
                         HT = [1, 1.5, 4],
                         TC = [2, 5, 4], 
                         DW = [3, 6, 4],
                         WHub = [0.75, 0.75, 1],
                         E = [0.1, 0.2, 2],
                         theta = [math.pi/4, math.pi/6, 2],
                         Re = [0, 2, 10],
                         initial_Re = 10,
                         enable = enable_data)

MS.launch_gmsh_and_job(gmsh='gmsh',
                       max_mesh_length=0.04,
                       min_max=0.1,
                       decrease=0.01,
                       launch_big_or_small_sim=True,
                       enable=enable_job)

MS.get_torque_and_write_data(enable=enable_torque)