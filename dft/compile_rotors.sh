#!/bin/bash
#SBATCH --partition=short
#SBATCH --time=00:00:04

python $AUTOSCIENCE_REPO/dft/compile_rotors.py $1 $2

