#!/bin/bash
#SBATCH --time=06:00:00
#SBATCH --account=rrg-blaisbru
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=32G
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=valerie.bibeau@hotmail.ca
#SBATCH --output=%x-%j.out

source $SCRATCH/.dealii
source $SCRATCH/ENV/bin/activate
srun python3 relaunch_lethe.py
