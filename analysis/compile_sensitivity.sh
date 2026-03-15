#!/bin/bash
#SBATCH --job-name=compile_sensitivity
#SBATCH --time=00:10:00
#SBATCH --partition=short,sharing,west
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

# first argument is chem_annotated.inp file
python $AUTOSCIENCE_REPO/analysis/compile_sensitivity.py $1
