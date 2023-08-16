import os
import sys
import copy
import pandas as pd
import concurrent.futures
import numpy as np
import cantera as ct


user_mech_index = int(sys.argv[1])  # get this from user input so we can run in parallel on SLURM


MAX_WORKERS = 16

# Load the BASE CTI and the IMPROVED CTI

base_cti = '/work/westgroup/harris.se/autoscience/reaction_calculator/models/base_rmg_1week/chem_annotated.cti'
# base_cti = '/home/moon/autoscience/reaction_calculator/models/base_rmg_1week/chem_annotated.cti'
improved_cti = '/work/westgroup/harris.se/autoscience/reaction_calculator/models/base_rmg_1week/cutoff3_20230511_top50.cti'
# improved_cti = '/home/moon/autoscience/reaction_calculator/models/base_rmg_1week/cutoff3_20230511_top50.cti'

gas = ct.Solution(base_cti)
improved_gas = ct.Solution(improved_cti)


for i in range(len(gas.species())):
    assert gas.species_names[i] == improved_gas.species_names[i]


# Load the experimental conditions
ignition_delay_data = '/work/westgroup/harris.se/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
# ignition_delay_data = '/home/moon/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
df_exp = pd.read_csv(ignition_delay_data)
table_exp = df_exp[df_exp['Table'] < 13]
# Define Initial conditions using experimental data
tau_exp = table_exp['time (ms)'].values.astype(float)  # ignition delay
tau_exp[tau_exp == 0] = np.nan
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

    x_N2 = table_exp['%N2'].values[i] / 100.0 * x_diluent
    x_Ar = table_exp['%Ar'].values[i] / 100.0 * x_diluent
    x_CO2 = table_exp['%CO2'].values[i] / 100.0 * x_diluent
    conc_dict['N2'] = x_N2
    conc_dict['Ar'] = x_Ar
    conc_dict['CO2(7)'] = x_CO2

    concentrations.append(conc_dict)
assert len(T7) == len(concentrations)


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
        gas.TPX = T, P, X

        reactor = ct.IdealGasReactor(gas)
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


# Get the TOP 50 parameters to improve
top50 = [  # these are cantera indices
    959, 232, 943, 2469, 776, 821, 2283,
346, 446, 99, 443, 1693, 1764, 777,231,752,1842,742,1315,483,828,102,2346,1139,751,1789,1711,605,822,1138,
757,1316,2352,434,754,1131,2472,1794,606,1749,393,871,1686,861,1713,1550,823,1126,394,614,2356,444,
]


def same_reaction(rxn1, rxn2):
    """Returns true IFF reactions have same reactants, products, and type"""
    if rxn1.reactants == rxn2.reactants and rxn1.products == rxn2.products and type(rxn1) == type(rxn2):
        return True
    else:
        return False


def calc_log_squared_error(mech_delays):
    return np.nansum(np.float_power(np.log(mech_delays) - np.log(tau_exp / 1000.0), 2.0))


errors = np.zeros(51)

# for mech_index in range(0, 51):
for mech_index in [user_mech_index]:
    print(f'Loading Mech {mech_index} into memory')
    gas = ct.Solution(base_cti)
    for parameter_rank in range(0, mech_index):
        parameter_index = top50[parameter_rank]
        # change each of the parameters
        if parameter_index < 130:
            # change species
            print(f'Changing species {parameter_index}')
            gas.modify_species(parameter_index, improved_gas.species()[parameter_index])
        else:
            if same_reaction(improved_gas.reactions()[parameter_index], gas.reactions()[parameter_index]):
                improved_index = parameter_index
            else:
                for k in range(0, len(gas.reactions())):
                    if same_reaction(improved_gas.reactions()[k], gas.reactions()[parameter_index]):
                        improved_index = k
                        break
                else:
                    raise ValueError('Could not find matching reaction in base mechanism')
            print(f'Changing reaction {parameter_index}')
            gas.modify_reaction(parameter_index, improved_gas.reactions()[improved_index])

    print('Gas loaded')
    # Run the simulation
    improved_rmg_delays = np.zeros(len(concentrations))
    condition_indices = np.arange(0, len(concentrations))
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(
            run_simulation,
            [T7[j] for j in condition_indices],
            [P7[j] for j in condition_indices],
            [concentrations[j] for j in condition_indices]
        )):
            improved_rmg_delays[condition_index] = delay_time

        # save the delay times
        np.save(f'rmg_improved_delays_{mech_index:04}.npy', improved_rmg_delays)

        # calculate log error
    # assert np.sum(improved_rmg_delays == 0) == 0
    # log_sq_error = calc_log_squared_error(improved_rmg_delays)
    # errors[mech_index] = log_sq_error

# np.save('log_sq_errors.npy', errors)
