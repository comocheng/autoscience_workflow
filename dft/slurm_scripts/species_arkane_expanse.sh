#!/bin/bash
#SBATCH --partition=preempt
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --export=ALL
#SBATCH --account=nrt112
#SBATCH --ntasks-per-node=8


python ~/rmg/RMG-Py/Arkane.py input.py

