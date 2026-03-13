#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --time=18:00:00
#SBATCH --cpus-per-task=26
#SBATCH --array=0-200%20

python $AUTOSCIENCE_REPO/analysis/parallel_get_delays.py $1 $SLURM_ARRAY_TASK_ID
