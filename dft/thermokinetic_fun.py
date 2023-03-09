# set of functions related to thermokinetic calculations

import os
import glob
import sys
import pandas as pd
import time
import datetime
import yaml
import job_manager

import arkane.ess.gaussian  # does a lot better at reading gaussian files than ase

# do I really need any of these?
import shutil

import cclib.io

import autotst.species
import autotst.reaction
import autotst.calculator.gaussian

import ase.io.gaussian


try:
    DFT_DIR = os.environ['DFT_DIR']
except KeyError:
    DFT_DIR = "/work/westgroup/harris.se/autoscience/reaction_calculator/dft"
    # DFT_DIR = "/home/moon/autoscience/reaction_calculator/dft"

MAX_JOBS_RUNNING = 40


def termination_status(log_file):
    """Analyze a Gaussian run by reading in reverse (allegedly faster than reading from start)
    Returns:
    0 for Normal termination
    1 for Error termination not covered below
    2 for Error termination - due to all degrees of freedom being frozen
    3 for Error termination - Problem with the distance matrix.
    4 for No NMR shielding tensors so no spin-rotation constants  # TODO debug this instead of ignoring it
    5 for MANUAL SKIP
    -1 for no termination
    """
    error_termination = False
    with open(log_file, 'rb') as f:
        f.seek(0, os.SEEK_END)
        error_termination = False
        for i in range(0, 20):
            try:
                f.seek(-2, os.SEEK_CUR)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            saved_position = f.tell()
            last_line = f.readline().decode()
            f.seek(saved_position, os.SEEK_SET)
            if 'Normal termination' in last_line:
                return 0
            elif 'Error termination' in last_line:
                error_termination = True
            elif 'All variables have been frozen' in last_line:
                return 2
            elif 'Problem with the distance matrix' in last_line:
                return 3
            elif 'No NMR shielding tensors so no spin-rotation constants' in last_line:
                return 4
            elif 'MANUAL SKIP' in last_line.upper():
                return 5
        if error_termination:
            return 1
        return -1


def species_log(species_index, message):
    """Function to log messages to the species log file"""
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    logfile = os.path.join(species_dir, 'thermokinetic_fun.log')
    print(f'{datetime.datetime.now()} {message}')
    with open(logfile, 'a') as f:
        f.write(f'{datetime.datetime.now()} {message}' + '\n')


def reaction_log(reaction_index, message):
    """Function to log messages to the reaction log file"""
    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    logfile = os.path.join(reaction_dir, 'thermokinetic_fun.log')
    print(f'{datetime.datetime.now()} {message}')
    with open(logfile, 'a') as f:
        f.write(f'{datetime.datetime.now()} {message}' + '\n')


def species_index2smiles(species_index):
    """Function to return species smiles given a species index
    looks up the results in the species_list.csv
    """
    species_csv = os.path.join(DFT_DIR, 'species_list.csv')
    species_df = pd.read_csv(species_csv)
    species_index = species_df['SMILES'].values[species_index]
    return species_index


def reaction_index2smiles(reaction_index):
    """Function to return reaction smiles given a reaction index
    looks up the results in the reaction_list.csv
    """
    reaction_csv = os.path.join(DFT_DIR, 'reaction_list.csv')
    reaction_df = pd.read_csv(reaction_csv)
    reaction_smiles = reaction_df['SMILES'].values[reaction_index]
    return reaction_smiles


def get_species_status(species_index, job_type):
    """Check the status of the part of the species calculation by looking in the status file
    Possibilities are:
        - screen_conformers - complete if the conformer optimization files have been generated
        - conformer_opt - run Gaussian to optimize the conformers
    """
    status_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'status.yaml')
    if not os.path.exists(status_file):
        return False
    with open(status_file, 'r') as f:
        try:
            status = yaml.load(f, Loader=yaml.FullLoader)
        except AttributeError:
            status = yaml.safe_load(f)
    if job_type in status:
        return status[job_type]
    return False


