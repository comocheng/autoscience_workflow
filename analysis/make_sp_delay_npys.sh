#!/bin/bash
#SBATCH --job-name=sp_sens
#SBATCH --mem=20Gb
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=26
#SBATCH --partition=short,west,sharing
#SBATCH --array=0-300%20


python $AUTOSCIENCE_REPO/analysis/make_sp_delay_npys.py $1 $SLURM_ARRAY_TASK_ID
