# script to save a .npy with base delays for each of the tables across all 51 conditions

import os
import sys
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import rmgpy.chemkin
import subprocess


# get the table index from input for easy parallelization
chemkin = sys.argv[1]

experimental_table_index = int(sys.argv[2])

working_dir = os.path.join(os.path.dirname(chemkin))

# transport = os.path.join(working_dir, 'tran.dat')
# species_dict = os.path.join(working_dir, 'species_dictionary.txt')
# species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(chemkin, dictionary_path=species_dict, transport_path=transport)
# print(f'Loaded {len(species_list)} species, {len(reaction_list)} reactions')
base_yaml_path = os.path.join(working_dir, 'base.yaml')

assert os.path.exists(base_yaml_path)

# load the 2 ctis
base_gas = ct.Solution(base_yaml_path)


# Take Reactor Conditions from Table 7 of supplementary info in
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
def run_simulation(T_orig, P_orig, X_orig):
    # function to run a RCM simulation

    atols = [1e-15, 1e-15, 1e-18]
    rtols = [1e-9, 1e-12, 1e-15]
    for attempt_index in range(0, len(atols)):
        T = T_orig
        P = P_orig
        X = X_orig

        # gas is a global object
        t_end = 1.0  # time in seconds
        base_gas.TPX = T, P, X

        reactor = ct.IdealGasReactor(base_gas)
        reactor_net = ct.ReactorNet([reactor])
        reactor_net.atol = atols[attempt_index]
        reactor_net.rtol = rtols[attempt_index]

        times = [0]
        T = [reactor.T]
        P = [reactor.thermo.P]
        X = [reactor.thermo.X]  # mol fractions
        MAX_STEPS = 10000
        step_count = 0
        failed = False
        while reactor_net.time < t_end:
            try:
                reactor_net.step()
            except ct._cantera.CanteraError:
                print(f'Reactor failed to solve! {attempt_index}')
                failed = True
                break
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                # return 0

            times.append(reactor_net.time)
            T.append(reactor.T)
            P.append(reactor.thermo.P)
            X.append(reactor.thermo.X)

            step_count += 1
            if step_count > MAX_STEPS:
                print(f'Too many steps! Reactor failed to solve! {attempt_index}')
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                failed = True
                break
                # return 0

        if not failed:
            slopes = np.gradient(P, times)
            delay_i = np.argmax(slopes)
            return times[delay_i]
        print(f'trying again {attempt_index}')

    print('Reactor failed to solve after many attempts!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return 0


# Load the experimental conditions
ignition_delay_data = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'experiment', 'butane_ignition_delay.csv')
df_exp = pd.read_csv(ignition_delay_data)
table_exp = df_exp[df_exp['Table'] == experimental_table_index]
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

if phi7[0] == 0.3:
    x_diluent = 0.7821
    conc_dict = {
        'O2(2)': 0.2083,
        'butane(1)': 0.00962
    }
elif phi7[0] == 0.5:
    x_diluent = 0.7771
    conc_dict = {
        'O2(2)': 0.2070,
        'butane(1)': 0.01595
    }
elif phi7[0] == 1.0:
    x_diluent = 0.7649
    conc_dict = {
        'O2(2)': 0.2038,
        'butane(1)': 0.03135
    }
elif phi7[0] == 2.0:
    x_diluent = 0.7416
    conc_dict = {
        'O2(2)': 0.1976,
        'butane(1)': 0.06079
    }
else:
    raise ValueError

if 'aramco' in chemkin.lower():
    o2_conc = conc_dict.pop('O2(2)')
    conc_dict['O2'] = o2_conc

    butane_conc = conc_dict.pop('butane(1)')
    conc_dict['C4H10'] = butane_conc


for i in range(0, len(table_exp)):
    x_N2 = table_exp['%N2'].values[i] / 100.0 * x_diluent
    x_Ar = table_exp['%Ar'].values[i] / 100.0 * x_diluent
    x_CO2 = table_exp['%CO2'].values[i] / 100.0 * x_diluent
    conc_dict['N2'] = x_N2
    conc_dict['Ar'] = x_Ar
    if 'aramco' in chemkin.lower():
        conc_dict['CO2'] = x_CO2
    else:
        conc_dict['CO2(7)'] = x_CO2
    concentrations.append(conc_dict)

# just use the first concentration
Tmax = 1077  # use min and max temperature range of the data: 663K-1077K
Tmin = 663
N = 51
temperatures = np.linspace(Tmin, Tmax, N)


def same_reaction(rxn1, rxn2):
    """Returns true IFF reactions have same reactants, products, and type"""
    if rxn1.reactants == rxn2.reactants and rxn1.products == rxn2.products and type(rxn1) == type(rxn2):
        return True
    else:
        return False


# compute and save the delays
base_delays = np.zeros(len(temperatures))

# save the result as a pandas dataframe
table_dir = os.path.join(working_dir, f'table_{experimental_table_index:04}')
os.makedirs(table_dir, exist_ok=True)


# Run all simulations in parallel
condition_indices = np.arange(0, len(temperatures))

with concurrent.futures.ProcessPoolExecutor(max_workers=26) as executor:
    for condition_index, delay_time in zip(condition_indices, executor.map(
        run_simulation,
        [temperatures[j] for j in condition_indices],
        [P7[0] for j in condition_indices],
        [concentrations[0] for j in condition_indices]
    )):
        base_delays[condition_index] = delay_time


# save the result as a numpy thing
np.save(os.path.join(table_dir, f'base_delays_{experimental_table_index:04}.npy'), base_delays)
