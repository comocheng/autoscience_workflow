#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --partition=short
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --ntasks=24

export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch
mkdir -p $GAUSS_SCRDIR
module load gaussian/g16
source /shared/EL9/explorer/gaussian/g16-avx2-gpu/g16/bsd/g16.profile


g16 freq.com

