#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --job-name=freq
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL


python $AUTOSCIENCE_REPO/dft/run_freq.py $1
