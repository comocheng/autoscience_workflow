#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=26
#SBATCH --partition=short,west,sharing

python $AUTOSCIENCE_REPO/analysis/get_base_delays.py $1
