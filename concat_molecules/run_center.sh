#!/bin/bash
#SBATCH --job-name=concat_center
#SBATCH --partition=short
#SBATCH --time=00:30:00


python /work/westgroup/harris.se/autoscience/reaction_calculator/concat_molecules/center.py $1

