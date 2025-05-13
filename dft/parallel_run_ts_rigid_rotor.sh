#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL

python $AUTOSCIENCE_REPO/dft/parallel_run_ts_rigid_rotor.py $1
