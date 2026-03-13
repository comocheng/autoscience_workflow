#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --partition=west,short
#SBATCH --mem=20Gb
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=16
#SBATCH --array={array}


export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch
mkdir -p $GAUSS_SCRDIR
module load gaussian/g16
source /shared/EL9/explorer/gaussian/g16-avx2-gpu/g16/bsd/g16.profile

RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
fname="rotor_$RUN_i.com"

g16 $fname
