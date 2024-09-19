#!/bin/bash
#SBATCH --time=04:00:00

python $AUTOSCIENCE_REPO/dft/run_species.py $1
#SBATCH --time=24:00:00

