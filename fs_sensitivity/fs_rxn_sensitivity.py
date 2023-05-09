# script to run all flame speed sensitivities
import os
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import sys
import rmgpy.chemkin
import subprocess


chemkin = sys.argv[1]
rxn_index_start = int(sys.argv[2])  # start index for SLURM parallelization
working_dir = os.path.join(os.path.dirname(chemkin))


def same_reaction(rxn1, rxn2):
    """Returns true IFF reactions have same reactants, products, and type"""
    if rxn1.reactants == rxn2.reactants and rxn1.products == rxn2.products and type(rxn1) == type(rxn2):
        return True
    else:
        return False


# perturb every species and reaction in the mechanism
# we'll select the perturbations one at a time later in the script
def perturb_species(species, delta):
    # takes in an RMG species object
    # change the enthalpy offset
    for poly in species.thermo.polynomials:
        new_coeffs = poly.coeffs
        new_coeffs[5] *= (1.0 + delta)
        poly.coeffs = new_coeffs


def perturb_reaction(rxn, delta):
    # takes in an RMG reaction object
    # delta is the ln(k) amount to perturb the A factor
    # delta is a multiplicative factor- units don't matter, yay!
    # does not deepycopy because there's some issues with rmgpy.reactions copying
    rxn.kinetics.A.value *= np.exp(delta)


transport = os.path.join(working_dir, 'tran.dat')
species_dict = os.path.join(working_dir, 'species_dictionary.txt')
species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(chemkin, dictionary_path=species_dict, transport_path=transport)
print(f'Loaded {len(species_list)} species, {len(reaction_list)} reactions')
base_cti_path = os.path.join(working_dir, 'base.cti')
perturbed_chemkin = os.path.join(working_dir, 'perturbed.inp')
perturbed_cti_path = os.path.join(working_dir, 'perturbed.cti')


skip_create_perturb = False
if os.path.exists(perturbed_cti_path):
    skip_create_perturb = True
    print('Perturbed cti already exists, skipping creation of perturbed mechanism')


if not skip_create_perturb:
    # load the chemkin file and create a normal and perturbed cti for simulations:
    # # write base cantera
    subprocess.run(['ck2cti', f'--input={chemkin}', f'--transport={transport}', f'--output={base_cti_path}'])

    delta = 0.1
    for i in range(0, len(species_list)):
        perturb_species(species_list[i], delta)

    for i in range(0, len(reaction_list)):
        try:
            perturb_reaction(reaction_list[i], delta)
        except AttributeError:
            continue

    # save the results
    rmgpy.chemkin.save_chemkin_file(perturbed_chemkin, species_list, reaction_list, verbose=True, check_for_duplicates=True)
    subprocess.run(['ck2cti', f'--input={perturbed_chemkin}', f'--transport={transport}', f'--output={perturbed_cti_path}'])

# load the 2 ctis
base_gas = ct.Solution(base_cti_path)
perturbed_gas = ct.Solution(perturbed_cti_path)


# load the experimental conditions
flame_speed_data = '/work/westgroup/harris.se/autoscience/autoscience/butane/experimental_data/butane_flamespeeds.csv'
flame_speed_data = '/home/moon/autoscience/autoscience/butane/experimental_data/butane_flamespeeds.csv'
df_exp = pd.read_csv(flame_speed_data)


# get just the Park data
data_slice = df_exp[df_exp['Reference'] == 'Park et al. 2016']
N = 51
phi_min = 0.6
phi_max = 2.0
equiv_ratios = np.linspace(phi_min, phi_max, N)
temperatures = np.ones(len(equiv_ratios)) * data_slice['Tu (K)'].values[0]
pressures = np.ones(len(equiv_ratios)) * data_slice['Pu (atm)'].values[0] * ct.one_atm

# compute and save the delays
reaction_flamespeeds = np.zeros((len(perturbed_gas.reactions()), len(equiv_ratios)))


# list of starting conditions
# Define stoichiometric coefficients
v_fuel = 1.0
v_oxidizer = 13.0 / 2.0
v_N2 = 0.79 * (v_oxidizer / 0.21)  # air is approximately 79% N2 and 21% O2

# calculate actual ratio of fuel to oxidizer
actual_ratio = equiv_ratios * (v_fuel / v_oxidizer)
# start with 1.0 oxidizer, then normalize
x_O2 = 1.0
x_C4H10 = actual_ratio * x_O2
x_N2 = 0.79 * (x_O2 / .21)
total = x_O2 + x_C4H10 + x_N2
x_O2 = x_O2 / total
x_C4H10 = x_C4H10 / total
x_N2 = x_N2 / total

