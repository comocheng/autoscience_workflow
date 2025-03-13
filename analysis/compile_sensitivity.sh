#!/bin/bash
#SBATCH --job-name=compile_sensitivity
#SBATCH --time=00:20:00
#SBATCH --partition=express,short,west

# first argument is chem_annotated.inp file, second argument is the main table to use
python $AUTOSCIENCE_REPO/analysis/compile_sensitivity.py $1 $2
