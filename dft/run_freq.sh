#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --partition=short,sharing,west
#SBATCH --job-name=freq

python $AUTOSCIENCE_REPO/dft/run_freq.py $1
