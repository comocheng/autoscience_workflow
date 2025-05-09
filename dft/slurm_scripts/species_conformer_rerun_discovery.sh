#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --partition=short
#SBATCH --constrain=cascadelake
#SBATCH --mem=20Gb
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=32
#SBATCH --array={array}


export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch
mkdir -p $GAUSS_SCRDIR
module load gaussian/g16
source /shared/centos7/gaussian/g16/bsd/g16.profile

RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
fname="conformer_$RUN_i.com"

g16 $fname
