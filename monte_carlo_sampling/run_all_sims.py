# script to set up many simulations
import os
import sys
import numpy as np
import cantera as ct
import concurrent.futures

import rmgpy.chemkin
import rmgpy.species
import rmgpy.tools.canteramodel
import rmgpy.constants


# N=10  # These values must be copied in manually.
# Run the setup_mc.ipynb script to get the indices
rmg_species_perturb_indices = [5, 4, 24, 62, 19]
rmg_reaction_perturb_indices = [84, 238, 163, 689, 142]

# Specify this manually for whichever RMG model you want to analyze
basedir = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'RMG_example_fuel_YYYYMMDD')

k_perturbation_matrix = None
G_perturbation_matrix = None


def perturb_species(species, delta):
    # takes in an RMG species object
    # change the enthalpy offset
    # expecting units of J / mol
    # have to set entire list or changes won't persist in memory
    for poly in species.thermo.polynomials:
        new_coeffs = poly.coeffs
        new_coeffs[5] += delta / rmgpy.constants.R
        poly.coeffs = new_coeffs


def perturb_reaction(rxn, delta):  # 0.1 is default
    # takes in an RMG reaction object
    # delta is the ln(k) amount to perturb the A factor
    # delta is a multiplicative factor- units don't matter, yay!
    # does not deepycopy because there's some issues with rmgpy.reactions copying
    if type(rxn.kinetics) == rmgpy.kinetics.chebyshev.Chebyshev:
        rxn.kinetics.coeffs.value_si[0][0] += np.log10(np.exp(delta))
    elif type(rxn.kinetics) in [rmgpy.kinetics.falloff.Troe, rmgpy.kinetics.falloff.ThirdBody, rmgpy.kinetics.falloff.Lindemann]:
        if hasattr(rxn.kinetics, 'arrheniusHigh'):
            rxn.kinetics.arrheniusHigh.A.value *= np.exp(delta)
        if hasattr(rxn.kinetics, 'arrheniusLow'):
            rxn.kinetics.arrheniusLow.A.value *= np.exp(delta)
    elif type(rxn.kinetics) == rmgpy.kinetics.arrhenius.MultiArrhenius:
        for j in range(len(rxn.kinetics.arrhenius)):
            rxn.kinetics.arrhenius[j].A.value *= np.exp(delta)
    elif type(rxn.kinetics) == rmgpy.kinetics.arrhenius.PDepArrhenius:
        for j in range(len(rxn.kinetics.arrhenius)):
            if type(rxn.kinetics.arrhenius[j]) == rmgpy.kinetics.arrhenius.Arrhenius:
                rxn.kinetics.arrhenius[j].A.value *= np.exp(delta)
            elif type(rxn.kinetics.arrhenius[j]) == rmgpy.kinetics.arrhenius.MultiArrhenius:
                for k in range(len(rxn.kinetics.arrhenius[j].arrhenius)):
                    rxn.kinetics.arrhenius[j].arrhenius[k].A.value *= np.exp(delta)
            else:
                raise ValueError(f'weird kinetics {str(rxn.kinetics)}')
    elif type(rxn.kinetics) == rmgpy.kinetics.arrhenius.MultiPDepArrhenius:
        for i in range(len(rxn.kinetics.arrhenius)):
            for j in range(len(rxn.kinetics.arrhenius[i].arrhenius)):
                if type(rxn.kinetics.arrhenius[i].arrhenius[j]) == rmgpy.kinetics.arrhenius.Arrhenius:
                    rxn.kinetics.arrhenius[i].arrhenius[j].A.value *= np.exp(delta)
                elif type(rxn.kinetics.arrhenius[i].arrhenius[j]) == rmgpy.kinetics.arrhenius.MultiArrhenius:
                    for k in range(len(rxn.kinetics.arrhenius[i].arrhenius[j].arrhenius)):
                        rxn.kinetics.arrhenius[i].arrhenius[j].arrhenius[k].A.value *= np.exp(delta)
                else:
                    raise ValueError(f'weird kinetics {str(rxn.kinetics)}')

    else:  # Arrhenius
        rxn.kinetics.A.value *= np.exp(delta)


