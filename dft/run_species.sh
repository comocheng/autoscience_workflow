#!/bin/bash
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL

python $AUTOSCIENCE_REPO/dft/run_species.py $1
#SBATCH --time=24:00:00

