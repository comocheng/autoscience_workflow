#!/bin/bash
#SBATCH --time=00:20:00
#SBATCH --partition=short

python $AUTOSCIENCE_REPO/dft/run_species_arkane.py $1

