# script to automatically run reaction calculations based on what's in the mech_summary_DATE.csv
# The way this will work is that it will check every hour to see if there are fewer than 50 jobs running.
# If there are fewer than 50, it will spawn 5 new reaction calculations based on what's
# in the CSV, stopping at the top 10 - the only ones required to run the next RMG run


import os
import sys
import time
import datetime
import subprocess
import pandas as pd
import job_manager

import autotst_wrapper


STOP_AFTER = 20  # only focus on top 10 reactions/species that are possible
N_CALCULATIONS_TO_SPAWN = 5
MAX_JOBS_RUNNING = 50
try:
    DFT_DIR = os.environ['DFT_DIR']
except KeyError:
    DFT_DIR = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'dft')

previous_attempts = []  # store what has already been tried so we can move on (and mark failed status) if things are failing


uname = job_manager.get_user()
print(f'Username: {uname}')


def printlog(text):
    print(f'{datetime.datetime.now()}\t{text}')
    with open(os.path.join(os.path.dirname(__file__), 'automated_runner.log'), 'a') as f:
        f.write(f'{datetime.datetime.now()}\t{text}\n')


def check_index_running(idx):
    # checks the queue to see if a job with that index in the name is already running
    # returns True if already running
    # TODO edit the dependence on trailing "  out?
    myjobs = subprocess.run(['squeue', '--format="%.30j"', '-u', uname], capture_output=True)
    job_names = myjobs.stdout.decode().split()
    job_names = [j for j in job_names if j != '"']
    for j in job_names:
        if f'_{idx}"' in j:
            return True
    return False  # not found, safe to run


autotst_familes = ['disproportionation', 'intra_h_migration', 'h_abstraction', 'r_addition_multiple_bond']
printlog('Starting Automated Runner')


# open the csv file to see what we should calculate. MUST BE PROVIDED AS INPUT
calculation_list_file = sys.argv[1]
mech_summary = pd.read_csv(calculation_list_file, index_col=0)

successful_calculations = 0
possible_index = 0  # for counting which reactions are possible to calculate
while True:
    # count how many jobs are currently running
    # sleep if there's no room for more things to run
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(5.0 * 60.0)  # check every 5 minutes?
        jobs_running = job_manager.count_slurm_jobs()

    # spawn N_CALCULATIONS_TO_SPAWN
    calculations_spawned = 0
    i = 0
    while calculations_spawned < N_CALCULATIONS_TO_SPAWN:
        if possible_index >= STOP_AFTER and successful_calculations < STOP_AFTER:
            printlog(f'Done calculating {STOP_AFTER}. {successful_calculations} successful. Restarting at beginning.')
            successful_calculations = 0
            possible_index = 0
            break
        elif successful_calculations >= STOP_AFTER:
            printlog(f'SUCCESS CALCULATING TOP {STOP_AFTER}. QUITTING...')
            exit(0)

        if i > len(mech_summary):
            printlog('RAN OUT OF THINGS TO CALCULATE. QUITTING...')
            exit(0)

        idx = mech_summary['db_index'].values[i]
        name = mech_summary['reaction'].values[i]
        family = mech_summary['family'].values[i]
        printlog(f'Examining Rank {i}, db index {idx}, type {family}, name {name}')

        # if it is not possible to calculate, move on to the next thing
        if family.lower() not in autotst_familes and family != 'species':
            printlog(f'Skipping incompatible calculation {idx} {family} {name}')
            i += 1
            continue

        # -------------------------- Calculate Species ----------------------------- #
        if family == 'species':
            printlog(f'Calculating species {idx}: {name}')

            if autotst_wrapper.arkane_species_complete(idx):
                print(f'Species {idx}: {name} already ran')
                successful_calculations += 1
                possible_index += 1
                i += 1
                continue

            # use subprocess to run the species script
            subprocess.run(['python', os.path.join(DFT_DIR, 'run_species.sh'), idx])
            calculations_spawned += 1
            i += 1
        # ------------------------- Calculate Reaction ----------------------------- #
        else:
            printlog(f'Calculating reaction {idx}: {name}')

            if autotst_wrapper.arkane_reaction_complete(idx):
                printlog(f'Reaction {idx}: {name} already ran. Skipping...')
                successful_calculations += 1
                possible_index += 1
                i += 1
                continue

            # make sure that index isn't currently running:
            if check_index_running(idx):
                # run something else while we wait for this to finish
                printlog(f'Reaction {idx}: {name} is still running, so move on to something else')
                possible_index += 1
                i += 1
                continue

            # ------------------------------- Run Reaction Calc ------------------------------- #
            printlog(f'Running whole reaction calculation for {idx}: {name}')
            subprocess.run(['sbatch', os.path.join(DFT_DIR, 'run_whole_reaction.sh'), str(idx)])
            # TODO put a job name here in the sbatch command so I can see the reaction number on the queue
            calculations_spawned += 1
            possible_index += 1
            i += 1

    # wait a while before attempting to spawn another set of jobs. This is because the screen
    # conformers phase takes a few minutes and then spawns many jobs
    wait_minutes = 30.0
    printlog(f'Waiting {wait_minutes} minutes for jobs to get on the queue')
    time.sleep(wait_minutes * 60.0)
