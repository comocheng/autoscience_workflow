#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --job-name=freq_ts
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL


python $AUTOSCIENCE_REPO/dft/run_freq_ts.py $1
