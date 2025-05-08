#!/bin/bash
#SBATCH --time=48:00:00

python $AUTOSCIENCE_REPO/dft/parallel_run_ts_rigid_rotor.py $1
