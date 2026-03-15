# scipt to export improvement score ranking to mech_summary.csv
# takes chem_annotated.inp as input, expects species_dictionary, sensitivity and uncertainty files in same directory

# script to save the rankings for the mechanism
import os
import re
import sys
import glob
import copy
import logging
import yaml
import pickle
import subprocess
import numpy as np
import pandas as pd

import rmgpy.data.kinetics
import rmgpy.chemkin
import cantera as ct


sys.path.append(os.environ['DATABASE_DIR'])
import database_fun


chemkin_file = sys.argv[1]
if os.path.isdir(chemkin_file):
    working_dir = chemkin_file
    chemkin_file = os.path.join(working_dir, 'chem_annotated.inp')
else:
    working_dir = os.path.dirname(chemkin_file)


# ------------------------------ Load Files ----------------------------------
# Load mechanism
dictionary = os.path.join(working_dir, 'species_dictionary.txt')
cantera_file = os.path.join(working_dir, 'chem_annotated.yaml')
analysis_dir = os.path.join(working_dir, 'analysis')
os.makedirs(analysis_dir, exist_ok=True)

species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(input_chemkin, dictionary_path=dictionary, use_chemkin_names=True)

gas = ct.Solution(cantera_file)

# This cti -> rmg converter dictionary can be made using rmg_tools/ct2rmg_dict.py
RMG_TOOLS_DIR = '/home/harris.se/rmg/rmg_tools'
if not os.path.exists(os.path.join(working_dir, 'ct2rmg_rxn.pickle')):
    print('Creating ct2rmg pickle')
    subprocess.run(['python', os.path.join(RMG_TOOLS_DIR, 'ct2rmg_dict.py'), input_chemkin])

with open(os.path.join(working_dir, 'ct2rmg_rxn.pickle'), 'rb') as handle:
    ct2rmg_rxn = pickle.load(handle)
    

print(f'{len(species_list)} species loaded')
print(f'{len(reaction_list)} reactions loaded')


# load base and perturbed delays and check size
base_delays = np.load(os.path.join(working_dir, 'base_delays.npy'))
base_delays = np.array(np.repeat(np.matrix(base_delays), gas.n_species + gas.n_reactions, axis=0))
total_delays = np.load(os.path.join(working_dir, 'total_perturbed_mech_delays.npy'))

# check the size
conditions_dict_path = os.path.join(working_dir, 'sim_config.yaml')
if not os.path.exists(conditions_dict_path):
    logging.warning(f'Expected to find sim_config.yaml at {conditions_dict_path} but it does not exist. Please copy it to the directory with your mech file.')
    raise FileNotFoundError(f'sim_config.yaml not found at {conditions_dict_path}')

with open(conditions_dict_path) as f:
    conditions_dict = yaml.safe_load(f)
K = len(conditions_dict['sensitivity_points'])

assert total_delays.shape[0] == gas.n_species + gas.n_reactions
assert total_delays.shape[1] == K

N = gas.n_species
M = gas.n_reactions


rxn_uncertainty_file = os.path.join(working_dir, 'gao_reaction_uncertainty.npy')
sp_uncertainty_file = os.path.join(working_dir, 'gao_species_uncertainty.npy')

rmg_rxn_uncertainty = np.load(rxn_uncertainty_file)
rmg_sp_uncertainty = np.load(sp_uncertainty_file)

assert len(rmg_rxn_uncertainty) == len(reaction_list)
assert len(rmg_sp_uncertainty) == len(species_list)


rxn_uncertainty = np.zeros(gas.n_reactions)
for ct_index in range(len(rxn_uncertainty)):
    rxn_uncertainty[ct_index] = rmg_rxn_uncertainty[ct2rmg_rxn[ct_index]]

# Cantera species should be in same rmg order, but this makes sure for us
for i in range(len(species_list)):
    if str(species_list[i]) != gas.species_names[i]:
        print(i)
    assert str(species_list[i]) == gas.species_names[i]

sp_uncertainty = rmg_sp_uncertainty

total_uncertainty_array = np.concatenate((sp_uncertainty, rxn_uncertainty), axis=0)
total_uncertainty_mat = np.array(np.repeat(np.transpose(np.matrix(total_uncertainty_array)), K, axis=1))


# -------------------------- Compute Uncertainty --------------------------
SPECIES_DFT_ERROR = 1.5
REACTION_DFT_ERROR = 1 / np.sqrt(3) * np.log(10)

sp_dft_uncertainty_mat = np.ones((N, K)) * SPECIES_DFT_ERROR
rxn_dft_uncertainty_mat = np.ones((M, K)) * REACTION_DFT_ERROR
dft_uncertainty_mat = np.concatenate((sp_dft_uncertainty_mat, rxn_dft_uncertainty_mat), axis=0)


