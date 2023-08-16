#!/bin/bash
#SBATCH --job-name=concat_shell
#SBATCH --partition=short
#SBATCH --time=00:30:00


python /work/westgroup/harris.se/autoscience/reaction_calculator/concat_molecules/shell.py $1 $2

