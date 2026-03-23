import os
import sys
import cantera as ct
import numpy as np


mech_yaml = sys.argv[1]
mech_yaml = mech_yaml.replace('.inp', '.yaml')
    
gas = ct.Solution(mech_yaml)
    
T_init = 787
P_init = 10 * ct.one_atm
X_init = 'butane(1): 0.032065, N2: 0.7821, O2(2): 0.02083'
    
gas.TPX = T_init, P_init, X_init
reactor = ct.IdealGasReactor(gas)
sim = ct.ReactorNet([reactor])
    
t_end = 10.0  # seconds
times = []
concentrations = []
rates = []
while sim.time < t_end:
    sim.step()
    times.append(sim.time)
    concentrations.append(gas.X)
    rates.append(gas.net_rates_of_progress)
    
times = np.array(times)
concentrations = np.array(concentrations)
rates = np.array(rates)
    
np.save(os.path.join(os.path.dirname(mech_yaml), 'times.npy'), times)
np.save(os.path.join(os.path.dirname(mech_yaml), 'concentrations.npy'), concentrations)
np.save(os.path.join(os.path.dirname(mech_yaml), 'rates.npy'), rates)

