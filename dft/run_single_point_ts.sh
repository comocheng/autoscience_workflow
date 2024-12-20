#!/bin/bash
#SBATCH --time=24:00:00

python $AUTOSCIENCE_REPO/dft/run_single_point_ts.py $1 $2
