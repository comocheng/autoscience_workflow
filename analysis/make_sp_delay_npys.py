import os
import sys
import time
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import rmgpy.chemkin
import subprocess


# get the table index from input for easy parallelization
DELTA_J_MOL = 418.4  # J/mol, but equals 0.1 kcal/mol
R = 8.3144598  # gas constant in J/mol
DELTA = 0.01
chemkin = sys.argv[1]
sp_index = int(sys.argv[2])

aramco = 'aramco' in chemkin.lower()


working_dir = os.path.join(os.path.dirname(chemkin))
experimental_table_index = 7  # workflow only requires calculating it here
table_dir = os.path.join(working_dir, f'table_{experimental_table_index:04}')
os.makedirs(table_dir, exist_ok=True)


# perturb every species and reaction in the mechanism
# we'll select the perturbations one at a time later in the script
def perturb_species(species):
    # takes in an RMG species object
    # change the enthalpy offset
    increase = None
    for poly in species.thermo.polynomials:
        new_coeffs = poly.coeffs
        if not increase:
            # Only define the increase in enthalpy once or you'll end up with numerical gaps in continuity
            # increase = DELTA * new_coeffs[5]
            increase = DELTA_J_MOL / R
        new_coeffs[5] += increase
        poly.coeffs = new_coeffs


def perturb_reaction(rxn):
    # takes in an RMG reaction object
    # delta is the ln(k) amount to perturb the A factor
    # delta is a multiplicative factor- units don't matter, yay!
    # does not deepycopy because there's some issues with rmgpy.reactions copying
    if type(rxn.kinetics) == rmgpy.kinetics.chebyshev.Chebyshev:
        rxn.kinetics.coeffs.value_si[0][0] += np.log10(1.0 + DELTA)
    elif type(rxn.kinetics) in [rmgpy.kinetics.falloff.Troe, rmgpy.kinetics.falloff.ThirdBody, rmgpy.kinetics.falloff.Lindemann]:
        if hasattr(rxn.kinetics, 'arrheniusHigh'):
            rxn.kinetics.arrheniusHigh.A.value *= np.exp(DELTA)
        if hasattr(rxn.kinetics, 'arrheniusLow'):
            rxn.kinetics.arrheniusLow.A.value *= np.exp(DELTA)
    elif type(rxn.kinetics) == rmgpy.kinetics.arrhenius.MultiArrhenius:
        for j in range(len(rxn.kinetics.arrhenius)):
            rxn.kinetics.arrhenius[j].A.value *= np.exp(DELTA)
    elif type(rxn.kinetics) == rmgpy.kinetics.arrhenius.PDepArrhenius:
        for j in range(len(rxn.kinetics.arrhenius)):
            if type(rxn.kinetics.arrhenius[j]) == rmgpy.kinetics.arrhenius.Arrhenius:
                rxn.kinetics.arrhenius[j].A.value *= np.exp(DELTA)
            elif type(rxn.kinetics.arrhenius[j]) == rmgpy.kinetics.arrhenius.MultiArrhenius:
                for k in range(len(rxn.kinetics.arrhenius[j].arrhenius)):
                    rxn.kinetics.arrhenius[j].arrhenius[k].A.value *= np.exp(DELTA)
            else:
                raise ValueError(f'weird kinetics {str(rxn.kinetics)}')
    elif type(rxn.kinetics) == rmgpy.kinetics.arrhenius.MultiPDepArrhenius:
        for i in range(len(rxn.kinetics.arrhenius)):
            for j in range(len(rxn.kinetics.arrhenius[i].arrhenius)):
                if type(rxn.kinetics.arrhenius[i].arrhenius[j]) == rmgpy.kinetics.arrhenius.Arrhenius:
                    rxn.kinetics.arrhenius[i].arrhenius[j].A.value *= np.exp(DELTA)
                elif type(rxn.kinetics.arrhenius[i].arrhenius[j]) == rmgpy.kinetics.arrhenius.MultiArrhenius:
                    for k in range(len(rxn.kinetics.arrhenius[i].arrhenius[j].arrhenius)):
                        rxn.kinetics.arrhenius[i].arrhenius[j].arrhenius[k].A.value *= np.exp(DELTA)
                else:
                    raise ValueError(f'weird kinetics {str(rxn.kinetics)}')

    else:  # Arrhenius
        rxn.kinetics.A.value *= np.exp(DELTA)


transport = os.path.join(working_dir, 'tran.dat')
species_dict = os.path.join(working_dir, 'species_dictionary.txt')
species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(chemkin, dictionary_path=species_dict, transport_path=transport, use_chemkin_names=True)
print(f'Loaded {len(species_list)} species, {len(reaction_list)} reactions')
base_yaml_path = os.path.join(working_dir, 'base.yaml')
perturbed_chemkin = os.path.join(working_dir, 'perturbed.inp')
perturbed_yaml_path = os.path.join(working_dir, 'perturbed.yaml')

skip_create_perturb = False
if os.path.exists(perturbed_yaml_path):
    skip_create_perturb = True
    print('Perturbed yaml already exists, skipping creation of perturbed mechanism')

if not skip_create_perturb:
    if experimental_table_index == 7:  # only do this once, instead of once for each of the 12 tables
        # load the chemkin file and create a normal and perturbed cti for simulations:
        # # write base cantera
        subprocess.run(['ck2yaml', f'--input={chemkin}', f'--transport={transport}', f'--output={base_yaml_path}'])

        for i in range(0, len(species_list)):
            perturb_species(species_list[i])

        for i in range(0, len(reaction_list)):
            perturb_reaction(reaction_list[i])

            # try:
            #     perturb_reaction(reaction_list[i])
            # except AttributeError:
            #     continue

        # save the results
        rmgpy.chemkin.save_chemkin_file(perturbed_chemkin, species_list, reaction_list, verbose=True, check_for_duplicates=True)
        subprocess.run(['ck2yaml', f'--input={perturbed_chemkin}', f'--transport={transport}', f'--output={perturbed_yaml_path}'])
    else:
        while not os.path.exists(perturbed_yaml_path):
            time.sleep(10)


# load the 2 ctis
base_gas = ct.Solution(base_yaml_path)
perturbed_gas = ct.Solution(perturbed_yaml_path)


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
N = 51
temperatures = np.linspace(Tmin, Tmax, N)


# compute and save the delays
species_delays = np.zeros((len(perturbed_gas.species()), len(temperatures)))

if sp_index >= len(perturbed_gas.species()):
    print(f'Skipping species {sp_index} because not in model')
    exit(-1)

# for i in range(0, len(perturbed_gas.species())):
for i in [sp_index]:
    print(f'perturbing {i} {perturbed_gas.species()[i]}')

    spec_delay_file = os.path.join(table_dir, f'spec_delay_{experimental_table_index:04}_{i:04}.npy')
    if os.path.exists(spec_delay_file):
        print(f'skipping {i} because file already exists!')
        delays = np.load(spec_delay_file)
        species_delays[i, :] = delays
        continue

    # load the base gas
    base_gas = ct.Solution(base_yaml_path)

    # run the simulations at condition #j
    base_gas.modify_species(i, perturbed_gas.species()[i])

    # Run all simulations in parallel
    delays = np.zeros(len(temperatures))
    condition_indices = np.arange(0, len(temperatures))

    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(
            run_simulation,
            [temperatures[j] for j in condition_indices],
            [P7[0] for j in condition_indices],
            [concentrations[0] for j in condition_indices]
        )):
            delays[condition_index] = delay_time
    species_delays[i, :] = delays

    np.save(spec_delay_file, delays)
