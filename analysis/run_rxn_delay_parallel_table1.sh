#!/bin/bash
#SBATCH --job-name=delay1
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=26
#SBATCH --array=0-50


start_index=$(($SLURM_ARRAY_TASK_ID * 50))

python /work/westgroup/harris.se/autoscience/reaction_calculator/delay_uncertainty/make_rxn_delay_npys.py $1 1 $start_index
