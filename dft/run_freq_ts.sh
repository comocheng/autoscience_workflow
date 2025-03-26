#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --job-name=freq_ts

python $AUTOSCIENCE_REPO/dft/run_freq_ts.py $1
