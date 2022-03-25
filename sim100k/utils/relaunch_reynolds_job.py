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
    
    files_out = glob.glob('mixer_' + str(mixer) + '-*.out')
    id_files_out = [int(file.split('-')[1].split('.')[0]) for file in files_out]
    id_files_out.sort()
    last_file_out = id_files_out[-1]
    
    with open('mixer_' + str(mixer) + '-' + str(last_file_out) + '.out') as f:
        output = f.readlines()
    
    i = -1
    while True:
        if output[i].split(' ')[0] == 'Newton':
            newton_line = output[i].split(' ')[2]
            residual = float(output[i].split(' ')[7].rstrip('\n'))
            break
        else:
            i -= 1
    
    if os.path.isfile('torque.00.dat') and newton_line == '19' and residual > 1e-8:
        os.system('cp ../mixer.prm .')
        
        tag = open("mixer.txt","r")
        ratios = tag.read()
        ratio = ratios.split('\t')
        rTD = float(ratio[1])
        tag.close()
        
        last = open("last_reynolds.txt","w")
        last.write(str(float(ratio[15])))
        last.close()

        tag = open("mixer.txt","w")
        ratio[15] = '50.000000'
        ratios = "\t".join(ratio)
        tag.write(ratios)
        tag.close()
        
        prm = open("mixer.prm","r")
        cte = prm.read()
        template = Template(cte)
        parameters = template.render(viscosity = (1/rTD)**2/50,
                                     initial_viscosity = (1/rTD)**2/25)
        prm.close()
        
        prm = open("mixer.prm","w")
        prm.write(parameters)
        prm.close()
        
        os.system('cp ../utils/relaunch_lethe.sh .')
        os.system('cp ../utils/relaunch_lethe.py .')
        os.system('sbatch -J ' + 'mixer_' + str(mixer) + ' relaunch_lethe.sh')

os.chdir('../utils')
