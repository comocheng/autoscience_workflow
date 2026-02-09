#!/bin/bash
#SBATCH --partition=short,sharing,west
#SBATCH --time=00:20:00

python ~/rmg/RMG-Py/Arkane.py input.py

