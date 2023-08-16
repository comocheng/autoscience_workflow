#!/bin/bash
#SBATCH --job-name=concat_arkane
#SBATCH --partition=short
#SBATCH --time=00:30:00


python /work/westgroup/harris.se/autoscience/reaction_calculator/concat_molecules/concat_arkane.py $1

