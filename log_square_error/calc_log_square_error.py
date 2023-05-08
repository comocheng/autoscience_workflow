# script compute log squared error of a mechanism compared to all data points from RCM
# experiments, but in a more parallel way

# assume 32 workers available

import os
import sys
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures


# load the mechanism
mech = int(sys.argv[1])

base_rmg = '/work/westgroup/harris.se/autoscience/reaction_calculator/models/base_rmg_1week/chem_annotated.cti'
improved_rmg = '/work/westgroup/harris.se/autoscience/reaction_calculator/models/base_rmg_1week/cutoff3_20230505_top50.cti'
aramco = '/work/westgroup/harris.se/autoscience/autoscience/butane/models/aramco/AramcoMech3.0.cti'

MAX_WORKERS = 48


# Take Reactor Conditions from Table 7 of supplementary info in
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
def run_simulation(T, P, X):
    # function to run a RCM simulation

    # gas is a global object
    t_end = 1.0  # time in seconds
    base_gas.TPX = T, P, X

    reactor = ct.IdealGasReactor(base_gas)
    reactor_net = ct.ReactorNet([reactor])

    times = [0]
    T = [reactor.T]
    P = [reactor.thermo.P]
    X = [reactor.thermo.X]  # mol fractions
    while reactor_net.time < t_end:
        try:
            reactor_net.step()
        except ct._cantera.CanteraError:
            print('Reactor failed to solve!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return 0

        times.append(reactor_net.time)
        T.append(reactor.T)
        P.append(reactor.thermo.P)
        X.append(reactor.thermo.X)

    slopes = np.gradient(P, times)
    delay_i = np.argmax(slopes)
    return times[delay_i]


# Load the experimental conditions
ignition_delay_data = '/work/westgroup/harris.se/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
# ignition_delay_data = '/home/moon/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
df_exp = pd.read_csv(ignition_delay_data)
table_exp = df_exp[df_exp['Table'] < 13]
# Define Initial conditions using experimental data
tau_exp = table_exp['time (ms)'].values.astype(float)  # ignition delay
T7 = table_exp['T_C'].values  # Temperatures
P7 = table_exp['nominal pressure(atm)'].values * ct.one_atm  # pressures in atm
phi7 = table_exp['phi'].values  # equivalence ratios
# list of starting conditions
# Mixture compositions taken from table 2 of
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
concentrations = []
for i in range(0, len(phi7)):
    if phi7[i] == 0.3:
        x_diluent = 0.7821
        conc_dict = {
            'O2(2)': 0.2083,
            'butane(1)': 0.00962
        }
    elif phi7[i] == 0.5:
        x_diluent = 0.7771
        conc_dict = {
            'O2(2)': 0.2070,
            'butane(1)': 0.01595
        }
    elif phi7[i] == 1.0:
        x_diluent = 0.7649
        conc_dict = {
            'O2(2)': 0.2038,
            'butane(1)': 0.03135
        }
    elif phi7[i] == 2.0:
        x_diluent = 0.7416
        conc_dict = {
            'O2(2)': 0.1976,
            'butane(1)': 0.06079
        }
    else:
        raise ValueError
    if mech == 3:
        o2_conc = conc_dict.pop('O2(2)')
        conc_dict['O2'] = o2_conc

        butane_conc = conc_dict.pop('butane(1)')
        conc_dict['C4H10'] = butane_conc
    
    x_N2 = table_exp['%N2'].values[i] / 100.0 * x_diluent
    x_Ar = table_exp['%Ar'].values[i] / 100.0 * x_diluent
    x_CO2 = table_exp['%CO2'].values[i] / 100.0 * x_diluent
    conc_dict['N2'] = x_N2
    conc_dict['Ar'] = x_Ar
    if mech < 3:
        conc_dict['CO2(7)'] = x_CO2
    else:
        conc_dict['CO2'] = x_CO2
    concentrations.append(conc_dict)
assert len(T7) == len(concentrations)

# compute and save the delays
if mech == 1:
    print('Running Base RMG Delays')
    base_rmg_delays = np.zeros(len(concentrations))
    base_gas = ct.Solution(base_rmg)
    condition_indices = np.arange(0, len(concentrations))
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(
            run_simulation,
            [T7[j] for j in condition_indices],
            [P7[j] for j in condition_indices],
            [concentrations[j] for j in condition_indices]
        )):
            base_rmg_delays[condition_index] = delay_time
    np.save('base_rmg_delays_parallel.npy', base_rmg_delays)
elif mech == 2:
    print('Running Improved RMG Delays')
    improved_rmg_delays = np.zeros(len(concentrations))
    base_gas = ct.Solution(improved_rmg)
    condition_indices = np.arange(0, len(concentrations))
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(
            run_simulation,
            [T7[j] for j in condition_indices],
            [P7[j] for j in condition_indices],
            [concentrations[j] for j in condition_indices]
        )):
            improved_rmg_delays[condition_index] = delay_time
    np.save('improved_rmg_delays_parallel.npy', improved_rmg_delays)
elif mech == 3:
    print('Running Aramco Delays')
    aramco_delays = np.zeros(len(concentrations))
    improved_rmg_delays = np.zeros(len(concentrations))
    base_gas = ct.Solution(aramco)
    condition_indices = np.arange(0, len(concentrations))
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(
            run_simulation,
            [T7[j] for j in condition_indices],
            [P7[j] for j in condition_indices],
            [concentrations[j] for j in condition_indices]
        )):
            aramco_delays[condition_index] = delay_time
    np.save('aramco_delays_parallel.npy', aramco_delays)
