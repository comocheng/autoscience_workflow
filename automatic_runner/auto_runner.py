# script to automatically run reaction calculations based on what's in the yaml
# The way this will work is that it will check every hour to see if there are fewer than 50 jobs running.
# If there are fewer than 50, it will spawn 5 new reaction calculations based on what's in the top_calculations yaml


import os
import sys
import time
import yaml
import datetime
sys.path.append('/work/westgroup/harris.se/autoscience/reaction_calculator/dft/')
import autotst_wrapper

N_REACTION_CALCULATIONS_TO_SPAWN = 5

previous_attempts = []  # store what has already been tried so we can move on (and mark failed status) if things are failing

def printlog(text):
    print(f'{datetime.datetime.now()}\t{text}')
    with open(os.path.join(os.path.dirname(__file__), 'automated_runner.log'), 'a') as f:
        f.write(f'{datetime.datetime.now()}\t{text}\n')


autotst_familes = ['disproportionation', 'intra_h_migration', 'h_abstraction', 'r_addition_multiple_bond']
printlog('Starting Automated Runner')
# open the yaml file to see what's left to calculate
try:
    calculation_list_file = sys.argv[1]
except IndexError:
    calculation_list_file = os.path.join(autotst_wrapper.DFT_DIR, 'top_calculations.yaml')

with open(calculation_list_file, 'r') as f:
    top_calculations = yaml.safe_load(f)

# top_calculations is a list of dicts
for i in range(len(top_calculations)):
    idx = top_calculations[i]['index']

    # Manual skip
    try:
        if top_calculations[i]['skip']:
            printlog(f'Skipping {top_calculations[i]["type"]} {idx} {top_calculations[i]["name"]}')
            continue
    except KeyError:
        pass

    # Check if already complete
    try:
        if top_calculations[i]['complete']:
            printlog(f'{top_calculations[i]["type"]} {idx} {top_calculations[i]["name"]} already ran. Skipping...')
            with open(calculation_list_file, 'w') as f:
                yaml.dump(top_calculations, f)
            continue
    except KeyError:
        top_calculations[i]['complete'] = False

    if top_calculations[i]['type'] == 'species':
        printlog(f'Calculating species {idx}: {top_calculations[i]["name"]}')

        if autotst_wrapper.arkane_species_complete(idx):
            print(f'Species {idx} {top_calculations[i]["name"]} already ran')
            top_calculations[i]['complete'] = True
            with open(calculation_list_file, 'w') as f:
                yaml.dump(top_calculations, f)
            continue

        autotst_wrapper.screen_species_conformers(idx)
        autotst_wrapper.optimize_conformers(idx)
        autotst_wrapper.setup_arkane_species(idx)
        autotst_wrapper.run_arkane_species(idx)

        # wait for species completion
        printlog(f'Waiting for species {idx} {top_calculations[i]["name"]} completion')
        while not autotst_wrapper.arkane_species_complete(idx):
            time.sleep(60.0)

        printlog(f'Completed species {idx} {top_calculations[i]["name"]}')
        top_calculations[i]['complete'] = True
        with open(calculation_list_file, 'w') as f:
            yaml.dump(top_calculations, f)

    elif top_calculations[i]['type'] == 'reaction':
        printlog(f'Calculating reaction {idx}: {top_calculations[i]["name"]}')
        # raise NotImplementedError

        # Skip if family isn't in AutoTST:
        try:
            if top_calculations[i]['family'].lower() not in autotst_familes:
                print(f'Reaction {idx} {top_calculations[i]["name"]} is family {top_calculations[i]["family"]} which is not in AutoTST. Skipping...')
                top_calculations[i]['skip'] = True
                continue
        except KeyError:
            pass

        if autotst_wrapper.arkane_reaction_complete(idx):
            print(f'Reaction {idx} {top_calculations[i]["name"]} already ran')
            top_calculations[i]['complete'] = True
            with open(calculation_list_file, 'w') as f:
                yaml.dump(top_calculations, f)
            continue

        autotst_wrapper.setup_opt(idx, 'shell')
        autotst_wrapper.run_opt(idx, 'shell')
        autotst_wrapper.setup_opt(idx, 'center')
        autotst_wrapper.run_opt(idx, 'center')
        autotst_wrapper.setup_opt(idx, 'overall')
        autotst_wrapper.run_opt(idx, 'overall')
        # autotst_wrapper.setup_arkane_reaction(idx, force_valid_ts=force_valid_ts)
        autotst_wrapper.setup_arkane_reaction(idx, force_valid_ts=False)
        autotst_wrapper.run_arkane_reaction(idx)

        # TODO wait more sanely for completion?
        printlog(f'Waiting for reaction {idx} {top_calculations[i]["name"]} completion')
        while not autotst_wrapper.arkane_reaction_complete(idx):
            time.sleep(60.0)

        printlog(f'Completed reaction {idx} {top_calculations[i]["name"]}')
        top_calculations[i]['complete'] = True
        with open(calculation_list_file, 'w') as f:
            yaml.dump(top_calculations, f)
