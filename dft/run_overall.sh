#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL


python $AUTOSCIENCE_REPO/dft/run_overall.py $1

