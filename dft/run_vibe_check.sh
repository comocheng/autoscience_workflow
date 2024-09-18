#!/bin/bash
#SBATCH --partition=express,short,west
#SBATCH --time=00:00:04

python $AUTOSCIENCE_REPO/dft/run_vibe_check.py $1