def get_reaction_status(reaction_index, job_type):
    """Check the status of the part of the reaction calculation by looking in the status file
    Possibilities are:
        - screen_conformers - complete if the conformer optimization files have been generated
        - shell_opt - run Gaussian to optimize the conformers
        - center_opt
        - overall_opt
        - arkane?
    """
    status_file = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}', 'status.yaml')
    if not os.path.exists(status_file):
        return False
    with open(status_file, 'r') as f:
        try:
            status = yaml.load(f, Loader=yaml.FullLoader)
        except AttributeError:
            status = yaml.safe_load(f)
    if job_type in status:
        return status[job_type]
    return False


def set_species_status(species_index, job_type, job_status):
    """Set the status of the part of the species calculation by writing the status file
    Possibilities are:
        - screen_conformers - complete if the conformer optimization files have been generated
        - conformer_opt - run Gaussian to optimize the conformers
    """
    status_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'status.yaml')
    status = {}
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            try:
                status = yaml.load(f, Loader=yaml.FullLoader)
            except AttributeError:
                status = yaml.safe_load(f)
    status[job_type] = job_status
    with open(status_file, 'w') as f:
        yaml.dump(status, f)


def set_reaction_status(reaction_index, job_type, job_status):
    """Set the status of the part of the reaction calculation by writing the status file
    Possibilities are:
        - screen_conformers - complete if the conformer optimization files have been generated
        - shell_opt - run Gaussian to optimize the conformers
        - center_opt
        - overall_opt
        - arkane?
    """
    status_file = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}', 'status.yaml')
    status = {}
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            try:
                status = yaml.load(f, Loader=yaml.FullLoader)
            except AttributeError:
                status = yaml.safe_load(f)
    status[job_type] = job_status
    with open(status_file, 'w') as f:
        yaml.dump(status, f)


def ordered_array_str(list_of_indices):
    # convenient script for putting a list of task numbers into a string that can be used for a SLURM array job
    # assume it's sorted
    if len(list_of_indices) == 1:
        return str(list_of_indices[0])
    elif len(list_of_indices) == 2:
        return f'{list_of_indices[0]}, {list_of_indices[1]}'

    array_str = str(list_of_indices[0]) + '-'
    for j in range(1, len(list_of_indices) - 1):
        if list_of_indices[j] - list_of_indices[j - 1] != 1:
            if j > 1:
                array_str += str(list_of_indices[j - 1])
                array_str += f',{list_of_indices[j]}-'
            else:
                array_str = array_str.replace('-', ',')
                array_str += f'{list_of_indices[j]}-'
        # cap the end
        if j + 2 == len(list_of_indices):
            if list_of_indices[j + 1] - list_of_indices[j] != 1:
                array_str += f'{list_of_indices[j]},{list_of_indices[j + 1]}'
            else:
                array_str += f'{list_of_indices[j + 1]}'

    return array_str


