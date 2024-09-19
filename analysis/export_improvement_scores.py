# script to calculate and export the improvement score after the
# sensitivity has been run

# script to save the rankings for the mechanism
import os
import re
import sys
import glob
import copy
import yaml
import pickle
import subprocess
import numpy as np
import pandas as pd

import rmgpy.data.kinetics
import rmgpy.chemkin
import cantera as ct

sys.path.append(os.path.join(os.environ['AUTOSCIENCE_REPO'], 'database'))
import database_fun


# ----------------------- Load the mechanism in Cantera and RMG ----------------------------------
input_chemkin = sys.argv[1]
assert input_chemkin.endswith('chem_annotated.inp')
basedir = os.path.dirname(input_chemkin)
analysis_dir = os.path.join(basedir, 'analysis')
os.makedirs(analysis_dir, exist_ok=True)

cantera_file = os.path.join(basedir, 'chem_annotated.yaml')
base_chemkin = os.path.join(basedir, 'chem_annotated.inp')
dictionary = os.path.join(basedir, 'species_dictionary.txt')
transport = os.path.join(basedir, 'tran.dat')

# convert chemkin to cantera if it doesn't already exist
if not os.path.exists(cantera_file):
    subprocess.run(['ck2yaml', f'--input={input_chemkin}', f'--transport={transport}', f'--output={cantera_file}'])

species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(base_chemkin, dictionary_path=dictionary, transport_path=transport, use_chemkin_names=True)

gas = ct.Solution(cantera_file)
perturbed_cti_path = os.path.join(basedir, 'perturbed.yaml')
perturbed_gas = ct.Solution(perturbed_cti_path)

# make a dictionary for mapping from cantera reactions back to RMG reactions
if not os.path.exists(os.path.join(basedir, 'ct2rmg_rxn.pickle')):
    print('Creating ct2rmg pickle')
    subprocess.run(['python', os.path.join(os.environ['AUTOSCIENCE_REPO'], 'analysis', 'ct2rmg_dict.py'), base_chemkin])

with open(os.path.join(basedir, 'ct2rmg_rxn.pickle'), 'rb') as handle:
    ct2rmg_rxn = pickle.load(handle)

print(f'{len(species_list)} species loaded')
print(f'{len(reaction_list)} reactions loaded')

N = len(gas.species())
M = len(gas.reactions())

# ----------------------- Load the Uncertainty ----------------------
rxn_uncertainty_file = os.path.join(basedir, 'gao_reaction_uncertainty.npy')
sp_uncertainty_file = os.path.join(basedir, 'gao_species_uncertainty.npy')

rmg_rxn_uncertainty = np.load(rxn_uncertainty_file)
rmg_sp_uncertainty = np.load(sp_uncertainty_file)

assert len(rmg_rxn_uncertainty) == len(reaction_list)
assert len(rmg_sp_uncertainty) == len(species_list)

# create big matrix of uncertainties based on Cantera order
rxn_uncertainty = np.zeros(len(gas.reactions()))
for ct_index in range(len(rxn_uncertainty)):
    rxn_uncertainty[ct_index] = rmg_rxn_uncertainty[ct2rmg_rxn[ct_index]]

# Cantera species should be in same rmg order, but this makes sure for us
for i in range(len(species_list)):
    assert str(species_list[i]) == gas.species_names[i]

sp_uncertainty = rmg_sp_uncertainty

total_uncertainty_array = np.concatenate((sp_uncertainty, rxn_uncertainty), axis=0)
total_uncertainty_mat = np.repeat(np.transpose(np.matrix(total_uncertainty_array)), 12 * 51, axis=1)

# create matrix of DFT errors
# will later subtract this from actual error to see if DFT is expected to improve model
SPECIES_DFT_ERROR = 3.0
REACTION_DFT_ERROR = 1 / np.sqrt(3) * np.log(10)
sp_dft_uncertainty_mat = np.ones((N, 12 * 51)) * SPECIES_DFT_ERROR
rxn_dft_uncertainty_mat = np.ones((M, 12 * 51)) * REACTION_DFT_ERROR
dft_uncertainty_mat = np.concatenate((sp_dft_uncertainty_mat, rxn_dft_uncertainty_mat), axis=0)

# print out the top 10 uncertain reactions
reaction_indices = np.arange(0, len(gas.reactions()))
reaction_uncertainty_order = [x for _, x in sorted(zip(rxn_uncertainty, reaction_indices))][::-1]
print('Top 10 Uncertain Reactions')
print('i\tDelta\tReaction\tSensitivity\tImprovement Score')
# TODO convert to db indices? instead of ct
for i in range(0, 10):
    ct_index = reaction_uncertainty_order[i]
    print(ct_index, '\t', np.round(rxn_uncertainty[ct_index], 3),
          '\t', gas.reactions()[ct_index],
          '\t', reaction_list[ct2rmg_rxn[ct_index]].family)


# ---------------------- Load sensitivities -------------------
# load the giant base delays matrix
base_delay_file = os.path.join(basedir, 'total_base_delays.npy')
base_delays = np.load(base_delay_file)

