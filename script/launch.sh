#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --acount=rrg-blaisbru
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=6G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=valerie.bibeau@hotmail.ca
#SBATCH --output=%x-%j.out

srun gls_navier_stokes_3d mixer.prm