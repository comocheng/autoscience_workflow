# script to save a .npy with base delays for each of the tables across given base conditions
# first argument is chemkin (or cantera) file, second argument is optional path to sim_config.yaml (if not given, will look in same dir as mech file)


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
mech_yaml = chemkin.replace('.inp', '.yaml')
working_dir = os.path.dirname(chemkin)
save_path = mech_yaml.replace('.yaml', '.npy')
gas = ct.Solution(mech_yaml)

conditions_dict_path = os.path.join(working_dir, 'sim_config.yaml')
# conditions_dict_path = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'experiment', 'butane1.yaml')
if not os.path.exists(conditions_dict_path):
    logging.warning(f'Expected to find sim_config.yaml at {conditions_dict_path} but it does not exist. Please copy it to the directory with your mech file.')
    raise FileNotFoundError(f'sim_config.yaml not found at {conditions_dict_path}')

with open(conditions_dict_path) as f:
    conditions_dict = yaml.safe_load(f)

condition_list = conditions_dict['experiment_points']
delays = np.zeros(len(condition_list))
for i, condition in enumerate(condition_list):
    T = condition['T']
    P = condition['P']
    X = condition['X']
    delays[i] = simulation.run_simulation_for_delay(gas, T, P, X)

np.save(save_path, delays)
