#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --account=rrg-blaisbru
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=15G
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=valerie.bibeau@hotmail.ca
#SBATCH --output=%x-%j.out

source $HOME/.dealii
srun ../../lethe/build/applications/gls_navier_stokes_3d/gls_navier_stokes_3d mixer.prm
