# script to run many flame speeds
import os
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import sys
import yaml


if len(sys.argv) > 1:
    cti_path = sys.argv[1]
else:
    raise ValueError

ratio = 5
slope = 0.25
curve = 0.27

gas = ct.Solution(cti_path)


this_dir = os.path.dirname(__file__)
mechs = {
    'AramcoMech3.0': 'aramco',
    'chem_annotated': 'base_rmg',
    'chem_annotated.': 'base_rmg',
    'cutoff3_20230113': 'improved_model',
    'cutoff3_20230418': 'improved_model',
    'cutoff3_20230113.': 'improved_model',
    'cutoff3_20230418.': 'improved_model',
}

save_dir = os.path.join(this_dir, mechs[os.path.basename(cti_path)[:-4]])
os.makedirs(save_dir, exist_ok=True)


# load the experimental conditions
flame_speed_data = '/work/westgroup/harris.se/autoscience/autoscience/butane/experimental_data/butane_flamespeeds.csv'
df_exp = pd.read_csv(flame_speed_data)

# get just the Park data
data_slice = df_exp[df_exp['Reference'] == 'Park et al. 2016']

# Define Initial conditions using experimental data
speeds = data_slice['SL0 (cm/s)'].values.astype(float)  # ignition delay
temperatures = data_slice['Tu (K)'].values  # Temperatures
pressures = data_slice['Pu (atm)'].values * ct.one_atm  # pressures in atm
equiv_ratios = data_slice['Equivalence Ratio'].values  # equivalence ratio


# list of starting conditions
# Define stoichiometric coefficients
v_fuel = 1.0
v_oxidizer = 13.0 / 2.0
v_N2 = 0.79 * (v_oxidizer / 0.21)  # air is approximately 79% N2 and 21% O2

# calculate actual ratio of fuel to oxidizer
actual_ratio = equiv_ratios * (v_fuel / v_oxidizer)


# start with 1.0 oxidizer, then normalize
x_O2 = 1.0
x_C4H10 = actual_ratio * x_O2
x_N2 = 0.79 * (x_O2 / .21)
total = x_O2 + x_C4H10 + x_N2
x_O2 = x_O2 / total
x_C4H10 = x_C4H10 / total
x_N2 = x_N2 / total

# concentrations = [{'C4H10': x_C4H10[i], 'O2': x_O2[i], 'N2': x_N2[i]} for i in range(0, len(equiv_ratios))]
concentrations = [{'butane(1)': x_C4H10[i], 'O2(2)': x_O2[i], 'N2': x_N2[i]} for i in range(0, len(equiv_ratios))]


# function for running a flame speed
# assumes gas has been properly initialized
def run_flame_speed(condition_index):
    gas = ct.Solution(cti_path)

    if 'butane(1)' not in gas.species_names and 'butane(1)' in concentrations[condition_index].keys():
        # check the keys to make sure we don't pop twice TODO should be O2 not in keys
        concentrations[condition_index]['C4H10'] = concentrations[condition_index].pop('butane(1)')
    if 'O2(2)' not in gas.species_names and 'O2(2)' in concentrations[condition_index].keys():
        concentrations[condition_index]['O2'] = concentrations[condition_index].pop('O2(2)')
    if 'CO2(7)' not in gas.species_names and 'CO2(7)' in concentrations[condition_index].keys():
        concentrations[condition_index]['CO2'] = concentrations[condition_index].pop('CO2(7)')
    if 'Ar' not in gas.species_names and 'Ar' in concentrations[condition_index].keys():
        concentrations[condition_index]['AR'] = concentrations[condition_index].pop('Ar')


    gas.TPX = temperatures[condition_index], pressures[condition_index], concentrations[condition_index]

    tol_ss = [1.0e-13, 1.0e-9]  # abs and rel tolerances for steady state problem
    tol_ts = [1.0e-13, 1.0e-9]  # abs and rel tie tolerances for time step function

    width = 0.08
    flame = ct.FreeFlame(gas, width=width)
    flame.flame.set_steady_tolerances(default=tol_ss)   # set tolerances
    flame.flame.set_transient_tolerances(default=tol_ts)
    flame.set_refine_criteria(ratio=5, slope=0.25, curve=0.27)
    flame.max_time_step_count = 5000
    #flame.max_time_step_count = 900
    loglevel = 1

    print("about to solve")
    flame.solve(loglevel=loglevel, auto=True)
    Su = flame.velocity[0]

    print("Save CSV")
    #csv_filepath = os.path.join(os.path.dirname(cti_path), f"flame_{condition_index}.csv")
    csv_filepath = os.path.join(save_dir, f"flame_{condition_index}.csv")
    flame.write_csv(csv_filepath)

    print("Save YAML")
    yaml_filepath = os.path.join(save_dir, f"flame_{condition_index}.yaml")
    flame.save(yaml_filepath, name="solution", description="Initial methane flame")

    
    return Su


# Run all simulations in parallel
flame_speeds = np.zeros(len(data_slice))
condition_indices = np.arange(0, len(data_slice))
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
    for condition_index, flame_speed in zip(condition_indices, executor.map(run_flame_speed, condition_indices)):
        flame_speeds[condition_index] = flame_speed


out_df = pd.DataFrame(flame_speeds)
# out_df.to_csv('aramco_flame_speeds.csv')

# out_df.to_csv('naive_improved_flame_speeds.csv')
# out_df.to_csv('rmg_changed_flame_speeds.csv')
#out_df.to_csv(f'{cti_path[:-4]}.csv')
#out_df.to_csv(f'{os.path.join(this_dir, os.path.basename(cti_path))[:-4]}.csv')
if cti_path[-4:] == 'yaml':
    # out_df.to_csv(f'{os.path.join(save_dir, os.path.basename(cti_path))[:-4]}.csv')  # yml
    out_df.to_csv(f'{os.path.join(save_dir, os.path.basename(cti_path))[:-5]}.csv')  # yaml
else:
    out_df.to_csv(f'{os.path.join(save_dir, os.path.basename(cti_path))[:-4]}.csv')  # yaml

