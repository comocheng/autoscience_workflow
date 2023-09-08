# script to automatically run reaction calculations based on what's in the yaml
# The way this will work is that it will check every hour to see if there are fewer than 50 jobs running.
# If there are fewer than 50, it will spawn 5 new reaction calculations based on what's in the top_calculations yaml


import os
import sys
import time
import yaml
import datetime
import subprocess
sys.path.append('/work/westgroup/harris.se/autoscience/reaction_calculator/dft/')
import autotst_wrapper

N_CALCULATIONS_TO_SPAWN = 5
MAX_JOBS_RUNNING = 50
try:
    DFT_DIR = os.environ['DFT_DIR']
except KeyError:
    DFT_DIR = '/work/westgroup/harris.se/autoscience/reaction_calculator/dft'

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
# open the yaml file to see what's left to calculate
try:
    calculation_list_file = sys.argv[1]
except IndexError:
    calculation_list_file = os.path.join(autotst_wrapper.DFT_DIR, 'top_calculations.yaml')

while True:  # this will just run until the job gets deleted or it runs out of things to calculate

    # count how many jobs are currently running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(5.0 * 60.0)  # check every 5 minutes?
        jobs_running = job_manager.count_slurm_jobs()

    # spawn N_CALCULATIONS_TO_SPAWN
    calculations_spawned = 0
    i = 0
    while calculations_spawned < N_CALCULATIONS_TO_SPAWN:
        if i > len(top_calculations):
            printlog('RAN OUT OF THINGS TO CALCULATE. QUITTING...')
            exit(0)

        with open(calculation_list_file, 'r') as f:
            top_calculations = yaml.safe_load(f)

        idx = top_calculations[i]['index']

        # Manual skip
        try:
            if top_calculations[i]['skip']:
                printlog(f'Skipping MANUAL {top_calculations[i]["type"]} {idx} {top_calculations[i]["name"]}')
                i += 1
                continue
        except KeyError:
            pass

        # skip because we've already tried this one and it didn't go well
        try:
            if top_calculations[i]['failed']:
                printlog(f'Skipping FAILED {top_calculations[i]["type"]} {idx} {top_calculations[i]["name"]}')
                i += 1
                continue
        except KeyError:
            pass

        # Check if already complete
        try:
            if top_calculations[i]['complete']:
                printlog(f'{top_calculations[i]["type"]} {idx} {top_calculations[i]["name"]} already ran. Skipping...')
                with open(calculation_list_file, 'w') as f:
                    yaml.dump(top_calculations, f)
                i += 1
                continue
        except KeyError:
            top_calculations[i]['complete'] = False

        # -------------------------- Calculate Species ----------------------------- #
        if top_calculations[i]['type'] == 'species':
            printlog(f'Calculating species {idx}: {top_calculations[i]["name"]}')

            if autotst_wrapper.arkane_species_complete(idx):
                print(f'Species {idx} {top_calculations[i]["name"]} already ran')
                top_calculations[i]['complete'] = True
                with open(calculation_list_file, 'w') as f:
                    yaml.dump(top_calculations, f)
                i += 1
                continue

            # skip because we've already tried this one and it didn't go well
            calc_name = f'species {idx}'
            if calc_name in previous_attempts:
                printlog(f'Skipping PREVIOUSLY ATTEMPTED {top_calculations[i]["type"]} {idx} {top_calculations[i]["name"]}')
                printlog(f'Marking failed')
                
                top_calculations[i]['failed'] = True
                with open(calculation_list_file, 'w') as f:
                    yaml.dump(top_calculations, f)

                i += 1
                continue

            # use subprocess to run the species script
            subprocess.run(['python', os.path.join(DFT_DIR, 'run_species.sh'), idx])
            calculations_spawned += 1
            i += 1
            previous_attempts.append(calc_name)

        # ------------------------- Calculate Reaction ----------------------------- #
        elif top_calculations[i]['type'] == 'reaction':
            printlog(f'Calculating reaction {idx}: {top_calculations[i]["name"]}')
            # raise NotImplementedError

            # Skip if family isn't in AutoTST:
            try:
                if top_calculations[i]['family'].lower() not in autotst_familes:
                    print(f'Reaction {idx} {top_calculations[i]["name"]} is family {top_calculations[i]["family"]} which is not in AutoTST. Skipping...')
                    top_calculations[i]['skip'] = True
                    i += 1
                    continue
            except KeyError:
                pass

            if autotst_wrapper.arkane_reaction_complete(idx):
                print(f'Reaction {idx} {top_calculations[i]["name"]} already ran')
                top_calculations[i]['complete'] = True
                with open(calculation_list_file, 'w') as f:
                    yaml.dump(top_calculations, f)
                i += 1
                continue


            # make sure that index isn't currently running:
            if check_index_running(idx):
                # run something else while we wait for this to finish
                i += 1
                continue

            # get status from grep of logfiles
            cmd = f'grep -l Normal {DFT_DIR}/kinetics/reaction_{idx:06}/shell/*_*.log'
            my_shells = subprocess.run(cmd, capture_output=True, shell=True)
            shell_results = my_shells.stdout.decode('utf-8').split()

            cmd = f'grep -l Normal {DFT_DIR}/kinetics/reaction_{idx:06}/center/*_*.log'
            my_shells = subprocess.run(cmd, capture_output=True, shell=True)
            center_results = my_shells.stdout.decode('utf-8').split()

            cmd = f'grep -l Normal {DFT_DIR}/kinetics/reaction_{idx:06}/overall/*_*.log'
            my_shells = subprocess.run(cmd, capture_output=True, shell=True)
            overall_results = my_shells.stdout.decode('utf-8').split()

            # ------------------------------- Run Shell ------------------------------- #
            if not shell_results:
                # SKIP if we already tried this
                calc_name = f'reaction {idx} shell'
                if calc_name in previous_attempts:
                    printlog(f'Skipping PREVIOUSLY ATTEMPTED {top_calculations[i]["type"]} {idx} shell {top_calculations[i]["name"]}')
                    printlog(f'Marking failed')
                    
                    top_calculations[i]['failed'] = True
                    with open(calculation_list_file, 'w') as f:
                        yaml.dump(top_calculations, f)

                    i += 1
                    continue

                subprocess.run(['python', os.path.join(DFT_DIR, 'run_shell6.sh'), idx])
                calculations_spawned += 1
                i += 1
                previous_attempts.append(calc_name)

            # ------------------------------- Run Center ------------------------------- #
            elif not center_results:          
                # SKIP if we already tried this
                calc_name = f'reaction {idx} center'
                if calc_name in previous_attempts:
                    printlog(f'Skipping PREVIOUSLY ATTEMPTED {top_calculations[i]["type"]} {idx} center {top_calculations[i]["name"]}')
                    printlog(f'Marking failed')
                    
                    top_calculations[i]['failed'] = True
                    with open(calculation_list_file, 'w') as f:
                        yaml.dump(top_calculations, f)

                    i += 1
                    continue

                subprocess.run(['python', os.path.join(DFT_DIR, 'run_center6.sh'), idx])
                calculations_spawned += 1
                i += 1
                previous_attempts.append(calc_name)
            # ------------------------------- Run Overall ------------------------------- #
            elif not overall_results:          
                # SKIP if we already tried this
                calc_name = f'reaction {idx} overall'
                if calc_name in previous_attempts:
                    printlog(f'Skipping PREVIOUSLY ATTEMPTED {top_calculations[i]["type"]} {idx} overall {top_calculations[i]["name"]}')
                    printlog(f'Marking failed')
                    
                    top_calculations[i]['failed'] = True
                    with open(calculation_list_file, 'w') as f:
                        yaml.dump(top_calculations, f)

                    i += 1
                    continue

                subprocess.run(['python', os.path.join(DFT_DIR, 'run_overall6.sh'), idx])
                calculations_spawned += 1
                i += 1
                previous_attempts.append(calc_name)

            # ------------------------------ Run Arkane ---------------------------------- #
            else:
                autotst_wrapper.setup_arkane_reaction(idx, force_valid_ts=False)
                autotst_wrapper.run_arkane_reaction(idx)
                printlog(f'Completed reaction {idx} {top_calculations[i]["name"]}')
                top_calculations[i]['complete'] = True
                with open(calculation_list_file, 'w') as f:
                    yaml.dump(top_calculations, f)

            # wait an hour before attempting to spawn more jobs
            printlog(f'Waiting for jobs to get on the queue')
                time.sleep(60.0 * 60.0)
