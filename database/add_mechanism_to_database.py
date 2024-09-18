# script to save the rankings for the mechanism
import os
import sys
import time
import pandas as pd

import rmgpy.chemkin
# script to save the rankings for the mechanism

sys.path.append(os.path.join(os.environ['AUTOSCIENCE_REPO'], 'database'))
import database_fun
import importlib


# Load New Mechanism
chemkin = sys.argv[1]
if os.path.isdir(chemkin):
    chemkin = os.path.join(chemkin, 'chem_annotated.inp')
elif chemkin.endswith('.yaml'):
    chemkin = chemkin.replace('.inp')

new_model_dir = os.path.dirname(chemkin)
# assumes species dictionary etc have the following names:
species_dict = os.path.join(new_model_dir, 'species_dictionary.txt')
transport = os.path.join(new_model_dir, 'tran.dat')
species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(chemkin, dictionary_path=species_dict, transport_path=transport, use_chemkin_names=True)

# Add species to database
database_fun.add_species_to_database(species_list)

# reimport to update species list
importlib.reload(database_fun)

# Add reactions to database
database_fun.add_reaction_to_database(reaction_list)
