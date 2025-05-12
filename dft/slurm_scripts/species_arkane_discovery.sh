#!/bin/bash
#SBATCH --partition=express,short,west
#SBATCH --time=00:20:00

python ~/rmg/RMG-Py/Arkane.py input.py

