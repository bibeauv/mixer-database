import MixerSim as MS

MS.launch_gmsh_and_job(gmsh='gmsh',
                       max_mesh_length=0.04,
                       min_max=0.1,
                       decrease=0.01,
                       enable=True)
