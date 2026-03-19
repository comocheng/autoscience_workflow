#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --partition=west,sharing,short
#SBATCH --job-name=single_point

python $AUTOSCIENCE_REPO/dft/run_single_point.py $1 $2
