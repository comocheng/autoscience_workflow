#!/bin/bash
#SBATCH --job-name=error_vs_included_calcs
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=16
#SBATCH --array=0-50

python /work/westgroup/harris.se/autoscience/reaction_calculator/error_vs_num_included/compute_error.py $SLURM_ARRAY_TASK_ID
