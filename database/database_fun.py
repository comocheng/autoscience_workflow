# A module to contain some useful functions for database operations
# the goal is to avoid copying code from the various scripts.
# they can all make use of the functions here, which ideally has a very lightweight set of dependencies
import os
import pandas as pd
import rmgpy.reaction


try:
    DFT_DIR = os.environ['DFT_DIR']
except KeyError:
    print('using default DFT_DIR')
    DFT_DIR = '/work/westgroup/harris.se/autoscience/reaction_calculator/dft'

species_df = pd.read_csv(os.path.join(DFT_DIR, 'species_database.csv'))

total_species_list = [rmgpy.species.Species().from_adjacency_list(adj_list) for adj_list in species_df['adjacency_list'].values]


def get_unique_species_index(species):
    for j in range(len(total_species_list)):
        if species.is_isomorphic(total_species_list[j]):
            return int(species_df['i'].values[j])
    raise IndexError('Species not in database')


def get_unique_reaction_index(reaction):
    reaction_df = pd.read_csv(os.path.join(DFT_DIR, 'reaction_database.csv'))
    unique_string = get_unique_string(reaction)
    for j in range(len(reaction_df)):
        if unique_string == reaction_df['unique_string'].values[j]:
            return int(reaction_df['i'].values[j])
    raise IndexError('Reaction not in database')


def get_unique_string(reaction):
    """Returns the unique string for a given reaction
    Looks up unique species indices in the species index (based on adjacenecy list)
    and returns the result in sorted order, something like 12+300=14+303
    """
    reactants = []
    for sp in reaction.reactants:
        sp_index = get_unique_species_index(sp)
        reactants.append(sp_index)
    products = []
    for sp in reaction.products:
        sp_index = get_unique_species_index(sp)
        products.append(sp_index)
    reactants.sort()
    products.sort()

    reactants = [str(sp) for sp in reactants]
    products = [str(sp) for sp in products]
    unique_string = '+'.join(reactants) + '=' + '+'.join(products)
    return unique_string


def reaction2smiles(reaction):
    """Takes an RMG reaction and returns the smiles representation
    This is not sorted and therefore not unique, also smiles isn't unique to begin with
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
