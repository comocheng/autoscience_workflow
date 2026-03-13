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
import cantera as ct
import simulation
import matplotlib.pyplot as plt
import numpy as np

# %matplotlib inline
# -

# # Test Ignition Delay Time

# +
gas = ct.Solution('gri30.yaml')

T = 1000
P = ct.one_atm * 10.0
X = 'CH4: 0.2, O2: 0.2, AR: 0.6'

times, temperatures, pressures, concs, rates = simulation.run_full_simulation(gas, T, P, X)
delay = simulation.run_simulation_for_delay(gas, T, P, X)
plt.plot(times, pressures)
plt.xlabel('time (s)')
plt.ylabel('Pressure (Pa)')
plt.axvline(x=delay, color='black', label='Ignition Delay Time')

# +
for i in range(gas.n_species):
    if np.max(concs[:, i]) > 1e-3:
        plt.plot(times, concs[:, i], label=gas.species_names[i])

plt.xlabel('Time (s)')
plt.ylabel('Concentration')
plt.axvline(x=delay, color='black', label='Ignition Delay Time', linewidth=0.2)
plt.legend()
# -

# # Test perturb thermo

gas.ne



for i in


