#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=shared
#SBATCH --time=48:00:00
#SBATCH --ntasks-per-node=16
#SBATCH --export=ALL
#SBATCH --account=nrt112
#SBATCH --mem-per-cpu=7G
#SBATCH --nodes=1
#SBATCH --array={array}

module load gaussian/g16
source /shared/centos7/gaussian/g16/bsd/g16.profile

cd {rotor_dir}
RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
fname="rotor_$RUN_i.com"

g16 $fname
