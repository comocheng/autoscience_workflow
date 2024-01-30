# script to compile all of the csvs into a single array
# modified from reaction_calculator/delay_uncertainty/compile_sensitivity.ipynb
import os
import sys
import glob
import pandas as pd
import numpy as np


mech_file = sys.argv[1]
mech_dir = os.path.dirname(mech_file)

# compile everything into a humongous array
#             table1 table2 ... table12
# species 1
# species 2
# .........
# species N
# reaction 1
# reaction 2
# .........
# reaction M


# load examples to get the right size
test_sp_file = os.path.join(mech_dir, 'table_0007', 'species_delays_0007.npy')
test_rxn_file = os.path.join(mech_dir, 'table_0007', 'reaction_delays_0007_0000.npy')

K = 51
N = np.load(test_sp_file).shape[0]
M = np.load(test_rxn_file).shape[0]
print(f'N={N}', 'species')
print(f'M={M}', 'reactions')

all_delays_ever = np.zeros((N + M, 12 * K))


for table_index in range(1, 13):
    table_dir = os.path.join(mech_dir, f'table_{table_index:04}')

    rxn_files = glob.glob(os.path.join(table_dir, f'reaction_delays_{table_index:04}_*.npy'))

    # insert all the species delays for that table
    sp_file = os.path.join(table_dir, f'species_delays_{table_index:04}.npy')
    if not os.path.exists(sp_file):
        print(f'missing species delay file {sp_file}')
        continue
        raise OSError(f'missing species delay file {sp_file}')

    all_delays_ever[0:N, (table_index - 1) * K: table_index * K] = np.load(sp_file)

    # fill in the reaction files
    rxn_table = np.zeros((M, K))
    for i in range(0, 51):
        rxn_delay_file = os.path.join(table_dir, f'reaction_delays_{table_index:04}_{i * 50:04}.npy')
        if not os.path.exists(rxn_delay_file):
            print('missing: ', i, rxn_delay_file[-50:])
            continue  # TODO use assert and do not continue
        rxn_table += np.load(rxn_delay_file)
    all_delays_ever[N:, (table_index - 1) * K: table_index * K] = rxn_table


# save the resulting delay array
np.save(os.path.join(mech_dir, 'total_perturbed_mech_delays.npy'), all_delays_ever)


# Also compile the base delays into a giant 1 x (12 * K) array
total_base_delays = np.zeros(12 * K)
for table_index in range(1, 13):
    table_dir = os.path.join(mech_dir, f'table_{table_index:04}')
    base_delay_file = os.path.join(table_dir, f'base_delays_{table_index:04}.npy')
    if not os.path.exists(base_delay_file):
        print(f'Missing base delay file {base_delay_file}')
        continue
        raise OSError(f'Missing base delay file {base_delay_file}')

    total_base_delays[(table_index - 1) * K:table_index * K] = np.load(base_delay_file)
# save the resulting base delay array
np.save(os.path.join(mech_dir, 'total_base_delays.npy'), total_base_delays)
