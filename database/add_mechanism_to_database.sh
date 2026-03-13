#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --partition=sharing,west,short

python /projects/westgroup/harris.se/autoscience/reaction_calculator/database/add_mechanism_to_database.py $1
