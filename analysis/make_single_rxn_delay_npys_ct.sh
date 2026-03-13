#!/bin/bash
#SBATCH --job-name=delay7
#SBATCH --time=4:00:00
#SBATCH --partition=short,west
#SBATCH --array=0-999%20


OFFSET=0
# OFFSET=1000
# OFFSET=2000
# OFFSET=3000
# OFFSET=4000
# OFFSET=5000
# OFFSET=6000


reaction_index=$(($SLURM_ARRAY_TASK_ID + $OFFSET))

python $AUTOSCIENCE_REPO/analysis/make_single_rxn_delay_npys_ct.py $1 $reaction_index
