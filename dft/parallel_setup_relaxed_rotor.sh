#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --partition=sharing,west,short


python $AUTOSCIENCE_REPO/dft/parallel_setup_relaxed_rotor.py $1
