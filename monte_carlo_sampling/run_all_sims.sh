#!/bin/bash
#SBATCH --job-name=monte_carlo
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --partition=short
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=16
#SBATCH --array=0-99%20


start_index=$(( 100 * $SLURM_ARRAY_TASK_ID ))

python $AUTOSCIENCE_REPO/monte_carlo_sampling/run_all_sims.py $start_index
