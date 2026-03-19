#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --error=error.log
#SBATCH --nodes=1
#SBATCH --partition=short,west
#SBATCH --mem=200Gb
#SBATCH --time=8:00:00
#SBATCH --ntasks=16


ompi=/projects/westgroup/orca/openmpi-4.1.6/build
PATH=$ompi/bin:$PATH
LD_LIBRARY_PATH=$ompi/lib:$ompi/etc:$LD_LIBRARY_PATH

#Orca
orcadir=/projects/westgroup/orca/orca_6_0_1_linux_x86-64_shared_openmpi416
export PATH=$PATH:$orcadir
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$orcadir


cd {single_point_dir}

$orcadir/orca conformer.inp > conformer.out

    
