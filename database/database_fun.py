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
    """warning, this has the potential to be incorrect if species_df is modified later on
    but the speed advantages from generating total_species_list once on import are worth the risk
    """
    for j in range(len(total_species_list)):
        if species.is_isomorphic(total_species_list[j]):
            return int(species_df['i'].values[j])
    raise IndexError(f'Species {str(species)} not in database')


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


def index2adj_list(index):
    """Function to return species adjacency list given a species database index
    """
    return species_df[species_df['i'] == index]['adjacency_list'].values[0]


def index2species(index):
    """Function to return species object given a species database index
    """
    return rmgpy.species.Species().from_adjacency_list(index2adj_list(index))


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


def reaction_index2smiles(reaction_index):
    reaction_df = pd.read_csv(os.path.join(DFT_DIR, 'reaction_database.csv'))
    return reaction_df[reaction_df['i'] == reaction_index]['SMILES'].values[0]


def index2reaction(reaction_index):
    reaction_df = pd.read_csv(os.path.join(DFT_DIR, 'reaction_database.csv'))
    unique_string = reaction_df[reaction_df['i'] == reaction_index]['unique_string'].values[0]

    reactants_string = unique_string.split('=')[0]
    reactants_tokens = reactants_string.split('+')
    reactants_indices = [int(i) for i in reactants_tokens]
    reactants = [index2species(i) for i in reactants_indices]

    products_string = unique_string.split('=')[1]
    products_tokens = products_string.split('+')
    products_indices = [int(i) for i in products_tokens]
    products = [index2species(i) for i in products_indices]

    new_reaction = rmgpy.reaction.Reaction()
    new_reaction.reactants = reactants
    new_reaction.products = products
    return new_reaction


def add_species_to_database(species_list):
    """Takes a list of RMG species and adds only the new species to the databse
    """
    # Check if there are any new species:
    species_to_add = []

    # reload the species database just in case we're working with a stale version
    species_csv = os.path.join(DFT_DIR, 'species_database.csv')
    species_df = pd.read_csv(species_csv)
    print(f'Loaded species database contains {len(species_df)} unique species')
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

        print(f'\t{name}')
        species_df = species_df.append({'i': len(species_df), 'name': name, 'SMILES': smiles, 'adjacency_list': adjacency_list}, ignore_index=True)

    print('Saving new species database...')
    with open(species_csv, "w", newline="") as f:
        species_df.to_csv(species_csv, index=False)
        f.flush()

    # load it back in to test that it worked
    species_df = pd.read_csv(species_csv)
    print(f'Species database now contains {len(species_df)} unique species')


def add_reaction_to_database(reaction_list):
    # reload reaction_df and species_df fresh:
    # species_df = pd.read_csv(os.path.join(DFT_DIR, 'species_database.csv'))
    # total_species_list = [rmgpy.species.Species().from_adjacency_list(adj_list) for adj_list in species_df['adjacency_list'].values]
    # print(f'Reloaded species database contains {len(species_df)} unique species')

    reaction_csv = os.path.join(DFT_DIR, 'reaction_database.csv')
    reaction_df = pd.read_csv(reaction_csv)
    print(f'Loaded reaction database contains {len(reaction_df)} unique reactions')

    print('Looking for new reactions in mechanism...')
    entries_to_add = []
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

        print(f'\t{name}')
        next_i = reaction_df['i'].values[-1] + 1
        reaction_df = reaction_df.append({'i': next_i, 'name': name, 'SMILES': smiles, 'unique_string': unique_string}, ignore_index=True)

    print('Saving new reaction database...')
    reaction_df.to_csv(reaction_csv, index=False)

    # load it back in to test that it worked
    reaction_df = pd.read_csv(reaction_csv)
    print(f'Reaction database now contains {len(reaction_df)} unique reactions')
