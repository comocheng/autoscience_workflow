#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --partition=shared
#SBATCH --account=nrt112
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --ntasks-per-node=16


module reset
module load cpu/0.17.3b
module load gcc/10.2.0/npcyll4
module load openmpi/4.1.1/ygduf2r
module load orca/5.0.4/2nqnnmq

export UCX_NET_DEVICES='mlx5_2:1'
export UCX_MAX_RNDV_RAILS=1
export ORCAEXE=`which orca`

cd {single_point_dir}

$ORCAEXE conformer.inp > conformer.out
