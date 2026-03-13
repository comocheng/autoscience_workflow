#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=26

python $AUTOSCIENCE_REPO/analysis/dib_get_delays_at_experiment.py $1
