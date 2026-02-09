# module that has a sim function where you give it the RMG species list and rection list
# and temperature and it gives you the simulation results

import cantera as ct
import numpy as np
import rmgpy.chemkin
import subprocess


def run_quicksim(species_list, reaction_list, T=830, P=10.0 * ct.one_atm, X=None):
    # save chemkin file
    rmgpy.chemkin.save_chemkin_file('temp.inp', species_list, reaction_list, verbose=True, check_for_duplicates=True)

    # convert to cantera
    subprocess.run(['ck2yaml', '--input=temp.inp', '--output=temp.yaml'])
    gas = ct.Solution('temp.yaml')
    if X is None:
        X = {
            'O2(2)': 0.2038,
            'butane(1)': 0.03135,
            'N2': 0.7649,
        }
    print(f'Running quicksim with T={T}, P={P}, X={X}')
    gas.TPX = T, P, X
    t_end = 10.0  # time in seconds
          
    reactor = ct.IdealGasReactor(gas)
    reactor_net = ct.ReactorNet([reactor])
    reactor_net.atol = 1e-15
    reactor_net.rtol = 1e-9

    times = [0]
    T = [reactor.T]
    P = [reactor.thermo.P]
    X = [reactor.thermo.X]  # mol fractions
    MAX_STEPS = 10000
    step_count = 0
    failed = False
    while reactor_net.time < t_end:
        try:
            reactor_net.step()
        except ct._cantera.CanteraError:
            print(f'Reactor failed to solve!')
            failed = True
            break

        times.append(reactor_net.time)
        T.append(reactor.T)
        P.append(reactor.thermo.P)
        X.append(reactor.thermo.X)

        step_count += 1
        if step_count > MAX_STEPS:
            print(f'Too many steps! Reactor failed to solve!')
            failed = True
            break

    return times, P, X, failed

def get_ignition_delay_time(times, P):
    slopes = np.gradient(P, times)
    delay_i = np.argmax(slopes)
    return times[delay_i]
