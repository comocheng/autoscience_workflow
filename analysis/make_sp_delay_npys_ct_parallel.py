import os
import sys
import time
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import multiprocessing
import subprocess


start = time.time()
# get the table index from input for easy parallelization



CPUS = os.cpu_count()
print(f'{CPUS} cpus')


chemkin = sys.argv[1]
sp_index = int(sys.argv[2])
aramco = 'aramco' in chemkin.lower()

working_dir = os.path.join(os.path.dirname(chemkin))
experimental_table_index = 7  # workflow only requires calculating it here
table_dir = os.path.join(working_dir, f'table_{experimental_table_index:04}')
spec_delay_file = os.path.join(table_dir, f'spec_delay_{experimental_table_index:04}_{sp_index:04}.npy')
if os.path.exists(spec_delay_file):
    print(f'Skipping {sp_index} because file already exists!')
    exit(0)
os.makedirs(table_dir, exist_ok=True)

base_yaml_path = os.path.join(working_dir, 'base.yaml')


# Take Reactor Conditions from Table 7 of supplementary info in
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
# def run_simulation(yaml_file, species_index, T_orig, P_orig, X_orig):
def run_simulation(args):

    def perturb_species(species):  # TODO maybe load this from a util Python module so code doesn't get repeated so much
        # takes in an RMG species object
        # change the enthalpy offset
        DELTA_J_MOL = 418.4  # J/mol, but equals 0.1 kcal/mol
        R = 8.3144598  # gas constant in J/mol
        DELTA = 0.01

        # copy the species
        input_data = species.input_data
        increase = None
        for i in range(len(input_data['thermo']['data'])):
            if not increase:
                # Only define the increase in enthalpy once or you'll end up with numerical gaps in continuity
                # increase = DELTA * new_coeffs[5]
                increase = DELTA_J_MOL / R
            input_data['thermo']['data'][i][5] += increase
        new_species = ct.Species().from_dict(input_data)
        return new_species

    yaml_file, species_index, T_orig, P_orig, X_orig = args
    # function to run a RCM simulation
    gas = ct.Solution(yaml_file)

    # compute and save the delays
    if species_index >= len(gas.species()):
        print(f'Skipping species {species_index} because not in model')
        exit(-1)

    # perturb the one species
    sp_copy = ct.Species().from_dict(gas.species()[species_index].input_data)
    perturbed_species = perturb_species(gas.species()[species_index])
    gas.modify_species(species_index, perturbed_species)

    t_end = 1.0  # time in seconds
    atols = [1e-15, 1e-15, 1e-18]
    rtols = [1e-9, 1e-12, 1e-15]
    for attempt_index in range(0, len(atols)):
        T = T_orig
        P = P_orig
        X = X_orig

        gas.TPX = T, P, X

        reactor = ct.IdealGasReactor(gas)
        reactor_net = ct.ReactorNet([reactor])
        reactor_net.atol = atols[attempt_index]
        reactor_net.rtol = rtols[attempt_index]

        times = [0]
        T = [reactor.T]
        P = [reactor.thermo.P]
        MAX_STEPS = 10000
        step_count = 0
        failed = False
        print(f'starting sim T={T}K')
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
N = 4
temperatures = np.linspace(Tmin, Tmax, N)

# Run all simulations in parallel
delays = np.zeros(len(temperatures))
condition_indices = np.arange(0, len(temperatures))

sim_start = time.time()


def run_command(command):
    p = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    output = p.communicate()
    text = output[0].decode('utf-8')
    delay = float(text.strip())
    return delay


external_sim_script = '/work/westgroup/harris.se/autoscience/reaction_calculator/analysis/run_external_sim.py'


def run_external_simulation(args):
    yaml, T, P, X = args
    command = f'python {external_sim_script} {yaml} {sp_index} {T} {P} ' + "\"" + X + "\""
    return run_command(command)


conc_str = 'O2(2): 0.2038, butane(1): 0.03135, N2: 0.0, Ar: 0.7649, CO2(7): 0.0'
sim_start = time.time()

with multiprocessing.Pool(processes=int(CPUS / 2.0)) as pool:
    args = [(f'base{j}.yaml', temperatures[j], P7[0], conc_str) for j in condition_indices]
    delays = pool.map(run_external_simulation, args)


# with multiprocessing.Pool(processes=CPUS) as pool:
#     args = [(base_yaml_path, sp_index, temperatures[j], P7[0], {'O2(2)': 0.2038, 'butane(1)': 0.03135}) for j in condition_indices]
#     delays = pool.map(run_simulation, args)


# with concurrent.futures.ProcessPoolExecutor(max_workers=CPUS) as executor:
#     for condition_index, delay_time in zip(condition_indices, executor.map(
#         run_simulation,
#         [base_yaml_path for j in condition_indices],
#         [sp_index for j in condition_indices],
#         [temperatures[j] for j in condition_indices],
#         [P7[0] for j in condition_indices],
#         [concentrations[0] for j in condition_indices]
#     )):
#         delays[condition_index] = delay_time

np.save(spec_delay_file, delays)
end = time.time()

print(f'Elapsed: {end - start}')
print(f'Sim: {end - sim_start}')
