import MixerSim as MS

MS.launch_gmsh_and_job(gmsh='gmsh',
                       min_mesh_length=0.003,
                       min_max=10,
                       decrease=0.001)
