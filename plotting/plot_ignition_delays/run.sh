#!/bin/bash
#SBATCH --job-name=calc_smooth_delays
#SBATCH --partition=short
#SBATCH --time=24:00:00
#SBATCH --constraint=cascadelake


python calculate_smooth_delays.py
