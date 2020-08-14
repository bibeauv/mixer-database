import os

geo_path = os.getcwd()

path, dirs, files = next(os.walk(geo_path))
for d in np.linspace(1, len(dirs), len(dirs), dtype=int):
    os.chdir(geo_path + '/mixer_' + str(d))
    lethe = '/home/bibeauv/scratch/lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d'
    os.system(lethe + ' mixer.prm')