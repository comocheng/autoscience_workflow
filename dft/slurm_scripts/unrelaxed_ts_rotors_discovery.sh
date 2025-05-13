#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=short,west
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=7G
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --array=0-21%5

module load gaussian/g16
source /shared/centos7/gaussian/g16/bsd/g16.profile

cd {rotor_dir}
RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
fname="rotor_{rotor_index}_$RUN_i.com"

g16 $fname