def screen_species_conformers(species_index):
    """Sort through all the possible conformers and use a cheap calculator
    like Hotbit or LJ to screen the best options to investigate

    Takes a species index and saves the conformers to investigate as .pickle?
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    if get_species_status(species_index, 'screen_conformers'):
        species_log(species_index, 'Conformers already screened')
        return True

    conformer_dir = os.path.join(species_dir, 'conformers')
    os.makedirs(conformer_dir, exist_ok=True)
    species_log(species_index, f'Starting conformer screening job')

    # ------------------ Use Hotbit to screen the conformers ------------------
    # Get species smiles
    species_smiles = species_index2smiles(species_index)
    spec = autotst.species.Species([species_smiles])
    species_log(species_index, f'Loaded species {species_smiles}')

    try:
        import hotbit
        calc = hotbit.Hotbit()
    except (ImportError, RuntimeError):
        # if hotbit fails, use built-in lennard jones
        import ase.calculators.lj
        species_log(species_index, 'Using built-in ase LennardJones calculator instead of Hotbit')
        calc = ase.calculators.lj.LennardJones()
    # hotbit can't handle Ar, He, change calculator to lj if it's in the species
    hotbit_skiplist = ['AR', 'HE', 'NE']
    for element in hotbit_skiplist:
        if element in species_smiles.upper():
            import ase.calculators.lj
            species_log(species_index, f'Using built-in ase LennardJones calculator instead of Hotbit for {element}')
            calc = ase.calculators.lj.LennardJones()
            break

    spec.generate_conformers(
        ase_calculator=calc,
        max_combos=10000,
        max_conformers=1000,
        results_dir=conformer_dir,
        save_results=True,
    )

    n_conformers = 0
    for key in spec.conformers:
        n_conformers += len(spec.conformers[key])
    species_log(species_index, f'{n_conformers} found with {str(calc)}')

    # ------------------ Use Gaussian to do a more detailed calculation ------------------
    species_log(species_index, "Generating gaussian input files")
    save_offset = 0
    for resonance_smiles in spec.conformers.keys():
        for i, cf in enumerate(spec.conformers[resonance_smiles]):
            conformer_index = i + save_offset
            gaussian = autotst.calculator.gaussian.Gaussian(conformer=cf)
            calc = gaussian.get_conformer_calc()
            calc.label = f'conformer_{conformer_index:04}'
            calc.directory = conformer_dir
            calc.parameters.pop('scratch')
            calc.parameters.pop('multiplicity')
            calc.parameters['mult'] = cf.rmg_molecule.multiplicity
            calc.chk = f'conformer_{conformer_index:04}.chk'
            calc.write_input(cf.ase_molecule)
        save_offset += len(spec.conformers[resonance_smiles])

    # write to the status file to indicate that the conformer screening is complete
    set_species_status(species_index, 'screen_conformers', True)
    species_log(species_index, f'Conformer screening complete')
    return True


def optimize_conformers(species_index):
    """Optimize the conformers that were screened"""
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    species_log(species_index, f'Starting conformer optimization job')

    # check if the run was already completed
    if get_species_status(species_index, 'conformer_opt'):
        species_log(species_index, f'Conformer optimization already ran')
        return True
    if conformers_done_optimizing(conformer_dir):
        species_log(species_index, f'Conformer optimization already ran')
        set_species_status(species_index, 'conformer_opt', True)
        return True

    n_conformers = len(glob.glob(os.path.join(conformer_dir, 'conformer_*.com')))
    rerun_indices = []
    for i in range(0, n_conformers):
        conformer_logfile = os.path.join(conformer_dir, f'conformer_{i:04}.log')
        if os.path.exists(conformer_logfile):
            termination_status = termination_status(conformer_logfile)
            if termination_status == 1 or termination_status == -1:
                rerun_indices.append(i)

    # Make slurm script to run all the conformer calculations
    slurm_run_file = os.path.join(conformer_dir, 'run.sh')
    slurm_settings = {
        '--job-name': f'g16_cf_{species_index}',
        '--error': 'error.log',
        '--nodes': 1,
        '--partition': 'west,short',
        '--exclude': 'c5003',
        '--mem': '20Gb',
        '--time': '24:00:00',
        '--cpus-per-task': 16,
        '--array': f'0-{n_conformers - 1}%30',
    }
    if rerun_indices:
        slurm_run_file = os.path.join(conformer_dir, 'rerun.sh')
        slurm_settings['--partition'] = 'short'
        slurm_settings['--constraint'] = 'cascadelake'
        slurm_settings['--array'] = ordered_array_str(rerun_indices)
        slurm_settings['--cpus-per-task'] = 32
        slurm_settings.pop('--exclude')

    slurm_file_writer = job_manager.SlurmJobFile(
        full_path=slurm_run_file,
    )
    slurm_file_writer.settings = slurm_settings
    slurm_file_writer.content = [
        'export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch\n',
        'mkdir -p $GAUSS_SCRDIR\n',
        'module load gaussian/g16\n',
        'source /shared/centos7/gaussian/g16/bsd/g16.profile\n\n',

        'RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))\n',
        'fname="conformer_${RUN_i}.com"\n\n',

        'g16 $fname\n',
    ]
    slurm_file_writer.write_file()

    # submit the job
    start_dir = os.getcwd()
    os.chdir(conformer_dir)
    gaussian_conformers_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {slurm_run_file}"

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()

    gaussian_conformers_job.submit(slurm_cmd)
    os.chdir(start_dir)


def conformers_done_optimizing(base_dir, completion_threshold=0.9, base_name='conformer_'):
    """function to see if all the conformers are done optimizing, returns True if so"""
    n_conformers = len(glob.glob(os.path.join(base_dir, f'{base_name}*.com')))
    incomplete_indices = []
    good_runs = []
    finished_runs = []
    for i in range(0, n_conformers):
        conformer_file = os.path.join(base_dir, f'{base_name}{i:04}.log')
        if not os.path.exists(conformer_file):
            return False
        opt_status = termination_status(conformer_file)
        if opt_status == 0:
            good_runs.append(i)
            finished_runs.append(i)
        elif opt_status == 2 or opt_status == 3 or opt_status == 4 or opt_status == 5:
            # not good optimizations, but we're going to keep going anyways
            finished_runs.append(i)
        else:
            # optimization didn't finish
            incomplete_indices.append(i)
    if len(finished_runs) / n_conformers >= completion_threshold and len(good_runs) > 0:
        return True
    return False


def wait_for_conformer_opt(species_index):
    """Wait for the conformer optimization to finish"""
    # check if the run was already completed
    if get_species_status(species_index, 'conformer_opt'):
        species_log(species_index, f'Conformer optimization already ran')
        return True

    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    opt_completed = conformers_done_optimizing(conformer_dir)
    while not opt_completed:
        time.sleep(60)
        opt_completed = conformers_done_optimizing(conformer_dir)

    # write to the status file to indicate that the conformer screening is complete
    set_species_status(species_index, 'conformer_opt', True)
    species_log(species_index, f'Conformer optimization complete')


def arkane_species_complete(species_index):
    """Function to check whether the arkane job is complete for a species
    Expects to find the following directory structure:
    DFT_DIR/thermo/species_XXXX/arkane/RMG_libraries/thermo.py
    Returns True if complete, False otherwise
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    arkane_result = os.path.join(species_dir, 'arkane', 'RMG_libraries', 'thermo.py')
    return os.path.exists(arkane_result)


