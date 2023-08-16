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
working_dir = os.path.join(os.path.dirname(chemkin))
# working_dir = '/work/westgroup/harris.se/autoscience/reaction_calculator/fs_sensitivity/base_rmg_1week'
MAX_WORKERS = 16


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
    increase = None
    for poly in species.thermo.polynomials:
        new_coeffs = poly.coeffs
        if not increase:
            # Only define the increase in enthalpy once or you'll end up with numerical gaps in continuity
            increase = delta * new_coeffs[5]
        new_coeffs[5] += increase
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
