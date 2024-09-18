#!/bin/bash
#SBATCH --time=24:00:00

python $AUTOSCIENCE_REPO/analysis/run_analysis.py $1
