#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=26
#SBATCH --array=1-12

python $AUTOSCIENCE_REPO/analysis/get_base_delays.py $1 $SLURM_ARRAY_TASK_ID
