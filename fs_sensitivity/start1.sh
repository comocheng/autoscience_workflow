#!/bin/bash
#SBATCH --job-name=flame_sensitivity
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=16

python /work/westgroup/harris.se/autoscience/reaction_calculator/fs_sensitivity/generate_perturbed.py $1