def get_gaussian_file_energy(gaussian_log_file):
    """Function to get the energy from a Gaussian .log file"""
    with open(gaussian_log_file, 'r') as f:
        # check that it's really a gaussian file
        line = f.readline()
        if 'Gaussian' not in line:
            return None
        f.seek(0)
        gl = arkane.ess.gaussian.GaussianLog(gaussian_log_file, check_for_errors=False)
        return gl.load_energy()


def get_lowest_energy_gaussian_file(base_dir):
    """Function to get the lowest energy gaussian .log file from a directory"""
    lowest_energy = 1e6
    lowest_file = None
    log_files = glob.glob(os.path.join(base_dir, '*.log'))
    for gaussian_log_file in log_files:
        energy = get_gaussian_file_energy(gaussian_log_file)
        if energy is None:
            continue
        if energy < lowest_energy:
            lowest_energy = energy
            lowest_file = gaussian_log_file
    return lowest_file


def get_rotor_info(conformer, torsion, torsion_index):
    _, j, k, _ = torsion.atom_indices

    # Adjusted since mol's IDs start from 0 while Arkane's start from 1
    tor_center_adj = [j + 1, k + 1]

    tor_log = f'rotor_{torsion_index:04}.log'
    top_IDs = []
    for num, tf in enumerate(torsion.mask):
        if tf:
            top_IDs.append(num)

    # Adjusted to start from 1 instead of 0
    top_IDs_adj = [ID + 1 for ID in top_IDs]

    info = f"     HinderedRotor(scanLog=Log('{tor_log}'), pivots={tor_center_adj}, top={top_IDs_adj}, fit='fourier'),"

    return info


