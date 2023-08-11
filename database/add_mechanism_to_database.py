# script to save the rankings for the mechanism
import os
import sys
import pandas as pd

import rmgpy.chemkin


total_species_list = []  # define in a global context


def get_unique_species_index(species):
    for i in range(len(total_species_list)):
        if species.is_isomorphic(total_species_list[i]):
            return i
    raise IndexError('Species not in database')


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


# Load New Mechanism
chemkin = sys.argv[1]
new_model_dir = os.path.dirname(chemkin)
# assumes species dictionary etc have the following names:
species_dict = os.path.join(new_model_dir, 'species_dictionary.txt')
transport = os.path.join(new_model_dir, 'tran.dat')
species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(chemkin, dictionary_path=species_dict, transport_path=transport, use_chemkin_names=True)

# ----------------------------- Add Species ---------------------------- #
# Load Species Database
DFT_DIR = '/work/westgroup/harris.se/autoscience/reaction_calculator/dft'
species_csv = os.path.join(DFT_DIR, 'species_database.csv')
species_df = pd.read_csv(species_csv)

print(f'Species database contains {len(species_df)} unique species')
# Check if there are any new species:
species_to_add = []
for i, new_sp in enumerate(species_list):
    already_exists = False
    for db_species_adj_list in species_df['adjacency_list'].values:
        db_sp = rmgpy.species.Species().from_adjacency_list(db_species_adj_list)
        if db_sp.is_isomorphic(new_sp):
            already_exists = True
            break
    if already_exists:
        continue
    species_to_add.append(new_sp)


# add the new species
print('Added the following species to the database:')
addition_index = 0
for k, new_sp in enumerate(species_to_add):

    # first check that it's unique compared to everything before it in species_to_add
    is_unique = True
    for m in range(k):
        if new_sp.is_isomorphic(species_to_add[m]):
            is_unique = False
            break
    if not is_unique:
        continue

    name = new_sp.label
    smiles = new_sp.smiles
    # the split is for weird bug? where multiple adjacency lists end up in the species_list for a single species
    # maybe-only if you use chemkin names when loading the chemking
    adjacency_list = new_sp.to_adjacency_list().split('\n\n\n')[0]
    i = addition_index + len(species_df)

    print(f'\t{name}')
    species_df = species_df.append({'i': i, 'name': name, 'SMILES': smiles, 'adjacency_list': adjacency_list}, ignore_index=True)
    addition_index += 1

print('Saving new species database...')
species_df.to_csv(species_csv, index=False)

# load it back in to test that it worked
species_df = pd.read_csv(species_csv)
print(f'Species database now contains {len(species_df)} unique species')

# ----------------------------- Add Reactions ---------------------------- #
reaction_csv = os.path.join(DFT_DIR, 'reaction_database.csv')
reaction_df = pd.read_csv(reaction_csv)

print(f'Reaction database contains {len(reaction_df)} unique reactions')

# populate total species list
total_species_list = [rmgpy.species.Species().from_adjacency_list(adj_list) for adj_list in species_df['adjacency_list'].values]


# check if there are any new reactions to add
entries_to_add = []
print('Looking for new reactions in mechanism...')
for j in range(len(reaction_list)):
    unique_string = get_unique_string(reaction_list[j])
    already_exists = False
    for database_str in reaction_df['unique_string'].values:
        if unique_string == database_str:
            already_exists = True
            break
    if not already_exists:
        entries_to_add.append([j, unique_string])
print(f'Found {len(entries_to_add)} new reactions')

print('Added the following new reactions to the database:')
# actually add the new reactions
addition_index = 0
for j in range(len(entries_to_add)):
    rmg_index = entries_to_add[j][0]
    unique_string = entries_to_add[j][1]
    # make sure the 'unique_string' is actually unique compared to everything that came before it
    already_exists = False
    for k in range(j):
        # compare unique_string
        if entries_to_add[k][1] == unique_string:
            already_exists = True
            break
    if already_exists:
        continue

    name = str(reaction_list[rmg_index])
    smiles = reaction2smiles(reaction_list[rmg_index])
    i = len(reaction_df) + addition_index

    print(f'\t{name}')
    reaction_df = reaction_df.append({'i': i, 'name': name, 'SMILES': smiles, 'unique_string': unique_string}, ignore_index=True)
    addition_index += 1

print('Saving new reaction database...')
reaction_df.to_csv(reaction_csv, index=False)

# load it back in to test that it worked
reaction_df = pd.read_csv(reaction_csv)
print(f'Reaction database now contains {len(reaction_df)} unique reactions')
