# set of functions related to thermokinetic calculations

import os
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
    # DFT_DIR = "/work/westgroup/harris.se/autoscience/reaction_calculator/dft"
    DFT_DIR = "/home/moon/autoscience/reaction_calculator/dft"


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


def check_species_status(species_index, job_type):
    """Check the status of the part of the species calculation by looking in the status file"""
    status_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'status.yaml')
    if not os.path.exists(status_file):
        return False
    with open(status_file, 'r') as f:
        status = yaml.load(f, Loader=yaml.FullLoader)
    if job_type in status:
        return status[job_type]
    return False


def screen_conformers(species_index):
    """Sort through all the possible conformers and use a cheap calculator
    like Hotbit or LJ to screen the best options to investigate

    Takes a species index and saves the conformers to investigate as .pickle?
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    os.makedirs(conformer_dir, exist_ok=True)

    species_log(species_index, f'Starting conformers job')

    # check if the run was already completed
    if check_species_status(species_index, 'screen_conformers'):
        species_log(species_index, f'Conformers already ran')
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
    gaussian_conformers_job.submit(slurm_cmd)
    os.chdir(start_dir)


if __name__ == '__main__':
    species_index = 87
    screen_conformers(species_index)
