#!/bin/bash
#SBATCH --job-name=delay7
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=26
#SBATCH --array=0-350

# the upper limit of the array * REACTIONS_PER_FILE should be sized to the number of reactions.
# for example, if there are 3481 reactions, and 10 REACTIONS_PER_FILE do ~350 tasks

# cpus-per-task is also sized such that the array of 51 temperatures can be done in two cycles

# pass this in make_rxn_delay_npys.py
REACTIONS_PER_FILE=10
start_index=$(($SLURM_ARRAY_TASK_ID * $REACTIONS_PER_FILE))

python $AUTOSCIENCE_REPO/analysis/dib_make_rxn_delay_npys.py $1 24 $start_index $REACTIONS_PER_FILE
