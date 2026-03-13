#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=west,short
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=7G
#SBATCH --nodes=1
#SBATCH --array={array}

module load gaussian/g16
source /shared/EL9/explorer/gaussian/g16-avx2-gpu/g16/bsd/g16.profile

RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
fname="rotor_$RUN_i.com"

g16 $fname
