#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --account=rrg-blaisbru
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=valerie.bibeau@hotmail.ca
#SBATCH --output=%x-%j.out

source $HOME/.dealii
module load python/3
module load scipy-stack
source ~/ENV/bin/activate
srun python3 launch_data.py
