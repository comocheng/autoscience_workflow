#!/bin/bash
#SBATCH --time=48:00:00

python $AUTOSCIENCE_REPO/dft/run_ts_rotors.py $1
