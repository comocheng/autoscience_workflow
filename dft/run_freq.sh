#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --job-name=freq

python $AUTOSCIENCE_REPO/dft/run_freq.py $1
