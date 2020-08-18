import os
import numpy as np
import sys

mixer_path = os.getcwd()

# First and last mixer
print('First mixer to reset launch.sh :')
first_mixer = int(input())
print('Last mixer to reset launch.sh :')
last_mixer = int(input())

progress = 1

for mixer in np.linspace(first_mixer, last_mixer, (last_mixer-first_mixer)+1, dtype=int):
    os.chdir(mixer_path + '/mixer_' + str(mixer))

    os.system('cp ../launch.sh .')

    pctg = progress/((last_mixer-first_mixer)+1)
    sys.stdout.write("\rProgress: " + "{:.2%}".format(pctg))
    sys.stdout.flush()
    progress += 1
sys.stdout.write("\n")