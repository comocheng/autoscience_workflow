# script to save a .npy with base delays for each of the tables across all 51 conditions

import os
import sys
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import subprocess

sys.path.append(os.path.join(os.environ['AUTOSCIENCE_REPO'], 'analysis'))
import ignition_delay


cantera = sys.argv[1]
if cantera.endswith('.inp'):
    cantera = cantera[:-4] + '.yaml'
tokens = os.path.splitext(cantera)
out_npy_file = tokens[0] + '.npy'

base_gas = ct.Solution(cantera)

experimental_table_index = 24

working_dir = os.path.join(os.path.dirname(cantera))


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
            delay1, delay2, max_pressure_rise_time, max_pressure_rise_logtime, valid_ignition = ignition_delay.get_ignition_delays(times, P)
            return (delay1, delay2, max_pressure_rise_time, max_pressure_rise_logtime, valid_ignition)

            # slopes = np.gradient(P, times)
            # delay_i = np.argmax(slopes)
            # return times[delay_i]
        print(f'trying again {attempt_index}')

    print('Reactor failed to solve after many attempts!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return (0, 0, 0, 0, False)


ignition_delay_data = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'experiment', 'dib_ignition_delay.csv')
df_exp = pd.read_csv(ignition_delay_data)

# grab just the Metcalfe 2007 DIB phi=0.5 data P=4 atm (table 24)
ref_table = df_exp[df_exp['Table'] == 24]

# Define Initial conditions using experimental data
taus = ref_table['Time (ms)'].values.astype(float)  # ignition delay
Ts = ref_table['T (K)'].values  # Temperatures
Ps = ref_table['Pressure (bar)'].values * 1e5  # pressures in Pa
phi = ref_table['Phi'].values[0]

# list of starting conditions
concentrations = []
conc_dict = {
    'DIB1(1)': ref_table['DIB1'].values[0],
    'DIB2(2)': ref_table['DIB2'].values[0],
    'O2(3)': ref_table['O2'].values[0],
    'Ar': ref_table['Ar'].values[0]
}
concentrations = [conc_dict for i in range(len(ref_table))]


# compute and save the delays
base_delays = np.zeros((len(Ts), 5))

# Run all simulations in parallel
condition_indices = np.arange(0, len(Ts))

with concurrent.futures.ProcessPoolExecutor(max_workers=26) as executor:
    for condition_index, delay_time in zip(condition_indices, executor.map(
        run_simulation,
        [Ts[j] for j in condition_indices],
        [Ps[0] for j in condition_indices],
        [concentrations[0] for j in condition_indices]
    )):
        base_delays[condition_index, 0] = delay_time[0]  # 2nd-stage delay
        base_delays[condition_index, 1] = delay_time[1]  # 1st-stage delay
        base_delays[condition_index, 2] = delay_time[2]  # time of maximum pressure rise
        base_delays[condition_index, 3] = delay_time[3]  # time of maximum pressure rise using logtimes
        base_delays[condition_index, 4] = delay_time[4]  # valid ignition?


# save the result as a numpy thing
np.save(out_npy_file, base_delays)