# Load the giant delays matrix
total_delay_file = os.path.join(basedir, 'total_perturbed_mech_delays.npy')
total_delays = np.load(total_delay_file)

assert total_delays.shape[1] == len(base_delays)

total_base_delays = np.repeat(np.matrix(base_delays), total_delays.shape[0], axis=0)
total_base_delays[total_base_delays == 0] = np.nan
assert total_base_delays.shape == total_delays.shape

total_delays[total_delays == 0] = np.nan

d_ln_tau = np.log(total_delays) - np.log(total_base_delays)
avg_d_ln_tau = np.nanmean(d_ln_tau, axis=1)
avg_d_ln_tau[np.isnan(avg_d_ln_tau)] = -np.inf


# ----------------- Get Delta G -------------------
phi_dicts = []
for table_index in range(1, 13):

    # Load the experimental conditions
    ignition_delay_data = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'experiment', 'butane_ignition_delay.csv')
    df_exp = pd.read_csv(ignition_delay_data)
    table_exp = df_exp[df_exp['Table'] == table_index]
    # Define Initial conditions using experimental data
    tau_exp = table_exp['time (ms)'].values.astype(float)  # ignition delay
    T7 = table_exp['T_C'].values  # Temperatures
    P7 = table_exp['nominal pressure(atm)'].values * ct.one_atm  # pressures in atm
    phi7 = table_exp['phi'].values  # equivalence ratios
    # list of starting conditions
    # Mixture compositions taken from table 2 of
    # https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
    concentrations = []
    # for phi = 1
    x_diluent = 0.7649
    conc_dict = {
        'O2(2)': 0.2038,
        'butane(1)': 0.03135
    }

    x_N2 = table_exp['%N2'].values[0] / 100.0 * x_diluent
    x_Ar = table_exp['%Ar'].values[0] / 100.0 * x_diluent
    x_CO2 = table_exp['%CO2'].values[0] / 100.0 * x_diluent
    conc_dict['N2'] = x_N2
    conc_dict['Ar'] = x_Ar
    conc_dict['CO2(7)'] = x_CO2

    phi_dicts.append(conc_dict)


# There are 12 * K different simulation settings. We need each parameter estimate at each setting
# Create a matrix with temperatures and one with pressures
T = np.linspace(663, 1077, 51)
table_temperatures = np.repeat(np.matrix(T), 12, axis=1)
temperatures = np.repeat(table_temperatures, total_delays.shape[0], axis=0)
pressures = np.zeros(temperatures.shape)
for i in range(pressures.shape[1]):
    if int(i / 51) in [0, 3, 6, 9]:
        pressures[:, i] = 10.0 * 101325.0
    elif int(i / 51) in [1, 4, 7, 10]:
        pressures[:, i] = 20.0 * 101325.0
    elif int(i / 51) in [2, 5, 8, 11]:
        pressures[:, i] = 30.0 * 101325.0

G_base = np.zeros((N, total_delays.shape[1]))
G_perturbed = np.zeros((N, total_delays.shape[1]))

# get base G values
mod_gas = ct.Solution(cantera_file)
for j in range(N):
    for i in range(temperatures.shape[1]):
        T = temperatures[0, i]
        gas.TPX = T, pressures[0, i], phi_dicts[int(i / 51)]
        G_base[j, i] = gas.species()[j].thermo.h(T) - T * gas.species()[j].thermo.s(T)

# Get perturned G values
mod_gas = ct.Solution(cantera_file)
for j in range(N):
    # change just the one reaction
    mod_gas.modify_species(j, perturbed_gas.species()[j])
    for i in range(temperatures.shape[1]):
        T = temperatures[0, i]
        mod_gas.TPX = T, pressures[0, i], phi_dicts[int(i / 51)]
        G_perturbed[j, i] = mod_gas.species()[j].thermo.h(T) - T * mod_gas.species()[j].thermo.s(T)

    mod_gas.modify_species(j, gas.species()[j])

# G has units Enthalpy [J/kg or J/kmol] it's J / kmol
delta_G = G_perturbed - G_base
delta_G_kcal_mol = delta_G / 4.184 / 1000.0 / 1000.0  # needs to be kcal/mol to match Gao paper


# ----------------- Get Delta k -------------------
# except we know that by definition, this is 0.1
delta_ln_k = 0.1 * np.ones((M, total_delays.shape[1]))

# concatenate into a big delta matrix
delta = np.concatenate((delta_G_kcal_mol, delta_ln_k), axis=0)

# first derivative is change in delay / change in G
first_derivative = np.divide(d_ln_tau, delta)


# --------------------- Display top 10 sensitive parameters
avg_first_derivative = np.nanmean(first_derivative, axis=1)
abs_avg_first_derivative = np.abs(avg_first_derivative)
abs_avg_first_derivative[np.isnan(abs_avg_first_derivative)] = -np.inf

parameter_indices = np.arange(0, N + M)
reaction_sensitivity_order = [x for _, x in sorted(zip(abs_avg_first_derivative, parameter_indices))][::-1]

