"""A Module for simulating ignition delay at given reaction conditions"""
import cantera as ct
import numpy as np
import logging


def perturb_species(species, DELTA_J_MOL=418.4):
    # takes in a Cantera species and makes a copy with the enthalpy offset changed
    # Default of 418 J/mol equals 0.1 kcal/mol
    R = 8.3144598  # gas constant in J/mol

    # copy the species
    input_data = species.input_data.copy()
    increase = None
    for i in range(len(input_data['thermo']['data'])):
        if not increase:
            # Only define the increase in enthalpy once or you'll end up with numerical gaps in continuity
            increase = DELTA_J_MOL / R
        input_data['thermo']['data'][i][5] += increase
    new_species = ct.Species().from_dict(input_data)
    return new_species


def run_simulation_for_delay(gas, T_orig, P_orig, X_orig, t_end=1.0, MAX_STEPS=10000):
    """Run an ignition-delay simulation for a single initial condition.
    Args:
        gas (ct.Solution): Cantera gas object to simulate
        T_orig (float): Initial temperature in K
        P_orig (float): Initial pressure in Pa
        X_orig (dict | str): Initial composition in Cantera format
        t_end (float, optional): Maximum simulation time in seconds
        MAX_STEPS (int, optional): Maximum integrator steps before giving up

    Returns:
        float: Ignition delay time in seconds, returns ``0`` if all attempts fail
    """
    atols = [1e-15, 1e-15, 1e-18]
    rtols = [1e-9, 1e-12, 1e-15]
    for attempt_index in range(0, len(atols)):
        T = T_orig
        P = P_orig
        X = X_orig

        gas.TPX = T, P, X

        reactor = ct.IdealGasReactor(gas)
        reactor_net = ct.ReactorNet([reactor])
        reactor_net.atol = atols[attempt_index]
        reactor_net.rtol = rtols[attempt_index]

        times = [0]
        T = [reactor.T]
        P = [reactor.thermo.P]
        step_count = 0
        failed = False
        logging.debug(f'Starting sim T={T}K')
        while reactor_net.time < t_end:
            try:
                reactor_net.step()
            except ct._cantera.CanteraError:
                logging.debug(f'Cantera Error. Reactor failed to solve on attempt {attempt_index}')
                failed = True
                break

            times.append(reactor_net.time)
            T.append(reactor.T)
            P.append(reactor.thermo.P)

            step_count += 1
            if step_count > MAX_STEPS:
                logging.debug(f'Too many steps. Reactor failed to solve on attempt {attempt_index}')
                failed = True
                break

        if not failed:
            slopes = np.gradient(P, times)
            delay_i = np.argmax(slopes)
            return times[delay_i]
        logging.debug(f'Trying again with tighter tolerances: atol={atols[attempt_index]}, rtol={rtols[attempt_index]}')

    logging.debug('All attempts failed to solve the simulation, returning 0')
    return 0


def run_full_simulation(gas, T_orig, P_orig, X_orig, t_end=1.0, MAX_STEPS=10000):
    """Run an ignition-delay simulation for a single initial condition.
    Args:
        gas (ct.Solution): Cantera gas object to simulate
        T_orig (float): Initial temperature in K
        P_orig (float): Initial pressure in Pa
        X_orig (dict | str): Initial composition in Cantera format
        t_end (float, optional): Maximum simulation time in seconds
        MAX_STEPS (int, optional): Maximum integrator steps before giving up

    Returns:
        times, T, P, X, and net_rates_of_progress (usually for flux diagram creation)
    """
    atols = [1e-15, 1e-15, 1e-18]
    rtols = [1e-9, 1e-12, 1e-15]
    for attempt_index in range(0, len(atols)):
        T = T_orig
        P = P_orig
        X = X_orig

        gas.TPX = T, P, X

        reactor = ct.IdealGasReactor(gas)
        reactor_net = ct.ReactorNet([reactor])
        reactor_net.atol = atols[attempt_index]
        reactor_net.rtol = rtols[attempt_index]

        times = [0]
        temperatures = [reactor.T]
        pressures = [reactor.phase.P]
        concs = [reactor.phase.X]
        rates = [reactor.phase.net_rates_of_progress]
        step_count = 0
        failed = False
        logging.debug(f'Starting sim T={T}K')
        while reactor_net.time < t_end:
            try:
                reactor_net.step()
            except ct._cantera.CanteraError:
                logging.debug(f'Cantera Error. Reactor failed to solve on attempt {attempt_index}')
                failed = True
                break

            times.append(reactor_net.time)
            temperatures.append(reactor.T)
            pressures.append(reactor.phase.P)
            concs.append(reactor.phase.X)
            rates.append(reactor.phase.net_rates_of_progress)

            step_count += 1
            if step_count > MAX_STEPS:
                logging.debug(f'Too many steps. Reactor failed to solve on attempt {attempt_index}')
                failed = True
                break
        
        times = np.array(times)
        temperatures = np.array(temperatures)
        pressures = np.array(pressures)
        concs = np.array(concs)
        rates = np.array(rates)
        if not failed:
            return times, temperatures, pressures, concs, rates
        logging.debug(f'Trying again with tighter tolerances: atol={atols[attempt_index]}, rtol={rtols[attempt_index]}')

    logging.debug('All attempts failed to solve the simulation, returning None')
    return None
