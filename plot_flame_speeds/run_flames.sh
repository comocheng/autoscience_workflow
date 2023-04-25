#!/bin/bash
#SBATCH --ntasks=16
#SBATCH --time=24:00:00

python run_flame_speeds.py $1

