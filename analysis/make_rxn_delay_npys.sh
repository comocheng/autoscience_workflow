#!/bin/bash
#SBATCH --job-name=rxn_sens
#SBATCH --mem=20Gb
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=26
#SBATCH --partition=short,west,sharing
#SBATCH --array=0-999%20


OFFSET=0
#OFFSET=1000
# OFFSET=2000
# OFFSET=3000
# OFFSET=4000
# OFFSET=5000
# OFFSET=6000


reaction_index=$(($SLURM_ARRAY_TASK_ID + $OFFSET))

python $AUTOSCIENCE_REPO/analysis/make_rxn_delay_npys.py $1 $reaction_index
