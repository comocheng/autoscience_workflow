#!/bin/bash
#SBATCH --job-name=species_delays
#SBATCH --time=01:00:00
#SBATCH --partition=short,west,sharing
#SBATCH --array=0-400%15


python $AUTOSCIENCE_REPO/analysis/make_sp_delay_npys_ct.py $1 $SLURM_ARRAY_TASK_ID

