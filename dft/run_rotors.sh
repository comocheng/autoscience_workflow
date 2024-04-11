#!/bin/bash
#SBATCH --time=24:00:00

python /work/westgroup/harris.se/autoscience/reaction_calculator/dft/run_rotors.py $1 $2
