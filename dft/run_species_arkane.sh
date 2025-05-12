#!/bin/bash
#SBATCH --time=00:20:00
#SBATCH --partition=express,short,west

python $AUTOSCIENCE_REPO/dft/run_species_arkane.py $1

