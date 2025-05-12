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


module reset
module unload cpu/0.17.3b
module load cpu/0.15.4
module load gaussian/16.C.01
exe=`which g16`
export GAUSS_SCRDIR=/scratch/$USER/job_$SLURM_JOBID

RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
in_fname="rotor_$RUN_i.com"
out_fname="rotor_$RUN_i.log"

bash /cm/shared/examples/sdsc/gaussian/cpu/getcpusets $$
cat $$.out $in_fname >file.tmp.$$
/usr/bin/time $exe < file.tmp.$$ > $out_fname
rm -f $$.out file.tmp.$$
