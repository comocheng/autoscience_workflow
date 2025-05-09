#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --export=ALL
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=16
#SBATCH --array={array}


module reset
module unload cpu/0.17.3b
module load cpu/0.15.4
module load gaussian/16.C.01
exe=`which g16`
export GAUSS_SCRDIR=/scratch/$USER/job_$SLURM_JOBID

RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
in_fname="fwd_ts_$RUN_i.com"
out_fname="fwd_ts_$RUN_i.log"

bash /cm/shared/examples/sdsc/gaussian/cpu/getcpusets $$
cat $$.out $in_fname >file.tmp.$$
/usr/bin/time $exe < file.tmp.$$ > $out_fname
rm -f $$.out file.tmp.$$
