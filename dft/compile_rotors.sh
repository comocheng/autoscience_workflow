#!/bin/bash
#SBATCH --partition=preempt
#SBATCH --time=00:00:10
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL

python $AUTOSCIENCE_REPO/dft/compile_rotors.py $1 $2

