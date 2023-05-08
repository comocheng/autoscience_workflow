# Script to calculate delays at a given condition for a given set of models
# but it will use more temperature points than those given for smoother plots

import os
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures


def get_delay(gas, T, P, X):
    # function to run a RCM simulation

    t_end = 1.0  # time in seconds
    gas.TPX = T, P, X

    env = ct.Reservoir(ct.Solution('air.yaml'))
    # env = ct.Reservoir(ct.Solution('air.xml'))
    reactor = ct.IdealGasReactor(gas)
    wall = ct.Wall(reactor, env, A=1.0, velocity=0)
    reactor_net = ct.ReactorNet([reactor])
    # # allegedly faster solving
    # reactor_net.derivative_settings = {"skip-third-bodies": True, "skip-falloff": True}
    # reactor_net.preconditioner = ct.AdaptivePreconditioner()

    times = [0]
    T = [reactor.T]
    P = [reactor.thermo.P]
    X = [reactor.thermo.X]  # mol fractions
    while reactor_net.time < t_end:
        reactor_net.step()

        times.append(reactor_net.time)
        T.append(reactor.T)
        P.append(reactor.thermo.P)
        X.append(reactor.thermo.X)

    slopes = np.gradient(P, times)
    i = np.argmax(slopes)
    return times[i]


# Load the models
this_dir = os.path.dirname(__file__)
# base_rmg_path = os.path.join(this_dir, '../../butane/models/rmg_model/chem_annotated.cti')  # base RMG
base_rmg_path = '/home/moon/autoscience/autoscience/butane/models/rmg_model/chem_annotated.cti'  # base RMG
aramco_path = '/home/moon/autoscience/autoscience/butane/models/aramco/AramcoMech3.0.cti'
improved_rmg_path = '/home/moon/autoscience/autoscience/butane/models/modifications/cutoff3_20230418.cti'

base_rmg_path = '/work/westgroup/harris.se/autoscience/autoscience/butane/models/rmg_model/chem_annotated.cti'  # base RMG
aramco_path = '/work/westgroup/harris.se/autoscience/autoscience/butane/models/aramco/AramcoMech3.0.cti'
improved_rmg_path = '/work/westgroup/harris.se/autoscience/autoscience/butane/models/modifications/cutoff3_20230418.cti'


models_to_plot = {
    'base_rmg': base_rmg_path,
    'aramco': aramco_path,
    'improved_rmg': improved_rmg_path,
    # 'healy': healy_path,
}


# base_rmg_gas = ct.Solution(base_rmg_path)
# # aramco_gas = ct.Solution(aramco_path)
# improved_model_gas = ct.Solution(improved_model_path)

# tables_to_plot = [i for i in range(1, 13)]
# tables_to_plot = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
tables_to_plot = [8, 9, 10, 11, 12]
# tables_to_plot = [7]
model_keys = ['base_rmg', 'improved_rmg', 'aramco']
# model_keys = ['base_rmg']


# Load the experimental conditions

ignition_delay_data = '/home/moon/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
ignition_delay_data = '/work/westgroup/harris.se/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
df_exp = pd.read_csv(ignition_delay_data)
for table_index in tables_to_plot:

    # slice just table in question
    one_table = df_exp[df_exp['Table'] == table_index]
    # Define Initial conditions using experimental data
    tau = one_table['time (ms)'].values.astype(float)  # ignition delay
    T = one_table['T_C'].values  # Temperatures
    P = one_table['nominal pressure(atm)'].values * ct.one_atm  # pressures in atm

    # list of starting conditions
    # Mixture compositions taken from table 2 of
    # https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
    phi = one_table['phi'].values[0]
    if phi == 0.3:
        x_diluent = 0.7821
        conc_dict = {
            'O2(2)': 0.2083,
            'butane(1)': 0.00962
        }
    elif phi == 0.5:
        x_diluent = 0.7771
        conc_dict = {
            'O2(2)': 0.2070,
            'butane(1)': 0.01595
        }
    elif phi == 1.0:
        x_diluent = 0.7649
        conc_dict = {
            'O2(2)': 0.2038,
            'butane(1)': 0.03135
        }
    elif phi == 2.0:
        x_diluent = 0.7416
        conc_dict = {
            'O2(2)': 0.1976,
            'butane(1)': 0.06079
        }

    concentrations = []
    for i in range(0, len(one_table)):
        x_N2 = one_table['%N2'].values[i] / 100.0 * x_diluent
        x_Ar = one_table['%Ar'].values[i] / 100.0 * x_diluent
        x_CO2 = one_table['%CO2'].values[i] / 100.0 * x_diluent
        conc_dict['N2'] = x_N2
        conc_dict['Ar'] = x_Ar
        conc_dict['CO2(7)'] = x_CO2
        concentrations.append(conc_dict)

    def run_simulation(cti_path, T, P, X):
        gas = ct.Solution(cti_path)
        # replace the concentations that have different names in RMG and Aramco
        if 'butane(1)' not in gas.species_names and 'butane(1)' in X.keys():
            # check the keys to make sure we don't pop twice TODO should be O2 not in keys
            X['C4H10'] = X.pop('butane(1)')
        if 'O2(2)' not in gas.species_names and 'O2(2)' in X.keys():
            X['O2'] = X.pop('O2(2)')
        if 'CO2(7)' not in gas.species_names and 'CO2(7)' in X.keys():
            X['CO2'] = X.pop('CO2(7)')
        if 'Ar' not in gas.species_names and 'Ar' in X.keys():
            X['AR'] = X.pop('Ar')

        delay = get_delay(gas, T, P, X)
        return delay

    # Run all simulations in parallel for Base RMG model:

    # create an empty pandas dataframe to store the results
    results_df = pd.DataFrame(columns=['T', 'P', 'delay(ms)', 'phi', 'X', 'table_index'])

    # get min and max temperatures
    T_min = np.min(one_table['T_C'].values)
    T_max = np.max(one_table['T_C'].values)
    P = one_table['nominal pressure(atm)'].values[0] * ct.one_atm  # pressures in atm
    X = concentrations[0]
    N = 51
    temperatures = np.linspace(T_min, T_max, N)

    for model_key in model_keys:
        os.makedirs(os.path.join(this_dir, model_key), exist_ok=True)
        print(f'Running {model_key}')

        delays = np.zeros(len(temperatures))

        # # try serial first
        # for i in range(0, len(temperatures)):
        #     delays[i] = run_simulation(models_to_plot[model_key], temperatures[i], P, X)
        #     results_df = results_df.append({'T': temperatures[i], 'P': P, 'delay(ms)': delays[i], 'phi': phi, 'X': X, 'table_index': table_index}, ignore_index=True)

        # print(delays)
        condition_indices = np.arange(0, len(temperatures))
        with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
            for condition_index, delay_time in zip(condition_indices, executor.map(
                run_simulation,
                [models_to_plot[model_key] for x in condition_indices],
                [T for T in temperatures],
                [P for x in condition_indices],
                [X for x in condition_indices])
            ):
                delays[condition_index] = delay_time

        for i in range(0, len(temperatures)):
            results_df = results_df.append({'T': temperatures[i], 'P': P, 'delay(ms)': delays[i], 'phi': phi, 'X': X, 'table_index': table_index}, ignore_index=True)

        # save the results
        results_df.to_csv(os.path.join(this_dir, model_key, f'table_{table_index}_smooth.csv'))

        # np.save(os.path.join(this_dir, model_key, f'table_{table_index}.npy'), delays)
