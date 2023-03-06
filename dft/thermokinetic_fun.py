# set of functions related to thermokinetic calculations

import os
import glob
import sys
import numpy as np
import pandas as pd
import time
import datetime
import yaml
import job_manager


import autotst.species
import autotst.calculator.gaussian


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


def species_index2smiles(species_index):
    """Function to return species smiles given a species index
    looks up the results in the species_list.csv
    """
    species_csv = os.path.join(DFT_DIR, 'species_list.csv')
    species_df = pd.read_csv(species_csv)
    species_index = species_df['SMILES'].values[species_index]
    return species_index


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


def set_species_status(species_index, job_type, job_status):
    """Set the status of the part of the species calculation by looking in the status file
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


def screen_conformers(species_index):
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

    # check if the run was already completed
    if get_species_status(species_index, 'screen_conformers'):
        species_log(species_index, f'Conformer screening already ran')
        return True

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
    if conformers_done_optimizing(species_index):
        species_log(species_index, f'Conformer optimization already ran')
        set_species_status(species_index, 'conformer_opt', True)
        return True

    n_conformers = len(glob.glob(os.path.join(conformer_dir, 'conformer_*.com')))
    restart = False
    rerun_indices = []
    for i in range(0, len(n_conforers)):
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


def conformers_done_optimizing(species_index, completion_threshold=0.9):
    """function to see if all the conformers are done optimizing, returns True if so"""
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    n_conformers = len(glob.glob(os.path.join(conformer_dir, 'conformer_*.com')))
    incomplete_indices = []
    good_runs = []
    finished_runs = []
    for i in range(0, n_conformers):
        conformer_file = os.path.join(conformer_dir, f'conformer_{i:04}.log')
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

    opt_completed = conformers_done_optimizing(species_index)
    while not opt_completed:
        time.sleep(60)
        opt_completed = conformers_done_optimizing(species_index)

    # write to the status file to indicate that the conformer screening is complete
    set_species_status(species_index, 'conformer_opt', True)
    species_log(species_index, f'Conformer optimization complete')


if __name__ == '__main__':
    # run one

    if len(sys.argv) > 1:
        species_index = int(sys.argv[1])
    else:
        species_index = 87
    screen_conformers(species_index)
    optimize_conformers(species_index)
    exit(0)
    # run all
    # wait until # jobs is below 40 to start a new thing:
    import job_manager

    # for species_index in range(40, 65):
    for species_index in range(101, 110):
        jobs_running = job_manager.count_slurm_jobs()
        while jobs_running > 40:
            time.sleep(60)
            jobs_running = job_manager.count_slurm_jobs()
        screen_conformers(species_index)
