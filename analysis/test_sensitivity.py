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
import sensitivity
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

# +
species_index = gas.species_names.index('CH4')

original_species = ct.Species().from_dict(gas.species()[species_index].input_data.copy())
perturbed_species = sensitivity.perturb_species(gas.species()[species_index])

temperatures = np.linspace(800, 900, 101)
hs_original = np.zeros_like(temperatures)
hs_perturbed = np.zeros_like(temperatures)
hs_gas_object_before = np.zeros_like(temperatures)
hs_gas_object_after = np.zeros_like(temperatures)
for i in range(len(temperatures)):
    hs_original[i] = original_species.thermo.h(temperatures[i]) / 1000
    hs_perturbed[i] = perturbed_species.thermo.h(temperatures[i]) / 1000
    hs_gas_object_before[i] = gas.species()[species_index].thermo.h(temperatures[i]) / 1000

gas.modify_species(species_index, perturbed_species)
for i in range(len(temperatures)):
    hs_gas_object_after[i] = gas.species()[species_index].thermo.h(temperatures[i]) / 1000

plt.plot(temperatures, hs_original, label='Original')
plt.plot(temperatures, hs_perturbed, label='Perturbed')

plt.plot(temperatures, hs_gas_object_before, label='Gas Object Before', linestyle='dashed')
plt.plot(temperatures, hs_gas_object_after, label='Gas Object After', linestyle='dashed')

plt.ylabel('Enthalpy J/mol')
plt.xlabel('Temperature (K)')
plt.legend()

# +
# Plot results of changing CH4's H298
gas = ct.Solution('gri30.yaml')

T = 1000
P = ct.one_atm * 10.0
X = 'CH4: 0.2, O2: 0.2, AR: 0.6'

species_index = gas.species_names.index('OH')

times, temperatures, pressures, concs, rates = simulation.run_full_simulation(gas, T, P, X)
plt.plot(times, concs[:, species_index], label='Before')


original_species = ct.Species().from_dict(gas.species()[species_index].input_data.copy())
perturbed_species = sensitivity.perturb_species(gas.species()[species_index])
gas.modify_species(species_index, perturbed_species)
times, temperatures, pressures, concs, rates = simulation.run_full_simulation(gas, T, P, X)
plt.plot(times, concs[:, species_index], label='After')


gas.modify_species(species_index, original_species)


plt.xlabel('time (s)')
plt.ylabel('OH Concentration')
plt.xscale('log')
plt.xlim([1e-3, 1.0])
plt.legend()
# -

gas.species_names.index('OH')


