#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --partition=express,short,west


python $AUTOSCIENCE_REPO/dft/make_rotor_rerun_script.py $1
