#!/bin/bash
#SBATCH --job-name=compile_sensitivity
#SBATCH --time=00:20:00
#SBATCH --partition=express,short,west

python /work/westgroup/harris.se/autoscience/reaction_calculator/delay_uncertainty/compile_sensitivity.py $1
