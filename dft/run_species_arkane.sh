#!/bin/bash
#SBATCH --time=00:20:00
#SBATCH --partition=preempt
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL

python $AUTOSCIENCE_REPO/dft/run_species_arkane.py $1

