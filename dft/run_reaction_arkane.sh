#!/bin/bash
#SBATCH --time=01:00:00

python $AUTOSCIENCE_REPO/dft/run_reaction_arkane.py $1 $2
# python-jl $AUTOSCIENCE_REPO/dft/run_reaction_arkane.py $1 $2
