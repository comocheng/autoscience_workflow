#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=preempt
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL


python $AUTOSCIENCE_REPO/dft/run_reaction_arkane.py $1 $2
# python-jl $AUTOSCIENCE_REPO/dft/run_reaction_arkane.py $1 $2
