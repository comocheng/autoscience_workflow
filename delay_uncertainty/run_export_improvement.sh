#!/bin/bash
#SBATCH --job-name=export_improvement_scores
#SBATCH --mem=20Gb
#SBATCH --time=04:00:00

python /work/westgroup/harris.se/autoscience/reaction_calculator/delay_uncertainty/export_improvement_scores.py $1