print('Top Sensitive Parameters')
print('i\tDelta\tReaction\tSensitivity\tImprovement Score')
for i in range(0, 10):
    ct_index = reaction_sensitivity_order[i]
    if ct_index < N:
        print(ct_index, '\t', np.round(abs_avg_first_derivative[ct_index, 0], 9),
              '\t', gas.species()[ct_index], )
    else:
        print(ct_index, '\t', np.round(abs_avg_first_derivative[ct_index, 0], 9),
              '\t', gas.reactions()[ct_index - N])


# ------------- Compute the improvement score ------------
delta_uncertainty_squared = np.float_power(total_uncertainty_mat, 2.0) - np.float_power(dft_uncertainty_mat, 2.0)
sensitivity_squared = np.float_power(first_derivative, 2.0)

improvement_score = np.multiply(delta_uncertainty_squared, sensitivity_squared)

avg_improvement_score = np.nanmean(improvement_score, axis=1)
avg_improvement_score[np.isnan(avg_improvement_score)] = -np.inf

improvement_score[np.isnan(improvement_score)] = -np.inf

# Save the matrices for convenience
np.save(os.path.join(analysis_dir, 'total_uncertainty_mat'), total_uncertainty_mat)
np.save(os.path.join(analysis_dir, 'dft_uncertainty_mat'), dft_uncertainty_mat)
np.save(os.path.join(analysis_dir, 'first_derivative'), first_derivative)
np.save(os.path.join(analysis_dir, 'improvement_score'), improvement_score)


# -------------------- Display top 50 Improvement scores -------------
parameter_indices = np.arange(0, N + M)
improvement_order = [x for _, x in sorted(zip(avg_improvement_score, parameter_indices))][::-1]

# compute improvement total - sum of all possible improvements to make
improvement_total = np.sum(avg_improvement_score[avg_improvement_score > 0])
print('Top Improvement Scores')
print('i\tCt Index\tDb Index\tImprovement Score\tImprovement %\tReaction')
new_top50 = set()
for i in range(0, 50):
    ct_index = improvement_order[i]
    if ct_index < N:
        print(i, '\t', ct_index, '\t\t', '?', '\t', np.round(avg_improvement_score[ct_index, 0], 9),
              '\t', gas.species()[ct_index], )
        new_top50.add(ct_index)
    else:
        family = 'PDEP'
        try:
            family = reaction_list[ct2rmg_rxn[ct_index - N]].family
        except AttributeError:
            pass
        db_index = database_fun.get_unique_reaction_index(reaction_list[ct2rmg_rxn[ct_index - N]])
        print(i, '\t', ct_index - N, '\t\t', db_index, '\t', np.round(avg_improvement_score[ct_index, 0], 9),
              '\t', np.round(avg_improvement_score[ct_index, 0] / improvement_total, 9), '\t', gas.reactions()[ct_index - N], family)
        new_top50.add(ct_index - N)

print()
print()

# ------------------- Save the top_calculations mech_summary_2024XXXX.csv ---------------------
# Make a summary CSV

cols = ['rank', 'db_index', 'reaction', 'family', 'possible', 'avg_IS_pct_possible']
mech_summary = pd.DataFrame(columns=cols)

# improvement rank
# family is species, PDEP, or the reaction family
# possible is true (1) if we can calculate it, False otherwise
# avg_IS_pct_possible is the percent of the total posisble improvement score this parameter represents

total_possible = 0
for i in range(len(avg_improvement_score)):
    if avg_improvement_score[i] > 0:
        if i < N:  # assume all species are possible
            total_possible += avg_improvement_score[i, 0]
            continue
        family = 'PDEP'
        try:
            family = reaction_list[ct2rmg_rxn[i - N]].family
        except AttributeError:
            pass
        # only these families are possible for reactions
        if family in ['H_Abstraction', 'Disproportionation', 'intra_H_migration']:
            total_possible += avg_improvement_score[i, 0]

# rank the parameters, only do top 200
parameter_indices = np.arange(0, N + M)
improvement_order = [x for _, x in sorted(zip(avg_improvement_score, parameter_indices))][::-1]
for i in range(0, 200):
    ct_index = improvement_order[i]
    if ct_index < N:
        # it's a species
        mech_summary.loc[i] = [
            i,
            ct_index,
            str(database_fun.index2species(ct_index)),
            'species',
            1,
            np.round(avg_improvement_score[ct_index, 0] / total_possible, 9)
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
        if family in ['H_Abstraction', 'Disproportionation', 'intra_H_migration']:
            possible = 1
            improvement_percent = np.round(avg_improvement_score[ct_index, 0] / total_possible, 9)
        mech_summary.loc[i] = [
            i,
            db_index,
            str(database_fun.index2reaction(db_index)),
            family,
            possible,
            improvement_percent,
        ]

# save local copy, get _20240404 suffix from basedir folder name
suffix = ''
m1 = re.search('_\d\d\d\d\d\d\d\d', basedir)
if m1:
    suffix = m1[0]
mech_summary_outfile = os.path.join(basedir, f'mech_summary{suffix}.csv')
mech_summary.to_csv(mech_summary_outfile)
