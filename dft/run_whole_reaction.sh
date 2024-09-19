#!/bin/bash
#SBATCH --time=24:00:00

python $AUTOSCIENCE_REPO/dft/run_whole_reaction.py $1
