#!/bin/bash
#SBATCH --time=00:20:00

export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch
mkdir -p $GAUSS_SCRDIR
module load gaussian/g16
source /shared/EL9/explorer/gaussian/g16-avx2-gpu/g16/bsd/g16.profile

python $AUTOSCIENCE_REPO/dft/parallel_run_ts_rigid_rotor.py $1