reaction_indices = np.arange(0, len(gas.reactions()))
reaction_uncertainty_order = [x for _,x in sorted(zip(rxn_uncertainty, reaction_indices))][::-1]


print('Top Uncertain Reactions')
print('i\tDelta\tReaction\tSensitivity\tImprovement Score')
for i in range(0, 10):
    ct_index = reaction_uncertainty_order[i]
    print(ct_index, '\t', np.round(rxn_uncertainty[ct_index], 3),
          '\t', gas.reactions()[ct_index], 
          '\t', reaction_list[ct2rmg_rxn[ct_index]].family)

# ---------------------- Compute Sensitivity ---------------------------
assert total_delays.shape == base_delays.shape
total_delays[total_delays == 0] = np.nan

d_ln_tau = np.log(total_delays) - np.log(base_delays)
avg_d_ln_tau = np.nanmean(d_ln_tau, axis = 1)
avg_d_ln_tau[np.isnan(avg_d_ln_tau)] = -np.inf


delta_G_kcal_mol = np.zeros((N, K)) + 0.1

# we know that by definition, this is 0.1
delta_ln_k = 0.1 * np.ones((M, K))

# concatenate into a big delta matrix
delta = np.concatenate((delta_G_kcal_mol, delta_ln_k), axis=0)

# first derivative is change in delay / change in G
first_derivative = np.divide(d_ln_tau, delta)

avg_first_derivative = np.nanmean(first_derivative, axis=1)

abs_avg_first_derivative = np.abs(avg_first_derivative)
abs_avg_first_derivative[np.isnan(abs_avg_first_derivative)] = -np.inf


parameter_indices = np.arange(0, N + M)
reaction_sensitivity_order = [x for _, x in sorted(zip(abs_avg_first_derivative, parameter_indices))][::-1]

print('Top Sensitive Parameters')
print('i\tct idx\tSensitivity\tParameter')
for i in range(0, 20):
    ct_index = reaction_sensitivity_order[i]
    if ct_index < N:
        print(i, '\t', ct_index, '\t', np.round(abs_avg_first_derivative[ct_index], 9),
              '\t', gas.species()[ct_index], )
    else:
        print(i, '\t', ct_index, '\t', np.round(abs_avg_first_derivative[ct_index], 9),
              '\t', gas.reactions()[ct_index - N])


# ---------------------------- Compute Improvement Score ----------------------------
delta_uncertainty_squared = np.float_power(total_uncertainty_mat, 2.0) - np.float_power(dft_uncertainty_mat, 2.0)
sensitivity_squared = np.float_power(first_derivative, 2.0)

improvement_score = np.multiply(delta_uncertainty_squared, sensitivity_squared)

avg_improvement_score = np.nanmean(improvement_score, axis=1)
avg_improvement_score[np.isnan(avg_improvement_score)] = -np.inf

improvement_score[np.isnan(improvement_score)] = -np.inf


total_uncertainty_squared = np.nansum(np.multiply(sensitivity_squared, np.float_power(total_uncertainty_mat, 2.0)), axis=0)
total_uncertainty = np.array(np.float_power(total_uncertainty_squared, 0.5)).ravel()

# # Save the matrices for convenience
np.save(os.path.join(analysis_dir, 'total_uncertainty_mat'), total_uncertainty_mat)
np.save(os.path.join(analysis_dir, 'dft_uncertainty_mat'), dft_uncertainty_mat)
np.save(os.path.join(analysis_dir, 'first_derivative'), first_derivative)
np.save(os.path.join(analysis_dir, 'improvement_score'), improvement_score)



parameter_indices = np.arange(0, N + M)
improvement_order = [x for _, x in sorted(zip(avg_improvement_score, parameter_indices))][::-1]


# compute improvement total - sum of all possible improvements to make
improvement_total = np.sum(avg_improvement_score[avg_improvement_score > 0])


print('Top Improvement Scores')
print('i\tCt Index\tDb Index\tImprovement Score\tImprovement %\tReaction')
for i in range(0, 200):
    ct_index = improvement_order[i]

    if ct_index < N:
        db_index = database_fun.get_unique_species_index(species_list[ct_index])
        
        print(i, '\t', ct_index, '\t\t', db_index, '\t', np.round(avg_improvement_score[ct_index], 9),
              '\t', gas.species()[ct_index], )
    else:
        family = 'PDEP'
        try:
            family = reaction_list[ct2rmg_rxn[ct_index - N]].family
        except AttributeError:
            pass
        db_index = database_fun.get_unique_reaction_index(reaction_list[ct2rmg_rxn[ct_index - N]])
        print(i, '\t', ct_index - N, '\t\t', db_index, '\t', np.round(avg_improvement_score[ct_index], 9),
              '\t', np.round(avg_improvement_score[ct_index] / improvement_total, 9), '\t', gas.reactions()[ct_index - N], family)

