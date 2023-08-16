#!/bin/bash
#SBATCH --time=24:00:00

python /work/westgroup/harris.se/autoscience/reaction_calculator/dft/run_reaction_arkane.py $1 $2

