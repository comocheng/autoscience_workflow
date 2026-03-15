# script to run one sensitivity point and save a .npy with the delay

import os
import sys
import yaml
import cantera as ct
import numpy as np
import simulation
import logging


logging.basicConfig(level=logging.INFO)


# load chemkin file and assume a certain directory structure to get the yaml file and the experimental conditions
chemkin = sys.argv[1]
species_index = int(sys.argv[2])

mech_yaml = chemkin.replace('.inp', '.yaml')
if os.path.basename(mech_yaml) != 'chem_annotated.yaml':
    logging.warning(f'Expected mech yaml to be named chem_annotated.yaml but got {mech_yaml}. Proceed with caution!')

working_dir = os.path.dirname(chemkin)
results_dir = os.path.join(working_dir, 'sensitivity')
os.makedirs(results_dir, exist_ok=True)

save_path = os.path.join(results_dir, f'spec_delay_{species_index:04}.npy')
if os.path.exists(save_path):
    logging.info(f'Skipping species {species_index} because file already exists!')
    exit(0)


conditions_dict_path = os.path.join(working_dir, 'sim_config.yaml')
# conditions_dict_path = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'experiment', 'butane1.yaml')
if not os.path.exists(conditions_dict_path):
    logging.warning(f'Expected to find sim_config.yaml at {conditions_dict_path} but it does not exist. Please copy it to the directory with your mech file.')
    raise FileNotFoundError(f'sim_config.yaml not found at {conditions_dict_path}')

with open(conditions_dict_path) as f:
    conditions_dict = yaml.safe_load(f)

gas = ct.Solution(mech_yaml)
if species_index > gas.n_species:
    logging.warning(f'Species index greater than model size: {gas.n_species} species')
    exit(-1)

# modify the gas object to do sensitivity - does not get reset because it's one species at a time
perturbed_species = simulation.perturb_species(gas.species()[species_index])
gas.modify_species(species_index, perturbed_species)

condition_list = conditions_dict['sensitivity_points']
delays = np.zeros(len(condition_list))
for i, condition in enumerate(condition_list):
    T = condition['T']
    P = condition['P']
    X = condition['X']
    delays[i] = simulation.run_simulation_for_delay(gas, T, P, X, t_end=10.0)
np.save(save_path, delays)
