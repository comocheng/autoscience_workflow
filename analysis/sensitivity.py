"""A module for running species and reaction sensitivity analyses for ignition delay simulations"""

import os
import logging
import numpy as np
import sys
import cantera as ct
import numpy as np
import simulation
import yaml


def perturb_species(species, DELTA_J_MOL=418.4):
    # takes in a Cantera species and makes a copy with the enthalpy offset changed
    # Default of 418 J/mol equals 0.1 kcal/mol
    R = 8.3144598  # gas constant in J/mol

    # copy the species
    input_data = species.input_data.copy()
    increase = None
    for i in range(len(input_data['thermo']['data'])):
        if not increase:
            # Only define the increase in enthalpy once or you'll end up with numerical gaps in continuity
            increase = DELTA_J_MOL / R
        input_data['thermo']['data'][i][5] += increase
    new_species = ct.Species().from_dict(input_data)
    return new_species


def run_species_sensitivity(gas, species_index, conditions_dict):
    # conditions_dict is a dictionary with keys 'T', 'P', and 'X' for the conditions to run the simulation at. This is used to calculate the sensitivity of the ignition delay to the enthalpy of formation of the given species.
    Ts = conditions_dict['T']
    Ps = conditions_dict['P']
    Xs = conditions_dict['X']

    delays = np.zeros(len(Ts))

    sp_copy = ct.Species().from_dict(gas.species()[species_index].input_data)
    perturbed_species = perturb_species(gas.species()[species_index])
    gas.modify_species(species_index, perturbed_species)

    # After much experience and heartbreak, I have concluded that Cantera runs fastest when you throw as many processors
    # at a single simulation without attempting to parallelize across multiple simulations.
    for i in range(len(Ts)):
        T = Ts[i]
        P = Ps[i]
        X = Xs[i]
        delays[i] = simulation.run_simulation(gas, T, P, X)

    # set the species back to the original so that we can run the next sensitivity simulation
    gas.modify_species(species_index, sp_copy)
    return delays


def run_reaction_sensitivity(gas, reaction_index, conditions_dict):
    # conditions_dict is a dictionary with keys 'T', 'P', and 'X' for the conditions to run the simulation at. This is used to calculate the sensitivity of the ignition delay to the enthalpy of formation of the given species.
    Ts = conditions_dict['T']
    Ps = conditions_dict['P']
    Xs = conditions_dict['X']

    delays = np.zeros(len(Ts))
    gas.set_multiplier(1.1, reaction_index)

    # After much experience and heartbreak, I have concluded that Cantera runs fastest when you throw as many processors
    # at a single simulation without attempting to parallelize across multiple simulations.
    for i in range(len(Ts)):
        T = Ts[i]
        P = Ps[i]
        X = Xs[i]
        delays[i] = simulation.run_simulation(gas, T, P, X)

    # set the species back to the original so that we can run the next sensitivity simulation
    gas.set_multiplier(1.0, reaction_index)
    return delays


# This however we want to map to SLURM_ARRAY_TASK_ID because you can run on separate nodes
def save_species_sensitivity_npy(mech_yaml, species_index, conditions_dict):
    results_dir = os.path.join(os.path.dirname(mech_yaml), 'sensitivity')
    os.makedirs(results_dir, exist_ok=True)

    save_path = os.path.join(results_dir, f'spec_delay_{species_index:04}.npy')
    gas = ct.Solution(mech_yaml)
    conditions_dict = {}  # TODO load from yaml file
    delays = run_species_sensitivity(gas, species_index, conditions_dict)
    np.save(save_path, delays)


# This however we want to map to SLURM_ARRAY_TASK_ID because you can run on separate nodes
def save_reaction_sensitivity_npy(mech_yaml, reaction_index, conditions_dict):
    results_dir = os.path.join(os.path.dirname(mech_yaml), 'sensitivity')
    os.makedirs(results_dir, exist_ok=True)

    save_path = os.path.join(results_dir, f'reaction_delays_{reaction_index:06}.npy')
    gas = ct.Solution(mech_yaml)
    conditions_dict = {}  # TODO load from yaml file
    delays = run_reaction_sensitivity(gas, reaction_index, conditions_dict)
    np.save(save_path, delays)


# option to do them all in serial
def make_all_species_sensitivity_npys(mech_yaml, conditions_dict):
    if isinstance(conditions_dict, str):
        with open(conditions_dict) as f:
            conditions_dict = yaml.safe_load(f)
    results_dir = os.path.join(os.path.dirname(mech_yaml), 'sensitivity')
    gas = ct.Solution(mech_yaml)
    for species_index in range(gas.n_species):
        outfile = os.path.join(results_dir, f'spec_delay_{species_index:04}.npy')
        if os.path.exists(outfile):
            logging.info(f'Skipping species {species_index} because file already exists!')
            continue

        delays = run_species_sensitivity(gas, species_index, conditions_dict)
        np.save(outfile, delays)

def make_all_reaction_sensitivity_npys(mech_yaml, conditions_dict):
    if isinstance(conditions_dict, str):
        with open(conditions_dict) as f:
            conditions_dict = yaml.safe_load(f)
    results_dir = os.path.join(os.path.dirname(mech_yaml), 'sensitivity')
    gas = ct.Solution(mech_yaml)
    for reaction_index in range(gas.n_reactions):
        outfile = os.path.join(results_dir, f'reaction_delays_{reaction_index:06}.npy')
        if os.path.exists(outfile):
            logging.info(f'Skipping reaction {reaction_index} because file already exists!')
            continue

        delays = run_reaction_sensitivity(gas, reaction_index, conditions_dict)
        np.save(outfile, delays)



# if __name__ == '__main__':
#     species_index = int(sys.argv[1])
#     mech_yaml = sys.argv[2]
    


# chemkin = sys.argv[1]
# species_index = int(sys.argv[2])
# aramco = 'aramco' in chemkin.lower()

# working_dir = os.path.join(os.path.dirname(chemkin))
# experimental_table_index = 7  # workflow only requires calculating it here
# table_dir = os.path.join(working_dir, f'table_{experimental_table_index:04}')
# spec_delay_file = os.path.join(table_dir, f'spec_delay_{experimental_table_index:04}_{species_index:04}.npy')
# if os.path.exists(spec_delay_file):
#     print(f'Skipping {species_index} because file already exists!')
#     exit(0)
# os.makedirs(table_dir, exist_ok=True)

# base_yaml_path = os.path.join(working_dir, 'chem_annotated.yaml')
# gas = ct.Solution(base_yaml_path)
# if species_index >= len(gas.species()):
#     print(f'Skipping species {species_index} because not in model')
#     exit(-1)

# # perturb the species
# sp_copy = ct.Species().from_dict(gas.species()[species_index].input_data)
# perturbed_species = perturb_species(gas.species()[species_index])
# gas.modify_species(species_index, perturbed_species)




# # just use the first concentration
# Tmax = 1077  # use min and max temperature range of the data: 663K-1077K
# Tmin = 663
# # N = 51
# temperatures = np.linspace(Tmin, Tmax, N_Temps)

# # Run all simulations serially because Cantera has issues with multiprocessing-- it doesn't actually speed things up
# # https://groups.google.com/g/cantera-users/c/q_eUU6r0j_M/m/26F1IC-qAwAJ
# delays = np.zeros(len(temperatures))
# condition_indices = np.arange(0, len(temperatures))

# for condition_index in condition_indices:
#     print(condition_index)
#     delays[condition_index] = simulation.run_simulation(gas, temperatures[condition_index], P7[0], concentrations[0])

# np.save(spec_delay_file, delays)
