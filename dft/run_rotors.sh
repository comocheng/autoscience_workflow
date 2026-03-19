#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=short,sharing,west

python $AUTOSCIENCE_REPO/dft/run_rotors.py $1
