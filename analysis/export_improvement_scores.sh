#!/bin/bash
#SBATCH --job-name=export_improvement_scores
#SBATCH --mem=20Gb
#SBATCH --time=01:00:00
#SBATCH --partition=sharing,short,west
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=16

python $AUTOSCIENCE_REPO/analysis/export_improvement_scores.py $1
