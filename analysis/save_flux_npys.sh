#!/bin/bash
#SBATCH --job-name=base_delays
#SBATCH --mem=20Gb
#SBATCH --partition=short,west,sharing
#SBATCH --time=1:00:00
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1

python $AUTOSCIENCE_REPO/analysis/save_flux_npys.py $1

