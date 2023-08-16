#!/bin/bash
#SBATCH --time=00:20:00
#SBATCH --partition=express,short,west

python /work/westgroup/harris.se/autoscience/reaction_calculator/dft/run_species_arkane.py $1