# ----------------------- Save to summary csv ------------------------
database = rmgpy.data.rmg.RMGDatabase()

database.load(
    path = rmgpy.settings['database.directory'],
    thermo_libraries = ['BurkeH2O2', 'primaryThermoLibrary'],
    transport_libraries = [],
    reaction_libraries = [],
    seed_mechanisms = [],
    kinetics_families = ['Disproportionation', 'H_Abstraction', 'R_Addition_MultipleBond', 'intra_H_migration'],
    kinetics_depositories = ['training'],
    #frequenciesLibraries = self.statmechLibraries,
    depository = False,
)
for family in database.kinetics.families:
    if not database.kinetics.families[family].auto_generated:
        database.kinetics.families[family].add_rules_from_training(thermo_database=database.thermo)
        database.kinetics.families[family].fill_rules_by_averaging_up(verbose=True)


def PDEP_possible(pdep_reaction):
    for family in database.kinetics.families:
        try:
            database.kinetics.families[family].add_atom_labels_for_reaction(pdep_reaction)
            template_labels = database.kinetics.families[family].get_reaction_template_labels(pdep_reaction)
            template = database.kinetics.families[family].retrieve_template(template_labels)
            kinetics = database.kinetics.families[family].get_kinetics_for_template(template, degeneracy=pdep_reaction.degeneracy)[0]
            pdep_reaction.kinetics = kinetics
            return family
        except (rmgpy.exceptions.UndeterminableKineticsError, rmgpy.exceptions.KineticsError, rmgpy.exceptions.ActionError, IndexError, ValueError):
            continue
    return None



# Make a summary CSV

cols = ['rank', 'db_index', 'reaction', 'family', 'possible', 'avg_IS_pct_possible', 'uncertainty', 'avg_sens']
mech_summary = pd.DataFrame(columns=cols)

# improvement rank
# family is species, PDEP, or the reaction family
# possible is true (1) if we can calculate it, False otherwise
# avg_IS_pct_possible is the percent of the total possible improvement score this parameter represents


total_possible = 0
for i in range(len(avg_improvement_score)):
    if avg_improvement_score[i] > 0:
        if i < N:  # assume all species are possible
            total_possible += avg_improvement_score[i]
            continue
        
        family = 'PDEP'
        try:
            family = reaction_list[ct2rmg_rxn[i - N]].family
        except AttributeError:
            pass
        # only these families are possible for reactions
        if family in ['H_Abstraction', 'Disproportionation', 'intra_H_migration', 'R_Addition_MultipleBond'] or PDEP_possible(reaction_list[ct2rmg_rxn[i - N]]):
            total_possible += avg_improvement_score[i]


# rank the parameters

parameter_indices = np.arange(0, N + M)
improvement_order = [x for _, x in sorted(zip(avg_improvement_score, parameter_indices))][::-1]


for i in range(0, 200):
    ct_index = improvement_order[i]
    
    if ct_index < N:
        # it's a species
        db_index = database_fun.get_unique_species_index(species_list[ct_index])
        mech_summary.loc[i] = [
            i,
            db_index,
            str(database_fun.index2species(db_index)),
            'species',
            1,
            np.round(avg_improvement_score[ct_index] / total_possible, 9),
            total_uncertainty_array[ct_index],
            avg_first_derivative[ct_index]
        ]   
    else:
        family = 'PDEP'
        try:
            family = reaction_list[ct2rmg_rxn[ct_index - N]].family
        except AttributeError:
            pass
        
        db_index = database_fun.get_unique_reaction_index(reaction_list[ct2rmg_rxn[ct_index - N]])
        improvement_percent = 0
        
        possible = 0
        if family in ['H_Abstraction', 'Disproportionation', 'intra_H_migration', 'R_Addition_MultipleBond'] or PDEP_possible(reaction_list[ct2rmg_rxn[ct_index - N]]):
            possible = 1
            improvement_percent = np.round(avg_improvement_score[ct_index] / total_possible, 9)

        mech_summary.loc[i] = [
            i,
            db_index,
            str(database_fun.index2reaction(db_index)),
            family,
            possible,
            improvement_percent,
            total_uncertainty_array[ct_index],
            avg_first_derivative[ct_index]
        ] 
        
mech_summary.to_csv(os.path.join(working_dir, 'mech_summary.csv'))

