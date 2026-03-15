# script to compile all of the species and reaction sensitivity npts into a single npy
# notebook to compile all of the csvs into a single array
import os
import yaml
import numpy as np

import cantera as ct


mech_file = sys.argv[1]

if os.path.isdir(mech_file):
    working_dir = mech_file
    mech_file = os.path.join('working_dir', 'chem_annotated.yaml')
else:
    working_dir = os.path.dirname(mech_file)
    mech_file = mech_file.replace('.inp', '.yaml')

# Check dimensions
gas = ct.Solution(mech_yaml)

# check the size
conditions_dict_path = os.path.join(working_dir, 'sim_config.yaml')
if not os.path.exists(conditions_dict_path):
    logging.warning(f'Expected to find sim_config.yaml at {conditions_dict_path} but it does not exist. Please copy it to the directory with your mech file.')
    raise FileNotFoundError(f'sim_config.yaml not found at {conditions_dict_path}')

with open(conditions_dict_path) as f:
    conditions_dict = yaml.safe_load(f)

base_delays = np.load(os.path.join(working_dir, 'sensitivity', 'base_delays.npy'))
sample_spec_delays = np.load(os.path.join(working_dir, 'sensitivity', 'spec_delay_0000.npy'))
sample_reaction_delays = np.load(os.path.join(working_dir, 'sensitivity', 'reaction_delay_000000.npy'))


K = len(conditions_dict['sensitivity_points'])
assert len(base_delays) == K
assert len(sample_spec_delays) == K
assert len(sample_reaction_delays) == K



# Build big table of sensitivity delays
perturbed_delays = np.zeros((gas.n_species + gas.n_reactions, K))

for i in range(gas.n_species):
    spec_file = os.path.join(working_dir, 'sensitivity', f'spec_delay_{i:04}.npy')
    if not os.path.exists(spec_file):
        print(f'missing species {i:04}')
        continue
    perturbed_delays[i, :] = np.load(spec_file)

for i in range(gas.n_reactions):
    rxn_file = os.path.join(working_dir, 'sensitivity', f'reaction_delay_{i:06}.npy')
    if not os.path.exists(rxn_file):
        print(f'missing reaction {i:06}')
        continue
    perturbed_delays[gas.n_species + i, :] = np.load(rxn_file)


# save the resulting delay array
np.save(os.path.join(working_dir, 'total_perturbed_mech_delays.npy'), perturbed_delays)