def write_arkane_conformer_file(conformer, gauss_log, arkane_dir, include_rotors=False):
    # assume rotor and conformer logs have already been copied into the arkane directory
    label = conformer.smiles
    species_name = os.path.basename(gauss_log[:-4])
    parser = cclib.io.ccread(gauss_log)
    symbol_dict = {
        35: "Br",
        17: "Cl",
        9: "F",
        8: "O",
        7: "N",
        6: "C",
        1: "H",
        18: "Ar",
        2: "He",
        10: "Ne",
    }

    atoms = []

    for atom_num, coords in zip(parser.atomnos, parser.atomcoords[-1]):
        atoms.append(ase.Atom(symbol=symbol_dict[atom_num], position=coords))

    conformer._ase_molecule = ase.Atoms(atoms)
    conformer.update_coords_from("ase")
    mol = conformer.rmg_molecule
    output = ['#!/usr/bin/env python',
              '# -*- coding: utf-8 -*-', ]

    output += ["", f"spinMultiplicity = {conformer.rmg_molecule.multiplicity}", ""]
    model_chemistry = 'M06-2X/cc-pVTZ'

    # use relative path for easy transfer -- assume we will copy the log files into the Arkane folder
    gauss_log_relative = os.path.basename(gauss_log)
    output += ["energy = {", f"    '{model_chemistry}': Log('{gauss_log_relative}'),", "}", ""]  # fix this

    output += [f"geometry = Log('{gauss_log_relative}')", ""]
    output += [
        f"frequencies = Log('{gauss_log_relative}')", ""]

    # get the rotors
    torsions = conformer.get_torsions()
    n_rotors = len(torsions)

    if include_rotors and n_rotors > 0:
        output += ["rotors = ["]
        if len(conformer.torsions) == 0:
            conformer.get_molecules()
            conformer.get_geometries()
        for i, torsion in enumerate(conformer.torsions):
            output += [get_rotor_info(conformer, torsion, i)]
        output += ["]"]

    input_string = ""

    for t in output:
        input_string += t + "\n"

    with open(os.path.join(arkane_dir, species_name + '.py'), "w") as f:
        f.write(input_string)
    return True


