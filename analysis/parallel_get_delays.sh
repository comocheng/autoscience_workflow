#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=26
#SBATCH --array=0-200

python $AUTOSCIENCE_REPO/analysis/parallel_get_delays.py $1 $SLURM_ARRAY_TASK_ID
