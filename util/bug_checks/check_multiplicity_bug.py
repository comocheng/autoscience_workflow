# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import os
import re
import glob
DFT_DIR = os.environ['DFT_DIR']
import sys
sys.path.append(DFT_DIR)
import autotst_wrapper


# -

# code snippet to check a log file for Multiplicity = 1 (bad for TS)
def find_multiplicity(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    pattern = r'Multiplicity = (\d+)'
    for line in lines:
        m1 = re.search(pattern, line)
        if m1 is not None:
            return int(m1[1])

    return -1


# Check completed kinetics
final_logs = sorted(glob.glob(os.path.join(DFT_DIR, 'kinetics', f'reaction_*', 'arkane', 'ts', 'freq.log')))
for final_log in final_logs:
    assert find_multiplicity(final_log) > 1
    # print(final_log)
print('All completed reactions have correct multiplicity')

# check completed thermo
thermo_logs = sorted(glob.glob(os.path.join(DFT_DIR, 'thermo', f'species_*', 'arkane', 'freq.log')))
for thermo_log in thermo_logs:
    multiplicity = find_multiplicity(thermo_log)
    
    species_index = autotst_wrapper.get_species_index_from_path(thermo_log)
    ref_species = autotst_wrapper.database_fun.index2species(species_index)
    assert ref_species.multiplicity == multiplicity
    # print(species_index)
print('All completed species have correct multiplicity')


