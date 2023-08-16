# set of functions related to thermokinetic calculations

import os
import sys
import numpy as np
import pandas as pd

import rmgpy.reaction
import rmgpy.species

try:
    DFT_DIR = os.environ['DFT_DIR']
except KeyError:
    DFT_DIR = "/work/westgroup/harris.se/autoscience/reaction_calculator/dft"
    # DFT_DIR = "/home/moon/autoscience/reaction_calculator/dft"


def species_index2smiles(species_index):
    """Function to return species smiles given a species index
    looks up the results in the species_list.csv
    """
    species_csv = os.path.join(DFT_DIR, 'species_list.csv')
    species_df = pd.read_csv(species_csv)
    species_index = species_df['SMILES'].values[species_index]
    return species_index


def species_smiles2index(species_smiles):
    """Function to return species index given a species smiles
    looks up the results in the species_list.csv
    """
    species_csv = os.path.join(DFT_DIR, 'species_list.csv')
    species_df = pd.read_csv(species_csv)
    try:
        species_index = species_df[species_df['SMILES'] == species_smiles]['i'].values[0]
        return species_index
    except IndexError:
        import rmgpy.species
        # now we need to check all the species for isomorphism
        ref_sp = rmgpy.species.Species(smiles=species_smiles)
        for i in range(0, len(species_df)):
            sp = rmgpy.species.Species(smiles=species_df['SMILES'].values[i])
            resonance = sp.generate_resonance_structures()
            if resonance:
                sp = resonance
            else:
                sp = [sp]
            for compare_sp in sp:
                if ref_sp.is_isomorphic(compare_sp):
                    return i
        print(f'could not identify species {species_smiles}')


def reaction_index2smiles(reaction_index):
    """Function to return reaction smiles given a reaction index
    looks up the results in the reaction_list.csv
    """
    reaction_csv = os.path.join(DFT_DIR, 'reaction_list.csv')
    reaction_df = pd.read_csv(reaction_csv)
    reaction_smiles = reaction_df['SMILES'].values[reaction_index]
    return reaction_smiles


def reaction2smiles(reaction):
    """Takes an RMG reaction and returns the smiles representation
    """
    string = ""
    for react in reaction.reactants:
        if isinstance(react, rmgpy.species.Species):
            string += f"{react.molecule[0].to_smiles()}+"
        elif isinstance(react, rmgpy.molecule.Molecule):
            string += f"{react.to_smiles()}+"
    string = string[:-1]
    string += "_"
    for prod in reaction.products:
        if isinstance(prod, rmgpy.species.Species):
            string += f"{prod.molecule[0].to_smiles()}+"
        elif isinstance(prod, rmgpy.molecule.Molecule):
            string += f"{prod.to_smiles()}+"
    label = string[:-1]
    return label


def smiles2reaction(reaction_smiles):
    """Takes the reaction smiles and produces a corresponding rmg reaction
    """
    reaction = rmgpy.reaction.Reaction()
    reactants = []
    products = []

    # handle CO case
    if '[C-]#[O+]' in reaction_smiles:
        CO = rmgpy.species.Species(smiles='[C-]#[O+]')
        reaction_smiles = reaction_smiles.replace('[C-]#[O+]', 'carbonmonoxide')
    if '[O-][N+]#C' in reaction_smiles:
        CHNO = rmgpy.species.Species(smiles='[O-][N+]#C')
        reaction_smiles = reaction_smiles.replace('[O-][N+]#C', 'formonitrileoxide')
    if '[O-][N+]=C' in reaction_smiles:
        CH2NO = rmgpy.species.Species(smiles='[O-][N+]=C')
        reaction_smiles = reaction_smiles.replace('[O-][N+]=C', 'methylenenitroxide')

    reactant_token = reaction_smiles.split('_')[0]
    product_token = reaction_smiles.split('_')[1]

    reactant_tokens = reactant_token.split('+')
    product_tokens = product_token.split('+')

    # print(product_tokens)
    for reactant_str in reactant_tokens:
        if reactant_str == 'carbonmonoxide':
            reactant_str = '[C-]#[O+]'
        elif reactant_str == 'formonitrileoxide':
            reactant_str = '[O-][N+]#C'
        elif reactant_str == 'methylenenitroxide':
            reactant_str = '[O-][N+]=C'
        reactant = rmgpy.species.Species(smiles=reactant_str)
        reactants.append(reactant)

    for product_str in product_tokens:
        if product_str == 'carbonmonoxide':
            product_str = '[C-]#[O+]'
        elif product_str == 'formonitrileoxide':
            product_str = '[O-][N+]#C'
        elif product_str == 'methylenenitroxide':
            ptoduct_str = '[O-][N+]=C'
        # print(product_str)
        product = rmgpy.species.Species(smiles=product_str)
        products.append(product)

    reaction.reactants = reactants
    reaction.products = products
    return reaction


def reaction_smiles2index(reaction_smiles):
    """Function to return reaction index given a smiles reaction
    doesn't necessarily have to be in the right order
    RMG reaction will check for isomorphism
    """
    # first check to see if the exact smiles is in the CSV
    reaction_csv = os.path.join(DFT_DIR, 'reaction_list.csv')
    reaction_df = pd.read_csv(reaction_csv)
    if reaction_smiles in reaction_df['SMILES'].values:
        idx = np.where(reaction_df['SMILES'].values == reaction_smiles)[0][0]
        return reaction_df['i'].values[idx]
    else:
        # use rmgpy.reaction to check for isomorphism
        ref_reaction = smiles2reaction(reaction_smiles)
        for i in range(0, len(reaction_df)):
            csv_reaction = smiles2reaction(reaction_df['SMILES'].values[i])
            if ref_reaction.is_isomorphic(csv_reaction):
                return i
    # reaction not found
    return -1
