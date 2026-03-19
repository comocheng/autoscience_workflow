#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=west,short,sharing
#SBATCH --job-name=freq_ts

export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch
mkdir -p $GAUSS_SCRDIR
module load gaussian/g16
source /shared/EL9/explorer/gaussian/g16-avx2-gpu/g16/bsd/g16.profile


python $AUTOSCIENCE_REPO/dft/run_freq_ts.py $1
