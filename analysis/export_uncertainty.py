# script to export mechanism uncertainty data to npy files

# Instructions:
# 1. Change the libraries to match the input file libraries
# 2. RMG-database should be on the same commit as the one used to run RMG
# 3. RMG-Py should be on the autoscience_uncertainties branch
# 4. Run the script by calling: python-jl export_uncertainty.py path/to/chem_annotated.inp

import os
import sys
import numpy as np
import rmgpy.tools.uncertainty


# Pass in the chem_annotated.inp file
chemkin = sys.argv[1]
mech_dir = os.path.dirname(chemkin)
species_dict = os.path.join(mech_dir, 'species_dictionary.txt')

# --------------- CAUTION!!! Databases here must match the exact order of the ones used to generate the mechanism
thermo_libs = [  # <------------------------- edit these to match input file libraries
    'BurkeH2O2',
    'primaryThermoLibrary',
]

kinetic_libs = [  # <------------------------- edit these to match input file libraries
    'BurkeH2O2inN2',
]
# ----------------------------------------------------------------------------

DFT_THERMO_UNCERTAINTY = 3.0
DFT_KINETIC_UNCERTAINTY = 1 / np.sqrt(3) * np.log(10)
calculated_thermo_libs = [
    'harris_butane'  # <----- edit these to match name of thermo library calculated during this workflow
]

calculated_kinetic_libs = [
    'harris_butane'  # <----- edit these to match names of kinetics libraries calculated during this workflow
]


uncertainty = rmgpy.tools.uncertainty.Uncertainty(output_directory=os.path.join(mech_dir, 'rmg_uncertainty'))
uncertainty.load_model(chemkin, species_dict)

uncertainty.load_database(
    thermo_libraries=thermo_libs,
    kinetics_families='default',
    reaction_libraries=kinetic_libs,
    kinetics_depositories=['training'],
)

# Get the different kinetic and thermo sources
uncertainty.extract_sources_from_model()
uncertainty.assign_parameter_uncertainties()


# change values of parameters calculated by this workflow
# RMG automatically estimates uncertainty as 0.5 for kinetics libraries
# but should be closer to ~1.1 for this workflow
for i in range(len(uncertainty.species_list)):
    if 'Thermo library: ' in uncertainty.species_list[i].thermo.comment:
        thermo_library = uncertainty.species_list[i].thermo.comment[len('Thermo library: '):]
        if thermo_library.lower() in calculated_thermo_libs:
            uncertainty.thermo_input_uncertainties[i] = DFT_THERMO_UNCERTAINTY

for i in range(len(uncertainty.species_list)):
    if hasattr(uncertainty.reaction_list[i], 'library'):
        if uncertainty.reaction_list[i].library.lower() in calculated_kinetic_libs:
            uncertainty.kinetic_input_uncertainties[i] = DFT_KINETIC_UNCERTAINTY


np.save(os.path.join(mech_dir, 'gao_reaction_uncertainty.npy'), uncertainty.kinetic_input_uncertainties)
np.save(os.path.join(mech_dir, 'gao_species_uncertainty.npy'), uncertainty.thermo_input_uncertainties)
