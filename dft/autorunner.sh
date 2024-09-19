#!/bin/bash
#SBATCH --job-name=AUTORUNNER
#SBATCH --time=24:00:00
#SBATCH --partition=short

# argument is mech_summary.csv file with list of stuff to compute
python $AUTOSCIENCE_REPO/dft/autorunner.py $1

