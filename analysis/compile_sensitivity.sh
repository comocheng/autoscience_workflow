#!/bin/bash
#SBATCH --job-name=compile_sensitivity
#SBATCH --time=00:20:00
#SBATCH --partition=express,short,west

python $AUTOSCIENCE_REPO/analysis/compile_sensitivity.py $1
