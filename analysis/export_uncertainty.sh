#!/bin/bash
#SBATCH --time=01:00:00

python $AUTOSCIENCE_REPO/analysis/export_uncertainty.py $1
