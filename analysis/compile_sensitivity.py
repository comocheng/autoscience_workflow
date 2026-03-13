# script to compile all of the csvs into a single array
# modified from reaction_calculator/delay_uncertainty/compile_sensitivity.ipynb
import os
import sys
import glob
import pandas as pd
import numpy as np


mech_file = sys.argv[1]

if os.path.isdir(mech_file):
    mech_dir = mech_file
else:
    mech_dir = os.path.dirname(mech_file)

main_table = 7
if len(sys.argv) > 2:
    main_table = int(sys.argv[2])

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

main_table = 7
# Compile the species sensitivities if that hasn't been done yet
sp_delay_file = os.path.join(mech_dir, f'table_{main_table:04}', f'species_delays_{main_table:04}.npy')
if not os.path.exists(sp_delay_file):
    sp_files = glob.glob(os.path.join(mech_dir, f'table_{main_table:04}', f'spec_delay_{main_table:04}_*.npy'))
    N = len(sp_files)
    K = 51
    spec_delays = np.zeros((N, K))
    for i in range(N):
        spec_delays[i, :] = np.load(os.path.join(mech_dir, f'table_{main_table:04}', f'spec_delay_{main_table:04}_{i:04}.npy'))
    np.save(os.path.join(mech_dir, f'table_{main_table:04}', f'species_delays_{main_table:04}.npy'), spec_delays)
else:
    spec_delays = np.load(sp_delay_file)

# load examples to get the right size
test_sp_file = os.path.join(mech_dir, f'table_{main_table:04}', f'species_delays_{main_table:04}.npy')
test_rxn_file = os.path.join(mech_dir, f'table_{main_table:04}', f'reaction_delays_{main_table:04}_0000.npy')

N_REACTIONS_PER_FILE = 10

K = 51
N = spec_delays.shape[0]
M = np.load(test_rxn_file).shape[0]
print(f'N={N}', 'species')
print(f'M={M}', 'reactions')

all_delays_ever = np.zeros((N + M, 12 * K))

# for table_index in range(1, 13):
for table_index in [7]:
    table_dir = os.path.join(mech_dir, f'table_{table_index:04}')

    rxn_files = glob.glob(os.path.join(table_dir, f'reaction_delays_{table_index:04}_*.npy'))

    all_delays_ever[0:N, (table_index - 1) * K: table_index * K] = spec_delays

    # fill in the reaction files
    rxn_table = np.zeros((M, K))
    for i in range(0, int(3500 / N_REACTIONS_PER_FILE)):
        rxn_delay_file = os.path.join(table_dir, f'reaction_delays_{table_index:04}_{i * N_REACTIONS_PER_FILE:04}.npy')
        if not os.path.exists(rxn_delay_file):
            print('missing: ', i, rxn_delay_file)
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

np.save(os.path.join(mech_dir, 'total_base_delays.npy'), total_base_delays)
