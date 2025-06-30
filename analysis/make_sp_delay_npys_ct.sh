#!/bin/bash
#SBATCH --job-name=species_delays
#SBATCH --time=00:30:00
#SBATCH --partition=short
#SBATCH --array=0-400%8


python $AUTOSCIENCE_REPO/analysis/make_sp_delay_npys_ct.py $1 $SLURM_ARRAY_TASK_ID

