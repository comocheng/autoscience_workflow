#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --export=ALL
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50Gb
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=32
#SBATCH --array={array}


module reset
module unload cpu/0.17.3b
module load cpu/0.15.4
module load gaussian/16.C.01
exe=`which g16`
export GAUSS_SCRDIR=/scratch/$USER/job_$SLURM_JOBID

RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
fname="conformer_$RUN_i.com"

bash /cm/shared/examples/sdsc/gaussian/cpu/getcpusets $$
cat $$.out $fname >file.tmp.$$
/usr/bin/time $exe < file.tmp.$$ > $fname.out
rm -f $$.out file.tmp.$$
