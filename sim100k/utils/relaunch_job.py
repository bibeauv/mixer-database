import os
import numpy as np
from jinja2 import Template
import glob

# First and last mixer
print('First mixer to relaunch job :')
first_mixer = int(input())
print('Last mixer to relaunch job :')
last_mixer = int(input())

this_path = os.getcwd() + '/..'
for mixer in np.linspace(first_mixer, last_mixer, (last_mixer-first_mixer)+1, dtype=int):
    geo_path = this_path + '/mixer_' + str(mixer)
    os.chdir(geo_path)
    with open(glob.glob('mixer_' + str(mixer) + '-*.out')[-1]) as f:
        output = f.readlines()
    if not os.path.isfile('torque.00.dat') and output[-2] == 'Aborting!\n' and output[-3] != 'std::exception\n':
        os.system('cp ../utils/mixer.geo .')
        
        tag = open("mixer.txt","r")
        ratios = tag.read()
        ratio = ratios.split('\t')
        tag.close()

        tag = open("mixer.txt","w")
        ratio[13] = '0.0'
        ratios = "\t".join(ratio)
        tag.write(ratios)
        tag.close()
        
        geo = open("mixer.geo","r")
        cte = geo.read()
        template = Template(cte)
        geometries = template.render(ratioTD = float(ratio[1]),
                                     ratioHT = float(ratio[3]),
                                     ratioTC = float(ratio[5]),
                                     ratioDW = float(ratio[7]),
                                     ratioDW_Hub = float(ratio[9]),
                                     p_thick = float(ratio[11]),
                                     theta = 0.0,
                                     min_mesh_length = "{{min_mesh_length}}",
                                     max_mesh_length = "{{max_mesh_length}}")

        geo.close()
        geo = open("mixer.geo","w")
        geo.write(geometries)
        geo.close()
        
        os.system('cp ../utils/relaunch_lethe.sh .')
        os.system('cp ../utils/relaunch_lethe.py .')
        os.system('sbatch -J ' + 'mixer_' + str(mixer) + ' relaunch_lethe.sh')

os.chdir('../utils')
