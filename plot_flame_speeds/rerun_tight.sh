#!/bin/bash
#SBATCH --ntasks=16
#SBATCH --time=24:00:00

python /work/westgroup/harris.se/autoscience/reaction_calculator/plot_flame_speeds/tight_rerun_flame_speeds.py $1

