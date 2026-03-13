import os
import sys
import time
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import subprocess


chemkin = sys.argv[1]
reaction_index = int(sys.argv[2])
aramco = False
experimental_table_index = 7

N_Temps = 51
working_dir = os.path.join(os.path.dirname(chemkin))
table_dir = os.path.join(working_dir, f'table_{experimental_table_index:04}')
output_reaction_delays_file = os.path.join(table_dir, f'reaction_delays_{experimental_table_index:04}_{reaction_index:04}.npy')
if os.path.exists(output_reaction_delays_file):
    print(f'Skipping reaction sensitivity {reaction_index} because file already exists!')
    exit(0)
os.makedirs(table_dir, exist_ok=True)


base_yaml_path = os.path.join(working_dir, 'chem_annotated.yaml')


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
if not aramco:
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
    for i in range(0, len(table_exp)):
        x_N2 = table_exp['%N2'].values[i] / 100.0 * x_diluent
        x_Ar = table_exp['%Ar'].values[i] / 100.0 * x_diluent
        x_CO2 = table_exp['%CO2'].values[i] / 100.0 * x_diluent
        conc_dict['N2'] = x_N2
        conc_dict['Ar'] = x_Ar
        conc_dict['CO2(7)'] = x_CO2
        concentrations.append(conc_dict)
else:
    if phi7[0] == 0.3:
        x_diluent = 0.7821
        conc_dict = {
            'O2': 0.2083,
            'C4H10': 0.00962
        }
    elif phi7[0] == 0.5:
        x_diluent = 0.7771
        conc_dict = {
            'O2': 0.2070,
            'C4H10': 0.01595
        }
    elif phi7[0] == 1.0:
        x_diluent = 0.7649
        conc_dict = {
            'O2': 0.2038,
            'C4H10': 0.03135
        }
    elif phi7[0] == 2.0:
        x_diluent = 0.7416
        conc_dict = {
            'O2': 0.1976,
            'C4H10': 0.06079
        }
    else:
        raise ValueError
    for i in range(0, len(table_exp)):
        x_N2 = table_exp['%N2'].values[i] / 100.0 * x_diluent
        x_Ar = table_exp['%Ar'].values[i] / 100.0 * x_diluent
        x_CO2 = table_exp['%CO2'].values[i] / 100.0 * x_diluent
        conc_dict['N2'] = x_N2
        conc_dict['AR'] = x_Ar
        conc_dict['CO2'] = x_CO2
        concentrations.append(conc_dict)

# just use the first concentration
Tmax = 1077  # use min and max temperature range of the data: 663K-1077K
Tmin = 663
# N = 51
temperatures = np.linspace(Tmin, Tmax, N_Temps)


# compute and save the delays
species_delays = np.zeros((len(base_gas.species()), len(temperatures)))
reaction_delays = np.zeros((len(base_gas.reactions()), len(temperatures)))
print(f'perturbing {reaction_index} {base_gas.reactions()[reaction_index]}')

# load the base gas
# base_gas = ct.Solution(base_yaml_path)
base_gas.set_multiplier(1.1, reaction_index)

# Run all simulations in serial because it's faster than parallel
delays = np.zeros(len(temperatures))
condition_indices = np.arange(0, len(temperatures))

for condition_index in range(len(condition_indices)):
    delays[condition_index] = run_simulation(temperatures[condition_index], P7[0], concentrations[0])

reaction_delays[reaction_index, :] = delays


# save the result as a numpy thing
np.save(output_reaction_delays_file, reaction_delays)