def setup_arkane_species(species_index, include_rotors=False):
    """Function to set up the Arkane species directory for a given species
    default is to not do rotors. But if rotors are specified, the arkane directory
    will be arkane_rotors
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    arkane_dir = os.path.join(species_dir, 'arkane')
    os.makedirs(arkane_dir, exist_ok=True)
    if include_rotors:
        arkane_dir = os.path.join(species_dir, 'arkane_rotors')
    species_log(species_index, f'Setting up Arkane species')
    if arkane_species_complete(species_index):
        species_log(species_index, f'Arkane species already complete')
        return True

    species_smiles = species_index2smiles(species_index)
    # make a conformer object from the SMILES
    new_cf = autotst.species.Conformer(smiles=species_smiles)
    # read the conformer geometry from the file
    conformer_file = get_lowest_energy_gaussian_file(conformer_dir)

    shutil.copy(conformer_file, arkane_dir)
    with open(conformer_file, 'r') as f:
        atoms = ase.io.gaussian.read_gaussian_out(f)

    new_cf._ase_molecule = atoms
    new_cf.update_coords_from(mol_type="ase")

    if include_rotors:
        rotor_dir = os.path.join(species_dir, 'rotors')
        torsions = new_cf.get_torsions()
        for i, torsion in enumerate(torsions):
            # TODO check for valid output
            torfile = os.path.join(rotor_dir, f'rotor_{i:04}.log')
            shutil.copy(torfile, arkane_dir)

    # write the Arkane conformer file
    write_arkane_conformer_file(new_cf, conformer_file, arkane_dir, include_rotors=include_rotors)

    # write the Arkane input file
    input_file = os.path.join(arkane_dir, 'input.py')
    formula = new_cf.rmg_molecule.get_formula()
    lines = [
        '#!/usr/bin/env python\n\n',
        f'modelChemistry = "M06-2X/cc-pVTZ"\n',
        f'useHinderedRotors = {include_rotors}' + '\n',
        'useBondCorrections = False\n\n',

        'frequencyScaleFactor = 0.982\n',

        f"species('{formula}', '{os.path.basename(conformer_file[:-4])}.py', structure=SMILES('{new_cf.rmg_molecule.smiles}'))\n\n",

        f"thermo('{formula}', 'NASA')\n",
    ]
    with open(input_file, 'w') as f:
        f.writelines(lines)

    # copy a run script into the arkane directory
    run_script = os.path.join(arkane_dir, 'run_arkane.sh')
    with open(run_script, 'w') as f:
        # Run on express
        f.write('#!/bin/bash\n')
        f.write('#SBATCH --partition=express,short,west\n')
        f.write('#SBATCH --time=00:20:00\n\n')
        f.write('python ~/rmg/RMG-Py/Arkane.py input.py\n\n')


def delete_double_spaces(gaussian_com_file):
    # Get rid of first double-linespace found,
    # usually between xyz and modredundant sections
    double_space = False
    lines = []
    with open(gaussian_com_file, 'r') as f:
        lines = f.readlines()
        for j in range(1, len(lines)):
            if lines[j] == '\n' and lines[j - 1] == '\n':
                double_space = True
                break
    if double_space:
        lines = lines[0:j - 1] + lines[j:]
        with open(gaussian_com_file, 'w') as f:
            f.writelines(lines)


def screen_reaction_ts(reaction_index, direction='forward'):
    """Function to screen TS conformers for a given reaction
    Writes the resulting conformers as gaussian input files in the shell directory
    """
    # check if the screening already ran
    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    if get_reaction_status(reaction_index, 'screen_conformers'):
        reaction_log(reaction_index, 'Conformers already screened')
        return True

    screen_dir = os.path.join(reaction_dir, 'screen')
    os.makedirs(screen_dir, exist_ok=True)
    reaction_log(reaction_index, f'Starting conformer screening job')

    shell_dir = os.path.join(reaction_dir, 'shell')
    os.makedirs(shell_dir, exist_ok=True)

    # ------------------ Use Hotbit to screen the conformers ------------------
    # Get reaction smiles
    reaction_smiles = reaction_index2smiles(reaction_index)
    reaction_log(reaction_index, f'Constructing reaction in AutoTST...')
    reaction = autotst.reaction.Reaction(label=reaction_smiles)

    reaction.ts[direction][0].get_molecules()
    try:
        import hotbit
        calc = hotbit.Hotbit()
    except (ImportError, RuntimeError):
        # if hotbit fails, use built-in lennard jones
        import ase.calculators.lj
        reaction_log(reaction_index, 'Using built-in ase LennardJones calculator instead of Hotbit')
        calc = ase.calculators.lj.LennardJones()
    reaction.generate_conformers(
        ase_calculator=calc,
        max_combos=1000,
        max_conformers=100,
        save_results=True,
        results_dir=screen_dir,
    )
    reaction_log(reaction_index, f'Done generating conformers in AutoTST...')
    reaction_log(reaction_index, f'{len(reaction.ts[direction])} conformers found')

    # -------------- Write the results as gaussiuan calculations in the shell dir
    # Check for already finished shell logfiles
    # first, return if all of them have finished
    shell_label = 'fwd_ts_0000.log'
    if direction == 'reverse':
        shell_label = 'rev_ts_0000.log'

    for i in range(0, len(reaction.ts[direction])):
        shell_label = shell_label[:-8] + f'{i:04}.log'

        ts = reaction.ts[direction][i]
        gaussian = autotst.calculator.gaussian.Gaussian(conformer=ts)
        calc = gaussian.get_shell_calc()
        calc.label = shell_label[:-4]
        calc.directory = shell_dir
        calc.parameters.pop('scratch')
        calc.parameters.pop('multiplicity')
        calc.parameters['mult'] = ts.rmg_molecule.multiplicity
        calc.write_input(ts.ase_molecule)

        # Get rid of double-space between xyz block and mod-redundant section
        delete_double_spaces(os.path.join(shell_dir, calc.label + '.com'))

    # write to the status file to indicate that the conformer screening is complete
    set_reaction_status(reaction_index, 'screen_conformers', True)
    reaction_log(reaction_index, f'Conformer screening complete')
    return True


def run_shell_opt(reaction_index, direction='forward'):
    """Run optimization on the shell (freeze reaction core and relax the rest of the molecule)
    """
    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    shell_dir = os.path.join(reaction_dir, 'shell')
    os.makedirs(shell_dir, exist_ok=True)
    reaction_log(reaction_index, f'Starting shell optimization job')

    # check if the run was already completed
    if get_reaction_status(reaction_index, 'shell_opt'):
        reaction_log(reaction_index, f'Shell optimization already ran')
        return True

    # manually check if the shell optimizations are complete
    shell_label = 'fwd_ts_0000.log'
    if direction == 'reverse':
        shell_label = 'rev_ts_0000.log'
    if conformers_done_optimizing(shell_dir, base_name=shell_label[:-8]):
        reaction_log(reaction_index, f'TS optimization already ran')
        set_reaction_status(reaction_index, 'shell_opt', True)
        return True

    n_conformers = len(glob.glob(os.path.join(shell_dir, f'{shell_label[:-8]}*.com')))
    rerun_indices = []
    for i in range(0, n_conformers):
        conformer_logfile = os.path.join(shell_dir, f'conformer_{i:04}.log')
        if os.path.exists(conformer_logfile):
            termination_status = termination_status(conformer_logfile)
            if termination_status == 1 or termination_status == -1:
                rerun_indices.append(i)

    # Make slurm script to run all the conformer calculations
    slurm_run_file = os.path.join(shell_dir, 'run.sh')
    slurm_settings = {
        '--job-name': f'g16_shell_{reaction_index}',
        '--error': 'error.log',
        '--nodes': 1,
        '--partition': 'west,short',
        '--exclude': 'c5003',
        '--mem': '20Gb',
        '--time': '24:00:00',
        '--cpus-per-task': 16,
        '--array': f'0-{n_conformers - 1}%30',
    }
    if rerun_indices:
        slurm_run_file = os.path.join(shell_dir, 'rerun.sh')
        slurm_settings['--partition'] = 'short'
        slurm_settings['--constraint'] = 'cascadelake'
        slurm_settings['--array'] = ordered_array_str(rerun_indices)
        slurm_settings['--cpus-per-task'] = 32
        slurm_settings.pop('--exclude')

    slurm_file_writer = job_manager.SlurmJobFile(
        full_path=slurm_run_file,
    )
    slurm_file_writer.settings = slurm_settings
    slurm_file_writer.content = [
        'export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch\n',
        'mkdir -p $GAUSS_SCRDIR\n',
        'module load gaussian/g16\n',
        'source /shared/centos7/gaussian/g16/bsd/g16.profile\n\n',

        'RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))\n',
        f'fname="{shell_label[:-8]}' + '${RUN_i}.com"\n\n',

        'g16 $fname\n',
    ]
    slurm_file_writer.write_file()

    # submit the job
    start_dir = os.getcwd()
    os.chdir(shell_dir)
    gaussian_shell_opt_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {slurm_run_file}"

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()
    gaussian_shell_opt_job.submit(slurm_cmd)
    os.chdir(start_dir)


if __name__ == '__main__':
    top_reactions = [915, 749, 324, 419, 1814, 1287, 748, 1288, 370, 1103,
        371, 213, 420, 581, 464, 1289, 720, 722, 1658, 574, 725, 1736,
        418, 1290, 1721, 1665, 1685, 427, 1714, 1766, 655, 1773, 1003, 650,
        985, 918, 585, 692, 1532, 1326, 1578, 1428, 916, 595, 693, 1242]
    
    if len(sys.argv) > 1:
        reaction_index = int(sys.argv[1])
        screen_reaction_ts(reaction_index)
    else:
        for rxn in top_reactions:
            print('Screen reaction', rxn)
            screen_reaction_ts(rxn)
            run_shell_opt(rxn)
    exit(0)
    # setup_arkane_species(87)
    # exit(0)

    # run one

    # if len(sys.argv) > 1:
    #     species_index = int(sys.argv[1])
    # else:
    #     species_index = 87
    # screen_conformers(species_index)
    # optimize_conformers(species_index)
    # exit(0)
    # run all
    # wait until # jobs is below 40 to start a new thing:
    import job_manager

    # for species_index in range(40, 65):
    # for species_index in range(15, 110):
    for species_index in range(0, 15):
        jobs_running = job_manager.count_slurm_jobs()
        while jobs_running > 40:
            time.sleep(60)
            jobs_running = job_manager.count_slurm_jobs()
        screen_species_conformers(species_index)
        optimize_conformers(species_index)
