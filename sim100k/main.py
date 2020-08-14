import MixerSim as MS
import os

#os.system('rm -r mixer_*')

MS.generate_data_folders(TD = [2, 5, 2],
                         HT = [1, 1.5, 2],
                         TC = [2, 5, 2], 
                         DW = [3, 6, 2],
                         WHub = [0.75, 0.75, 1],
                         E = [0.1, 0.1, 1],
                         theta = [0.78, 0.78, 1],
                         Re = [0, 2, 2],
                         start = 1,
                         stop = 1,
                         enable = False)

MS.launch_gmsh(gmsh='gmsh',
               first_mixer=1,
               last_mixer=8,
               max_mesh_length=0.04,
               min_max=0.1,
               decrease=0.01,
               enable=False)

MS.launch_job(first_mixer=1, last_mixer=8, enable=False)

MS.launch_local(lethe='/home/bibeauv/soft/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d',
                first_mixer=1,
                last_mixer=8,
                enable=False)

MS.get_torque_and_write_data(first_mixer=1,
                             last_mixer=8,
                             enable=True)