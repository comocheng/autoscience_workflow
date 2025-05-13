#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=7G
#SBATCH --nodes=1
#SBATCH --export=ALL
#SBATCH --partition=shared
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --account=nrt112
#SBATCH --array=0-21


module reset
module unload cpu/0.17.3b
module load cpu/0.15.4
module load gaussian/16.C.01
exe=`which g16`
export GAUSS_SCRDIR=/scratch/$USER/job_$SLURM_JOBID

cd {rotor_dir}

RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))
in_fname="rotor_{rotor_index}_$RUN_i.com"
out_fname="rotor_{rotor_index}_$RUN_i.log"

bash /cm/shared/examples/sdsc/gaussian/cpu/getcpusets $$
cat $$.out $in_fname >file.tmp.$$
/usr/bin/time $exe < file.tmp.$$ > $out_fname
rm -f $$.out file.tmp.$$
