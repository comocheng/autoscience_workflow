#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --job-name=single_point
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

python $AUTOSCIENCE_REPO/dft/run_single_point.py $1 $2
