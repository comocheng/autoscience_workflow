#!/bin/bash
#SBATCH --job-name=AUTORUNNER
#SBATCH --time=24:00:00
#SBATCH --partition=short

# argument is yaml file with list of stuff to compute
python /work/westgroup/harris.se/autoscience/reaction_calculator/automatic_runner/auto_runner.py $1
