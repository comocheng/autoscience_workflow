#!/bin/bash
#SBATCH --job-name=delay7
#SBATCH --time=12:00:00
#SBATCH --partition=short
#SBATCH --array=0-400%10

# the upper limit of the array * REACTIONS_PER_FILE should be sized to the number of reactions.
# for example, if there are 3481 reactions, and 10 REACTIONS_PER_FILE do ~350 tasks

# cpus-per-task is also sized such that the array of 51 temperatures can be done in two cycles

# pass this in make_rxn_delay_npys.py
REACTIONS_PER_FILE=10
start_index=$(($SLURM_ARRAY_TASK_ID * $REACTIONS_PER_FILE))

python $AUTOSCIENCE_REPO/analysis/make_rxn_delay_npys_ct.py $1 7 $start_index $REACTIONS_PER_FILE
