#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=16
#SBATCH --array=0-21

export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch
module load gaussian/g16
source /shared/centos7/gaussian/g16/bsd/g16.profile

python $AUTOSCIENCE_REPO/dft/parallel_run_ts_rigid_rotor.py $1 $2 $SLURM_ARRAY_TASK_ID
