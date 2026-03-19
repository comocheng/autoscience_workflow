#!/bin/bash
#SBATCH --time=01:00:00
#SBATCh --partition=sharing,short,west
#SBATCH --job-name=single_point_ts

python $AUTOSCIENCE_REPO/dft/run_single_point_ts.py $1 $2
