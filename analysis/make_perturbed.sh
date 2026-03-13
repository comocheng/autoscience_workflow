#!/bin/bash
#SBATCH --job-name=make_perturbed
#SBATCH --time=00:30:00
#SBATCH --partition=express,short,west


python $AUTOSCIENCE_REPO/analysis/make_perturbed.py $1
