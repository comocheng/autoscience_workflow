#!/bin/bash
#SBATCH --time=24:00:00

python /work/westgroup/harris.se/autoscience/reaction_calculator/run_analysis.py $1