concentrations = [{'butane(1)': x_C4H10[i], 'O2(2)': x_O2[i], 'N2': x_N2[i]} for i in range(0, len(equiv_ratios))]


# function for running a flame speed
# assumes gas has been properly initialized
def run_flame_speed(condition_index):

    # fix species names for aramco
    if 'butane(1)' not in base_gas.species_names and 'butane(1)' in concentrations[condition_index].keys():
        # check the keys to make sure we don't pop twice TODO should be O2 not in keys
        concentrations[condition_index]['C4H10'] = concentrations[condition_index].pop('butane(1)')
    if 'O2(2)' not in base_gas.species_names and 'O2(2)' in concentrations[condition_index].keys():
        concentrations[condition_index]['O2'] = concentrations[condition_index].pop('O2(2)')
    if 'CO2(7)' not in base_gas.species_names and 'CO2(7)' in concentrations[condition_index].keys():
        concentrations[condition_index]['CO2'] = concentrations[condition_index].pop('CO2(7)')
    if 'Ar' not in base_gas.species_names and 'Ar' in concentrations[condition_index].keys():
        concentrations[condition_index]['AR'] = concentrations[condition_index].pop('Ar')

    base_gas.TPX = temperatures[condition_index], pressures[condition_index], concentrations[condition_index]

    tol_ss = [1.0e-13, 1.0e-9]  # abs and rel tolerances for steady state problem
    tol_ts = [1.0e-13, 1.0e-9]  # abs and rel tie tolerances for time step function

    width = 0.08
    flame = ct.FreeFlame(base_gas, width=width)
    flame.flame.set_steady_tolerances(default=tol_ss)   # set tolerances
    flame.flame.set_transient_tolerances(default=tol_ts)
    # flame.set_refine_criteria(ratio=5, slope=0.25, curve=0.27)  # loose
    flame.set_refine_criteria(ratio=2, slope=0.01, curve=0.01, prune=0.001)  # tight
    # flame.max_time_step_count = 5000
    flame.max_time_step_count = 5000
    loglevel = 1

    # set up from previous run
    h5_filepath_guess = os.path.join(working_dir, f"saved_flame_{condition_index}.h5")
    if os.path.exists(h5_filepath_guess):
        print('Loading initial flame conditions from', h5_filepath_guess)
        print("Load initial guess from HDF file via SolutionArray")
        arr2 = ct.SolutionArray(base_gas)
        # the flame domain needs to be specified as subgroup
        arr2.read_hdf(h5_filepath_guess, group="freeflame", subgroup="flame", force=True)
        flame.set_initial_guess(data=arr2)

    else:
        # print('Initial flame conditions not found, using default')
        raise OSError

    print("about to solve")
    flame.solve(loglevel=loglevel, auto=True)
    Su = flame.velocity[0]

    # Too many to run to save h5 files
    # print("Save HDF")
    # hdf_filepath = os.path.join(working_dir, f"perturbed_flame_{condition_index}.h5")
    # flame.write_hdf(
    #     hdf_filepath,
    #     group="freeflame",
    #     mode="w",
    #     quiet=False,
    #     description=("butane flame"),
    # )
    return Su


for i in range(rxn_index_start, min(rxn_index_start + 50, len(perturbed_gas.reactions()))):
    print(f'perturbing {i} {perturbed_gas.reactions()[i]}')
    # TODO skip the ones that haven't actually been perturbed because PDEP or whatever
    try:
        a = base_gas.reactions()[i].rate
    except AttributeError:
        print(f'skipping reaction {i}: {base_gas.reactions()[i]} because it is not perturbed from the base mechanism')
        continue

    # load the base gas
    base_gas = ct.Solution(base_cti_path)
    # order is not preserved between the mechanisms, so we have to find the reaction that matches
    if same_reaction(perturbed_gas.reactions()[i], base_gas.reactions()[i]):
        perturbed_index = i
    else:
        for k in range(0, len(base_gas.reactions())):
            if same_reaction(perturbed_gas.reactions()[k], base_gas.reactions()[i]):
                perturbed_index = k
                break
        else:
            raise ValueError('Could not find matching reaction in base mechanism')

    base_gas.modify_reaction(i, perturbed_gas.reactions()[perturbed_index])

    # Run all simulations in parallel
    flame_speeds = np.zeros(len(equiv_ratios))
    condition_indices = np.arange(0, len(equiv_ratios))
    with concurrent.futures.ProcessPoolExecutor(max_workers=26) as executor:
        for condition_index, flame_speed in zip(condition_indices, executor.map(
            run_flame_speed,
            condition_indices)
        ):
            flame_speeds[condition_index] = flame_speed

np.save(os.path.join(f'flame_speeds_{rxn_index_start:04}.npy'), flame_speeds)
