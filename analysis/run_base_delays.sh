#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=26
#SBATCH --array=1-12

python /work/westgroup/harris.se/autoscience/reaction_calculator/delay_uncertainty/get_base_delays.py $1 $SLURM_ARRAY_TASK_ID
