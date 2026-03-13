# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# Construct a configuration yaml for conditions at which to simulate for experiment, smooth, curve, and sensitivity

# +
# Load experiment csv
# -

import numpy as np
import pandas as pd
import yaml
import cantera as ct

# +
# Load the experimental conditions
ignition_delay_data = '../experiment/butane_ignition_delay.csv'
df_exp = pd.read_csv(ignition_delay_data)

# slice just table 7, where phi=1.0
table7 = df_exp[df_exp['Table'] == 7]

# slice up to just use Argon as diluent
table7 = table7[table7['%Ar'] == 100]

# Define Initial conditions using experimental data
tau7 = table7['time (ms)'].values.astype(float)  # ignition delay
T7 = table7['T_C'].values  # Temperatures
P7 = table7['nominal pressure(atm)'].values * ct.one_atm  # pressures in atm


# list of starting conditions
# Mixture compositions taken from table 2 of
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
concentrations = []
# for phi = 1
x_diluent = 0.7649


for i in range(0, len(table7)):
    conc_dict = {
        'O2(2)': 0.2038,
        'butane(1)': 0.03135
    }
    x_N2 = table7['%N2'].values[i] / 100.0 * x_diluent
    x_Ar = table7['%Ar'].values[i] / 100.0 * x_diluent
    x_CO2 = table7['%CO2'].values[i] / 100.0 * x_diluent
    conc_dict['N2'] = float(x_N2)
    conc_dict['Ar'] = float(x_Ar)
    # conc_dict['CO2(7)'] = float(x_CO2)
    concentrations.append(conc_dict)

# -

table7

concentrations

# temperature range
Tmax = 1077  # use min and max temperature range of the data: 663K-1077K
Tmin = 663
N = 51
full_temperature_range = np.linspace(Tmin, Tmax, N)

M = 6  # sensitivity points
sampled_temperature_range = np.linspace(Tmin, Tmax, M)

conditions_dict = {
    'experiment_points': [{'T': float(T7[i]), 'P': float(P7[i]), 'X': concentrations[i]} for i in range(len(T7))],
    'smooth_plot': [{'T': float(full_temperature_range[i]), 'P': float(P7[0]), 'X': concentrations[0]} for i in range(N)],
    'sensitivity_points': [{'T': float(sampled_temperature_range[i]), 'P': float(P7[0]), 'X': concentrations[0]} for i in range(M)]
}

experimental_yaml_file = 'butane1.yaml'
with open(experimental_yaml_file, 'w') as outfile:
    yaml.dump(conditions_dict, outfile, default_flow_style=False)

with open(experimental_yaml_file) as f:
    data = yaml.safe_load(f)


data['sensitivity_points']



# # original config with too many sensitivity points

# +
# temperature range
Tmax = 1077  # use min and max temperature range of the data: 663K-1077K
Tmin = 663
N = 51
full_temperature_range = np.linspace(Tmin, Tmax, N)

M = N  # sensitivity points
sampled_temperature_range = np.linspace(Tmin, Tmax, M)

# -

conditions_dict = {
    'experiment_points': [{'T': float(T7[i]), 'P': float(P7[i]), 'X': concentrations[i]} for i in range(len(T7))],
    'smooth_plot': [{'T': float(full_temperature_range[i]), 'P': float(P7[0]), 'X': concentrations[0]} for i in range(N)],
    'sensitivity_points': [{'T': float(sampled_temperature_range[i]), 'P': float(P7[0]), 'X': concentrations[0]} for i in range(M)]
}

experimental_yaml_file = 'butane0.yaml'
with open(experimental_yaml_file, 'w') as outfile:
    yaml.dump(conditions_dict, outfile, default_flow_style=False)

with open(experimental_yaml_file) as f:
    data = yaml.safe_load(f)

data