# Take Reactor Conditions from Table 7 of supplementary info in
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
def get_delay(gas, T_orig, P_orig, X_orig):
    # function to run a RCM simulation

    atols = [1e-15, 1e-15, 1e-18]
    rtols = [1e-9, 1e-12, 1e-15]
    for attempt_index in range(0, len(atols)):

        t_end = 1.0  # time in seconds
        gas.TPX = T_orig, P_orig, X_orig

        env = ct.Reservoir(ct.Solution('air.yaml'))
        reactor = ct.IdealGasReactor(gas)
        wall = ct.Wall(reactor, env, A=1.0, velocity=0)
        reactor_net = ct.ReactorNet([reactor])
        reactor_net.atol = atols[attempt_index]
        reactor_net.rtol = rtols[attempt_index]

        times = [0]
        T = [reactor.T]
        P = [reactor.thermo.P]
        X = [reactor.thermo.X]  # mol fractions

        MAX_STEPS = 100000
        step_count = 0

        failed = False
        while reactor_net.time < t_end:
            # reactor_net.step()

            try:
                reactor_net.step()
            except ct._cantera.CanteraError:
                print(f'Reactor failed to solve on attempt {attempt_index}!')
                failed = True
                break

            times.append(reactor_net.time)
            T.append(reactor.T)
            P.append(reactor.thermo.P)
            X.append(reactor.thermo.X)

            step_count += 1
            if step_count > MAX_STEPS:
                print(f'Too many steps! Reactor failed to solve on attempt {attempt_index}!')
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                failed = True
                break

        if not failed:
            slopes = np.gradient(P, times)
            i = np.argmax(slopes)
            # check if we think it actually ignited in this time:
            ignited = False
            if np.max(P) / np.min(P) > 1.5:
                ignited = True
            if not ignited:
                return times[i] * -1.0  # indicates no ignition

            return times[i]
        print(f'That was attempt {attempt_index}. Trying again...')

    print(f'That was attempt {attempt_index}. Ran out of attempts to try.')
    return 0


def run_simulation(condition_index, perturbation_index=0):
    # Create the cantera model
    print(f'Running simulation {condition_index} with perturbation {perturbation_index}')

    new_species_list = []
    new_reaction_list = []
    for i in range(len(species_list)):
        new_species_list.append(species_list[i])
        if i in rmg_species_perturb_indices:
            perturb_species(new_species_list[i], G_perturbation_matrix[i, perturbation_index])
    for i in range(len(reaction_list)):
        new_reaction_list.append(reaction_list[i])
        if i in rmg_reaction_perturb_indices:
            perturb_reaction(new_reaction_list[i], k_perturbation_matrix[i, perturbation_index])

    job = rmgpy.tools.canteramodel.Cantera(species_list=new_species_list, reaction_list=new_reaction_list)
    job.load_model(allow_negative_A=True)
    X = conc_dicts[condition_index]
    delay = get_delay(job.model, experimental_Ts[condition_index], experimental_Ps[condition_index], X)
    return delay


# decide which chunk of the random sampling to handle
sample_start_index = int(sys.argv[1])

# read in the model
chemkin_file = os.path.join(basedir, 'chem_annotated.inp')
dict_file = os.path.join(basedir, 'species_dictionary.txt')
transport = os.path.join(basedir, 'tran.dat')

# load the uncertainty values so we know how much to perturb each parameter
species_uncertainty_file = os.path.join(basedir, 'gao_species_uncertainty.npy')
reaction_uncertainty_file = os.path.join(basedir, 'gao_reaction_uncertainty.npy')
delta_Gs = np.load(species_uncertainty_file)
delta_ks = np.load(reaction_uncertainty_file)

species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(chemkin_file, dictionary_path=dict_file, transport_path=transport)


# experimental conditions copied from subset of # https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
conc_dicts = [{
    'O2(2)': 0.2038,
    'butane(1)': 0.03135,
    'Ar': 0.7649
}] * 10
experimental_Ts = [700, 731, 756, 794, 840, 872, 906, 926, 959, 1000]
experimental_Ps = [1013250] * 10

# Map the species to the objects within the Uncertainty class
butane = rmgpy.species.Species(smiles='CCCC')
O2 = rmgpy.species.Species(smiles='[O][O]')
Ar = rmgpy.species.Species(smiles='[Ar]')
mapping = rmgpy.tools.canteramodel.get_rmg_species_from_user_species([butane, O2, Ar], species_list)

# Define the reaction conditions
reactor_type_list = ['IdealGasReactor']
mol_frac_list = [{mapping[butane]: 0.03135, mapping[O2]: 0.2038, mapping[Ar]: 0.7649}]
Tlist = ([700, 731, 756, 794, 840, 872, 906, 926, 959, 1000], 'K')
Plist = ([1013250] * 10, 'bar')
reaction_time_list = ([500], 'ms')


# Generate the perturbations
np.random.seed(400)
N_total = 10000
N_chunk = 100
G_means = np.zeros(len(species_list))
k_means = np.zeros(len(reaction_list))
delta_Gs_J_per_mol = delta_Gs * 4184
k_perturbation_matrix = np.random.normal(k_means, delta_ks, (N_total, len(reaction_list))).transpose()  # only perturb A Factor
G_perturbation_matrix = np.random.normal(G_means, delta_Gs_J_per_mol, (N_total, len(species_list))).transpose()


total_delays = np.zeros((N_chunk, len(experimental_Ts)))
for i in range(0, N_chunk):  # do N_chunk samples

    perturb_index = sample_start_index + i

    # Run 16 simulations in parallel
    delays = np.zeros(len(experimental_Ts))
    condition_indices = np.arange(0, len(experimental_Ts))
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(experimental_Ts)) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(run_simulation, condition_indices, [perturb_index] * len(condition_indices))):
            delays[condition_index] = delay_time
    total_delays[i, :] = delays

np.save(f'delays_{sample_start_index:04}.npy', total_delays)
