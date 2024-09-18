#!/bin/bash
#SBATCH --job-name=export_improvement_scores
#SBATCH --mem=20Gb
#SBATCH --time=04:00:00

python $AUTOSCIENCE_REPO/analysis/export_improvement_scores.py $1
