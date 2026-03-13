#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --time=2:00:00
#SBATCH --cpus-per-task=26

python $AUTOSCIENCE_REPO/analysis/get_delays_at_experiment.py $1
