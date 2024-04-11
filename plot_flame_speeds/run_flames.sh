#!/bin/bash
#SBATCH --ntasks=26
#SBATCH --constraint=cascadelake
#SBATCH --time=24:00:00

python /work/westgroup/harris.se/autoscience/reaction_calculator/plot_flame_speeds/run_flame_speeds.py $1
