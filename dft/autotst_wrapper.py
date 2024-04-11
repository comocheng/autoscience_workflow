# set of functions related to thermokinetic calculations

import os
import re
import glob
import sys
import numpy as np
import time
import datetime
import yaml
import job_manager

import arkane.ess.gaussian  # does a lot better at reading gaussian files than ase

import cclib.io

import rmgpy.species
import rmgpy.reaction
import rmgpy.data.kinetics

import autotst.species
import autotst.reaction
import autotst.calculator.gaussian
import autotst.calculator.vibrational_analysis


import autotst.conformer.systematic
import autotst.conformer.utilities


# import ase.io
import ase.constraints
import ase.io.zmatrix
import ase.io.gaussian
import ase.calculators.lj  # the backup built-in calculator. Do not use it for anything important
import ase.geometry.analysis

# maybe put this in a try block?
try:
    import xtb.ase.calculator
    # calc = xtb.ase.calculator.XTB()
except ImportError:
    print("xtb not installed")

try:
    import hotbit
except ImportError:
    print('hotbit not installed')


# for rotor scans
import zmatrix  # https://github.com/wutobias/r2z
from simtk import unit


# for arkane at end
import rmgpy.chemkin
import arkane.exceptions
import shutil


sys.path.append('/work/westgroup/harris.se/autoscience/reaction_calculator/database/')
import database_fun


try:
    DFT_DIR = os.environ['DFT_DIR']
except KeyError:
    DFT_DIR = "/work/westgroup/harris.se/autoscience/reaction_calculator/dft"

MAX_JOBS_RUNNING = 50
MAX_N_CONFORMERS = 100
MAX_JOBS_PER_TASK = 30


def get_termination_status(log_file):
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
    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}')
    logfile = os.path.join(reaction_dir, 'thermokinetic_fun.log')
    print(f'{datetime.datetime.now()} {message}')
    with open(logfile, 'a') as f:
        f.write(f'{datetime.datetime.now()} {message}' + '\n')


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
        - shell_setup
        - center_setup
        - overall_setup
        - shell_opt - run Gaussian to optimize the conformers
        - center_opt
        - overall_opt
        - arkane?
        - hfsp?
    """
    status_file = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}', 'status.yaml')
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
        # TODO delete screen_conformers?
        - shell_setup
        - center_setup
        - overall_setup
        - shell_opt - run Gaussian to optimize the conformers
        - center_opt
        - overall_opt
        - arkane?
    """
    status_file = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}', 'status.yaml')
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
        return f'{list_of_indices[0]},{list_of_indices[1]}'

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

    NOTE DO NOT USE LJ TO SCREEN CONFORMER GEOMETRIES. IT'S TERRIBLE
    It should only be used to test for obvious errors in the workflow if Hotbit is not installed

    Takes a species index and saves the conformers to investigate as .pickle?
    """
    if arkane_species_complete(species_index):
        return True

    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    if get_species_status(species_index, 'screen_conformers'):
        species_log(species_index, 'Conformers already screened')
        return True

    conformer_dir = os.path.join(species_dir, 'conformers')
    os.makedirs(conformer_dir, exist_ok=True)
    species_log(species_index, f'Starting conformer screening job')

    # ------------------ Use Hotbit to screen the conformers ------------------
    # Get species smiles
    rmg_species = database_fun.index2species(species_index)
    species_smiles = rmg_species.smiles
    # spec = autotst.species.Species(rmg_species=rmg_species)  # this probably won't work, so just run with smiles
    spec = autotst.species.Species([species_smiles])
    species_log(species_index, f'Loaded species {species_smiles}')

    try:
        calc = hotbit.Hotbit()
    except (NameError, RuntimeError):
        # if hotbit fails, use built-in lennard jones
        species_log(species_index, 'Using built-in ase LennardJones calculator instead of Hotbit. DO NOT DO THIS')
        calc = ase.calculators.lj.LennardJones()
    # hotbit can't handle Ar, He, change calculator to lj if it's in the species
    hotbit_skiplist = ['AR', 'HE', 'NE']
    for element in hotbit_skiplist:
        if element in species_smiles.upper():
            species_log(species_index, f'Using built-in ase LennardJones calculator instead of Hotbit for {element}')
            calc = ase.calculators.lj.LennardJones()
            break

    spec.generate_conformers(
        ase_calculator=calc,
        max_combos=1000,
        max_conformers=MAX_N_CONFORMERS,
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
    if arkane_species_complete(species_index):
        return True

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

    n_conformers = min(len(glob.glob(os.path.join(conformer_dir, 'conformer_*.com'))), MAX_N_CONFORMERS)
    rerun_indices = []
    for i in range(0, n_conformers):
        conformer_logfile = os.path.join(conformer_dir, f'conformer_{i:04}.log')
        if os.path.exists(conformer_logfile):
            termination_status = get_termination_status(conformer_logfile)
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
        '--array': f'0-{n_conformers - 1}%{MAX_JOBS_PER_TASK}',
    }
    if rerun_indices:
        slurm_run_file = os.path.join(conformer_dir, 'rerun.sh')
        slurm_settings['--partition'] = 'short'
        slurm_settings['--constraint'] = 'cascadelake'
        slurm_settings['--array'] = ordered_array_str(rerun_indices) + f'%{MAX_JOBS_PER_TASK}'
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


def write_scan_file(fname, conformer, torsion_index, degree_delta=20.0):
    """Function to write a Gaussian rotor scan
    Takes an autoTST conformer and a rotor index
    """

    # header
    scan_job_lines = [
        "%mem=5GB",
        "%nprocshared=48",
        "#P m062x/cc-pVTZ",
        "Opt=(CalcFC,ModRedun)",
        "",
        "Gaussian input for a rotor scan",
        "",
        f"0 {conformer.rmg_molecule.multiplicity}",
    ]
    rdmol = conformer._rdkit_molecule
    cart_crds = np.array(rdmol.GetConformers()[0].GetPositions()) * unit.angstrom
    zm = zmatrix.ZMatrix(conformer._rdkit_molecule)

    zm_text = zm.build_pretty_zcrds(cart_crds)
    zm_lines = zm_text.splitlines()
    bonds = []
    angles = []
    dihedrals = []
    b = 1  # indices for bonds
    a = 1
    d = 1
    for line in zm_lines:
        tokens = line.split()
        # print(line)
        if len(tokens) == 1:
            pass
        elif len(tokens) == 3:
            bonds.append(f'B{b}        {tokens[2]}')
            tokens[2] = f'B{b}'
            b += 1
        elif len(tokens) == 5:
            bonds.append(f'B{b}        {tokens[2]}')
            tokens[2] = f'B{b}'
            b += 1
            angles.append(f'A{a}        {tokens[4]}')
            tokens[4] = f'A{a}'
            a += 1
        elif len(tokens) == 7:
            bonds.append(f'B{b}        {tokens[2]}')
            tokens[2] = f'B{b}'
            b += 1
            angles.append(f'A{a}        {tokens[4]}')
            tokens[4] = f'A{a}'
            a += 1
            dihedrals.append(f'D{d}        {tokens[6]}')
            tokens[6] = f'D{d}'
            d += 1
            tokens.append('0')
        else:
            raise NotImplementedError

        scan_job_lines.append(' '.join(tokens))

    scan_job_lines.append("")
    for bond in bonds:
        scan_job_lines.append(bond)
    for angle in angles:
        scan_job_lines.append(angle)
    for dihedral in dihedrals:
        scan_job_lines.append(dihedral)
    scan_job_lines.append("")

    # # bond order and connectivity - not sure if this is needed
    # rdkit_bonds = zm.rdmol.GetBonds()
    # bond_list = [f'{i + 1}' for i in range(0, len(rdkit_bonds))]
    # for bond in rdkit_bonds:
    #     bond_start = zm.a2z(bond.GetBeginAtomIdx())
    #     bond_end = zm.a2z(bond.GetEndAtomIdx())
    #     bond_order = bond.GetBondTypeAsDouble()
    #     bond_list[bond_start] += f' {bond_end + 1} {bond_order}'
    # for bond in bond_list:
    #     scan_job_lines.append(bond)
    # scan_job_lines.append("")

    # dihedral to scan
    indices = conformer.torsions[torsion_index].atom_indices

    # # don't convert to z-matrix index??
    # first = indices[0] + 1
    # second = indices[1] + 1
    # third = indices[2] + 1
    # fourth = indices[3] + 1

    # convert to z-matrix index
    first = zm.a2z(indices[0]) + 1
    second = zm.a2z(indices[1]) + 1
    third = zm.a2z(indices[2]) + 1
    fourth = zm.a2z(indices[3]) + 1

    N_increments = int(360.0 / degree_delta)
    scan_job_lines.append(f"D {first} {second} {third} {fourth} S {N_increments} {float(degree_delta)}")

    scan_job_lines.append("")
    with open(fname, 'w') as f:
        for line in scan_job_lines:
            f.write(line + '\n')


def setup_rotors(species_index, increment_deg=20):
    """Find the lowest energy conformer of the species and then set up Gaussian rotors calculations
    """
    if arkane_species_complete(species_index):
        return True

    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    rotor_dir = os.path.join(species_dir, 'rotors')
    os.makedirs(rotor_dir, exist_ok=True)

    standard_increment = True
    rotor_str = 'rotor'
    if increment_deg != 20:
        standard_increment = False
        rotor_str = f'rotor{int(increment_deg)}'
        species_log(species_index, f'Non-standard rotor increment {increment_deg}')

    # check if the rotors were already set up
    rotor_logfiles = glob.glob(os.path.join(rotor_dir, f'{rotor_str}_*.com'))
    if rotor_logfiles:
        species_log(species_index, 'Rotors already set up')
        return True
    species_log(species_index, f'Starting species rotor setup')

    # # ------------------ Use Hotbit to screen the conformers ------------------
    # Get species smiles
    rmg_species = database_fun.index2species(species_index)
    species_smiles = rmg_species.smiles

    valid_conformer = False
    conformer_blacklist = []
    while not valid_conformer:
        conformer_file = get_lowest_energy_gaussian_file(conformer_dir, blacklist=conformer_blacklist)
        if not conformer_file:
            species_log(species_index, f'Failed to find lowest energy gaussian file in {conformer_dir}')
            species_log(species_index, f'Conformer blacklist is {conformer_blacklist}')

        if bonds_too_large(conformer_file, species_index):
            conformer_blacklist.append(conformer_file)
            species_log(species_index, f'Bonds too large for conformer {conformer_file}, blacklisting...')
        else:
            valid_conformer = True
            species_log(species_index, f'Lowest energy conformer is {conformer_file}')

        if len(conformer_blacklist) >= len(glob.glob(os.path.join(conformer_dir, 'conformer_*.log'))):
            species_log(species_index, f'No valid conformers found. Quitting...')
            return False

    new_conformer_loc = os.path.join(rotor_dir, os.path.basename(conformer_file))
    shutil.copy(conformer_file, new_conformer_loc)

    # get the rotors
    with open(new_conformer_loc, 'r') as f:
        atoms = ase.io.gaussian.read_gaussian_out(f)

    # make a conformer object again
    new_cf = autotst.species.Conformer(smiles=species_smiles)  # TODO make this from adjacency list?
    new_cf._ase_molecule = atoms
    new_cf.update_coords_from(mol_type="ase")
    torsions = new_cf.get_torsions()  # TODO - is this only the nonterminal ones?
    n_rotors = len(torsions)

    # TODO verify atom labeling produces correct torsion calculations
    # we need to verify that this gets the atom labeling correct, or else revert to the commented out section above

    if n_rotors == 0:
        no_rotor_file = os.path.join(rotor_dir, 'NO_ROTORS.txt')
        with open(no_rotor_file, 'w') as f:
            f.write('NO ROTORS')
        print("no rotors to calculate")
        return True

    print("generating gaussian input files")
    for i, torsion in enumerate(new_cf.torsions):
        fname = os.path.join(rotor_dir, f'{rotor_str}_{i:04}.com')
        write_scan_file(fname, new_cf, i, degree_delta=increment_deg)
    return True


def run_rotor_offset(species_index, rotor_index):
    rotor_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'rotors')

    # read the job file:
    species_log(species_index, f'Running offset rotors for rotor {rotor_index}')
    original_rotor_file = os.path.join(rotor_dir, f'rotor_{rotor_index:04}.com')
    with open(original_rotor_file, 'r') as f:
        lines = f.readlines()
        for i in range(1, 5):
            pattern = 'D\s(\d+ \d+ \d+ \d+) S '
            m1 = re.search(pattern, lines[-i])
            if m1:
                scanline_index = i
                scanline = lines[-i]
                break
        else:
            species_log(species_index, 'could not find scanline')
            print(lines)

    dihedral_indices = [int(x) for x in scanline.split()[1:5]]

    with open(original_rotor_file, 'r') as f:
        file_sections = ase.io.gaussian._get_gaussian_in_sections(f)
        mod_red = file_sections['mol_spec']

    z_text = ''.join(file_sections['mol_spec'])
    z_values_text = []
    for i, row in enumerate(file_sections['extra']):
        if not row.strip():
            break
        z_values_text.append(row)

    bonds = {}
    angles = {}
    dihedrals = {}
    for z_value_row in z_values_text:
        # look for bond
        bond_pattern = 'B\d\s*'
        m1 = re.search(bond_pattern, z_value_row)
        if m1:
            bond_name = z_value_row.split()[0]
            bond_value = float(z_value_row.strip().split()[-1])
            bonds[bond_name] = bond_value
            continue

        # look for angle
        angle_pattern = 'A\d\s*'
        m1 = re.search(angle_pattern, z_value_row)
        if m1:
            angle_name = z_value_row.split()[0]
            angle_value = float(z_value_row.strip().split()[-1])
            angles[angle_name] = angle_value

        # look for dihedral
        dihedral_pattern = 'D\d\s*'
        m1 = re.search(dihedral_pattern, z_value_row)
        if m1:
            dihedral_name = z_value_row.split()[0]
            dihedral_value = float(z_value_row.strip().split()[-1])
            dihedrals[dihedral_name] = dihedral_value

    # make the thing
    for bond_key in bonds.keys():
        z_text = z_text.replace(bond_key, str(bonds[bond_key]))
    for angle_key in angles.keys():
        z_text = z_text.replace(angle_key, str(angles[angle_key]))
    for dihedral_key in dihedrals.keys():
        z_text = z_text.replace(dihedral_key, str(dihedrals[dihedral_key]))
    atoms = ase.io.zmatrix.parse_zmatrix(z_text)

    # get the dihedral index
    dihedral_indices = [int(x) for x in scanline.split()[1:5]]
    dihedral_angle = atoms.get_dihedral(*[x - 1 for x in dihedral_indices])
    my_dihedral = []
    for key in dihedrals.keys():
        if np.isclose(dihedrals[key], dihedral_angle):
            my_dihedral.append(key)
        elif np.isclose(dihedrals[key], dihedral_angle - 360.0):
            my_dihedral.append(key)
        elif np.isclose(dihedrals[key], dihedral_angle + 360.0):
            my_dihedral.append(key)
    print(dihedrals)
    print(my_dihedral)
    print('ref', dihedral_angle)
    assert len(my_dihedral) == 1

    splice_dir = os.path.join(os.path.dirname(original_rotor_file), f'spliced_rotors')

    # test if it already ran
    if os.path.exists(os.path.join(splice_dir, f'rotor_{rotor_index:04}_fwd_0000.log')):
        species_log(species_index, f'Offset rotor {rotor_index} already ran')
        return

    os.makedirs(splice_dir, exist_ok=True)

    for i in range(0, 8):
        dihedral_rot = 45 * i
        file_name = os.path.join(splice_dir, f'rotor_{rotor_index:04}_fwd_{i:04}.com')
        file_lines = []
        for line in lines:
            if line.startswith(my_dihedral[0] + ' '):
                # rotate it the amount
                line = my_dihedral[0] + ' ' + str(dihedrals[my_dihedral[0]] + dihedral_rot) + '\n'
            file_lines.append(line)
        with open(file_name, 'w') as f:
            f.writelines(file_lines)

    # Make slurm scripts to run all the rotors
    fwd_label = f'rotor_{rotor_index:04}_fwd_'
    slurm_run_file = os.path.join(splice_dir, f'run_{rotor_index:04}_fwd.sh')
    slurm_settings = {
        '--job-name': f'g16_sp{species_index}_rot{rotor_index}',
        '--error': 'error.log',
        '--nodes': 1,
        '--partition': 'short,west',
        # '--constraint': 'cascadelake',
        '--mem': '20Gb',
        '--time': '24:00:00',
        '--cpus-per-task': 16,
        '--array': f'0-7',
    }

    slurm_file_writer = job_manager.SlurmJobFile(full_path=slurm_run_file)
    slurm_file_writer.settings = slurm_settings
    slurm_file_writer.content = [
        'export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch\n',
        'mkdir -p $GAUSS_SCRDIR\n',
        'module load gaussian/g16\n',
        'source /shared/centos7/gaussian/g16/bsd/g16.profile\n\n',

        'RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))\n',
        f'fname="{fwd_label}' + '${RUN_i}.com"\n\n',

        'g16 $fname\n',
    ]
    slurm_file_writer.write_file()

    # submit the job
    start_dir = os.getcwd()
    os.chdir(splice_dir)
    gaussian_rotors_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {slurm_run_file}"

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()

    gaussian_rotors_job.submit(slurm_cmd)
    os.chdir(start_dir)


def run_rotors(species_index, increment_deg=20):
    """Run the rotor scans that were set up"""
    if arkane_species_complete(species_index):
        return True

    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    rotor_dir = os.path.join(species_dir, 'rotors')

    # skip running rotors if the NO_ROTORS file is present
    no_rotor_file = os.path.join(rotor_dir, 'NO_ROTORS.txt')
    if os.path.exists(no_rotor_file):
        species_log(species_index, f'No rotors to run. Skipping...')
        return True

    standard_increment = True
    rotor_str = 'rotor'
    suffix = ''
    if increment_deg != 20:
        standard_increment = False
        rotor_str = f'rotor{int(increment_deg)}'
        suffix = f'{int(increment_deg)}'

    # check if the rotors were already completed (might setup rerun even if already ran once)
    if conformers_done_optimizing(rotor_dir, completion_threshold=1.0, base_name=f'{rotor_str}_'):
        return True  # already ran

    species_log(species_index, f'Counting incomplete rotor scans...')
    rerun_indices = []
    n_rotors = len(glob.glob(os.path.join(rotor_dir, f'{rotor_str}_*.com')))
    for i in range(0, n_rotors):
        rotor_logfile = os.path.join(rotor_dir, f'{rotor_str}_{i:04}.log')
        if os.path.exists(rotor_logfile):
            termination_status = get_termination_status(rotor_logfile)
            if termination_status == 1 or termination_status == -1:
                rerun_indices.append(i)
                species_log(species_index, f'Rotor {i} did not complete')

    rotor_logfiles = glob.glob(os.path.join(rotor_dir, f'{rotor_str}_*.log'))
    if len(rotor_logfiles) == n_rotors and not rerun_indices:
        species_log(species_index, 'Rotors already ran')
        return True

    species_log(species_index, f'Starting rotor scans optimization job')
    # Make slurm script to run all the rotor calculations
    slurm_run_file = os.path.join(rotor_dir, f'run{suffix}.sh')
    slurm_settings = {
        '--job-name': f'g16_rot_{species_index}',
        '--error': 'error.log',
        '--nodes': 1,
        '--partition': 'west,short',
        '--exclude': 'c5003',
        '--mem': '20Gb',
        '--time': '24:00:00',
        '--cpus-per-task': 16,
        '--array': f'0-{n_rotors - 1}%{MAX_JOBS_PER_TASK}',
    }

    # ------------------ ROTOR OFFSET METHOD ----------------------
    if rerun_indices:
        # run the rotors using the offset method
        for rotor_index in rerun_indices:
            run_rotor_offset(species_index, rotor_index)

    else:
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
            'fname="' + rotor_str + '_${RUN_i}.com"\n\n',

            'g16 $fname\n',
        ]
        slurm_file_writer.write_file()

        # submit the job
        start_dir = os.getcwd()
        os.chdir(rotor_dir)
        gaussian_rotors_job = job_manager.SlurmJob()
        slurm_cmd = f"sbatch {slurm_run_file}"

        # wait for fewer than MAX_JOBS_RUNNING jobs running
        jobs_running = job_manager.count_slurm_jobs()
        while jobs_running > MAX_JOBS_RUNNING:
            time.sleep(60)
            jobs_running = job_manager.count_slurm_jobs()

        gaussian_rotors_job.submit(slurm_cmd)
        os.chdir(start_dir)


def conformers_done_optimizing(base_dir, completion_threshold=0.6, base_name='conformer_'):
    """function to see if all the conformers are done optimizing, returns True if so"""
    glob_str = os.path.join(base_dir, f'{base_name}*.com')
    # print(f'glob str is {glob_str}')
    n_conformers = len(glob.glob(glob_str))
    if n_conformers == 0:
        print(f'No conformers with glob string {glob_str}')
        return False

    unlisted_runs = []
    incomplete_indices = []
    good_runs = []
    finished_runs = []
    # for i in range(0, n_conformers):
    for i in range(0, MAX_N_CONFORMERS):
        conformer_file = os.path.join(base_dir, f'{base_name}{i:04}.log')
        if not os.path.exists(conformer_file):
            unlisted_runs.append(i)
            continue
        opt_status = get_termination_status(conformer_file)
        if opt_status == 0:
            good_runs.append(i)
            finished_runs.append(i)
        elif opt_status == 1 or opt_status == 2 or opt_status == 3 or opt_status == 4 or opt_status == 5:
            # not good optimizations, but we're going to keep going anyways
            finished_runs.append(i)
        else:
            # optimization didn't finish (-1)
            incomplete_indices.append(i)
    if len(finished_runs) / float(n_conformers) >= completion_threshold and len(good_runs) > 0:
        return True

    print('Not done optimizing:')
    print(len(finished_runs) / float(n_conformers))
    print(f'{len(finished_runs) } finished')
    print(f'{len(good_runs) } good')
    print(f'{len(incomplete_indices) } incomplete')
    print(f'{len(unlisted_runs) } unlisted')
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


def get_gaussian_file_geometry(gaussian_log_file):
    """Function to get the ase atoms object from a Gaussian .log file"""
    with open(gaussian_log_file, 'r') as f:
        # check that it's really a gaussian file
        line = f.readline()
        if 'Gaussian' not in line:
            return None
        f.seek(0)
        atoms = ase.io.gaussian.read_gaussian_out(f)
        return atoms


def get_lowest_energy_gaussian_file(base_dir, blacklist=[]):
    """Function to get the lowest energy gaussian .log file from a directory"""
    lowest_energy = 1e6
    lowest_file = None
    log_files = glob.glob(os.path.join(base_dir, '*.log'))
    for gaussian_log_file in log_files:
        if gaussian_log_file in blacklist:
            continue

        try:
            energy = get_gaussian_file_energy(gaussian_log_file)
        except arkane.exceptions.LogError:
            continue
        if energy is None:
            continue
        if energy < lowest_energy:
            lowest_energy = energy
            lowest_file = gaussian_log_file
    return lowest_file


def bonds_too_large(conformer_file, species_index):
    """Function to check whether the bonds are too big to make sense for a given species"""

    with open(conformer_file, 'r') as f:
        atoms = ase.io.gaussian.read_gaussian_out(f)

    # make a conformer object again
    rmg_species = database_fun.index2species(species_index)
    species_smiles = rmg_species.smiles
    new_cf = autotst.species.Conformer(smiles=species_smiles)
    new_cf._ase_molecule = atoms
    new_cf.update_coords_from(mol_type="ase")

    for bond in new_cf.get_bonds():
        bondtype = new_cf._ase_molecule[bond.atom_indices[0]].symbol + \
            new_cf._ase_molecule[bond.atom_indices[1]].symbol

        if 'H' in bondtype:
            threshold = 1.5 * 1.0932774602784967  # C-H in butane
        else:
            threshold = 1.5 * 1.5240247836472345  # C-C in butane

        if new_cf._ase_molecule.get_distances(*bond.atom_indices)[0] > threshold:
            return True

    return False


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


def write_arkane_conformer_file(conformer, gauss_log, arkane_dir, include_rotors=True):
    # assume rotor and conformer logs have already been copied into the arkane directory
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


def setup_arkane_species(species_index, include_rotors=True):
    """Function to set up the Arkane species directory for a given species
    default is to not do rotors. But if rotors are specified, the arkane directory
    will be arkane_rotors

    TODO add force recalc option to rerun calculation from scratch
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    rotor_dir = os.path.join(species_dir, 'rotors')
    arkane_dir = os.path.join(species_dir, 'arkane')
    os.makedirs(arkane_dir, exist_ok=True)

    species_log(species_index, f'Setting up Arkane species with rotors={include_rotors}')
    if arkane_species_complete(species_index):
        species_log(species_index, f'Arkane species already complete')
        return True

    rmg_species = database_fun.index2species(species_index)
    species_smiles = rmg_species.smiles
    # make a conformer object from the RMG species
    # AutoTST converts the molecule back into SMILES, but we're ignoring this for now
    # new_cf = autotst.species.Conformer(rmg_molecule=rmg_species.molecule[0])
    new_cf = autotst.species.Conformer(smiles=species_smiles)
    # read the conformer geometry from the file

    if include_rotors:
        # copy the conformer file in the rotors dir
        conformer_files = glob.glob(os.path.join(rotor_dir, 'conformer_*.log'))
        assert conformer_files, 'No conformer files in rotor dir'
        conformer_file = conformer_files[0]

        # copy the rotor files
        rotor_files = glob.glob(os.path.join(rotor_dir, 'rotor_*.log'))
        for rotor_file in rotor_files:
            shutil.copy(rotor_file, arkane_dir)
    else:
        conformer_file = get_lowest_energy_gaussian_file(conformer_dir)

    shutil.copy(conformer_file, arkane_dir)
    with open(conformer_file, 'r') as f:
        atoms = ase.io.gaussian.read_gaussian_out(f)

    new_cf._ase_molecule = atoms
    new_cf.update_coords_from(mol_type="ase")
    if include_rotors:
        torsions = new_cf.get_torsions()
        assert len(torsions) == len(rotor_files)

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


def run_arkane_species(species_index):
    # Run the arkane job
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    arkane_dir = os.path.join(species_dir, 'arkane')

    if arkane_species_complete(species_index):
        species_log(species_index, f'arkane already ran for species {species_index}')
        return True

    # Run the arkane job
    arkane_run_file = os.path.join(arkane_dir, 'run_arkane.sh')
    if not os.path.exists(arkane_run_file):
        species_log(species_index, f'arkane run not set up for species {species_index}')
        return False

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()

    start_dir = os.getcwd()
    os.chdir(arkane_dir)
    arkane_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {arkane_run_file}"
    arkane_job.submit(slurm_cmd)
    os.chdir(start_dir)


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


def setup_opt(reaction_index, opt_type, direction='forward', max_combos=1000, max_conformers=100):
    """Function to set up the gaussian files for a particular opt type
    screens the conformers using hotbit, then writes the gaussian input files
    types are 'shell', 'center', 'overall', 'hfsp', 'hfsp_shell', 'hfsp_overall'

    shell freezes 3 core atoms of reaction and relaxes the rest of the molecule
    center optimizes 3 core atoms of reaction to TS and freezes the rest of the molecule
    overall optimizes the entire molecule to TS

    hfsp - harmonically forced saddle point runs a TS optimization from initial HFSP guess
    hfsp_shell - freeze the 3 core atoms and relax molecule using HFSP initial guess
    hfsp_overall - use the result of hfsp to run TS optimization
    """

    assert opt_type in ['shell', 'center', 'overall', 'hfsp', 'hfsp_shell', 'hfsp_overall'], f'opt_type must be one of shell, center, overall, hfsp, hfsp_shell, hfsp_overall. Got {opt_type}'

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}')
    if not os.path.exists(reaction_dir):
        os.makedirs(reaction_dir, exist_ok=True)
    screen_dir = os.path.join(reaction_dir, 'screen')
    if not os.path.exists(screen_dir):
        os.makedirs(screen_dir, exist_ok=True)
    reaction_log(reaction_index, f'Starting {opt_type} opt job')

    # TODO - I don't like this status system. (get_reaction_status) A status file is not the actual status and the extra layer makes things worse. Get rid of it
    # check if the opt setup is already complete. But there should be some time-saving check before running autotst
    if get_reaction_status(reaction_index, f'{opt_type}_setup') or \
       get_reaction_status(reaction_index, f'{opt_type}_opt'):
        reaction_log(reaction_index, f'{opt_type} opt setup complete')
        return True

    screen_dir = os.path.join(reaction_dir, 'screen')
    opt_dir = os.path.join(reaction_dir, opt_type)
    os.makedirs(opt_dir, exist_ok=True)

    opt_label = 'fwd_ts_0000.log'
    if direction == 'reverse':
        opt_label = 'rev_ts_0000.log'

    # don't run center if shell isn't complete and
    # don't run overall if center isn't complete
    # don't run hfsp_overall if hfsp_shell isn't complete
    if opt_type == 'center':
        shell_dir = os.path.join(reaction_dir, 'shell')
        if get_reaction_status(reaction_index, 'shell_opt'):
            pass
        elif conformers_done_optimizing(shell_dir, base_name=opt_label[:-8]):
            set_reaction_status(reaction_index, 'shell_opt', True)
        else:
            reaction_log(reaction_index, f'Center opt setup incomplete, shell opt not complete')
            return False
    elif opt_type == 'overall':
        center_dir = os.path.join(reaction_dir, 'center')
        if get_reaction_status(reaction_index, 'center_opt'):
            pass
        elif conformers_done_optimizing(center_dir, base_name=opt_label[:-8]):
            set_reaction_status(reaction_index, 'center_opt', True)
        else:
            reaction_log(reaction_index, f'Overall opt setup incomplete, center opt not complete')
            return False
    elif opt_type == 'hfsp_overall':
        hfsp_shell_dir = os.path.join(reaction_dir, 'hfsp_shell')
        if get_reaction_status(reaction_index, 'hfsp_shell_opt'):
            pass
        elif conformers_done_optimizing(hfsp_shell_dir, base_name=opt_label[:-8]):
            set_reaction_status(reaction_index, 'hfsp_shell_opt', True)
        else:
            reaction_log(reaction_index, f'Cannot run hfsp_overall opt setup because hfsp_shell opt not complete')
            return False

    # ------------------ Use Hotbit to screen the conformers ------------------
    # Get reaction from index
    rmg_reaction = database_fun.index2reaction(reaction_index)
    reaction_log(reaction_index, f'Constructing reaction in AutoTST...')
    # Note that AutoTST uses SMILES instead of adjacency list, but we'll worry about that later
    reaction = autotst.reaction.Reaction(rmg_reaction=rmg_reaction)
    # smiles = database_fun.reaction2smiles(rmg_reaction)
    # reaction = autotst.reaction.Reaction(label=smiles)
    reaction.get_labeled_reaction()
    # TODO - log something about not finding a match if a match isn't found- see reaction #50 for example

    reaction.get_label()
    reaction.ts[direction][0].get_molecules()

    try:  # TODO fix issues with import in a try block
        calc = hotbit.Hotbit()
    except (NameError, RuntimeError):
        # if hotbit fails, use built-in lennard jones
        reaction_log(reaction_index, 'Using built-in ase LennardJones calculator instead of Hotbit')
        # If we're on Discovery, you need to abort this. This is bad.
        if job_manager.get_user() == 'harris.se':
            raise ImportError('You really need to use Hotbit or xtb. LJ is not good enough sorry')
        calc = ase.calculators.lj.LennardJones()
    reaction.generate_conformers(
        ase_calculator=calc,
        max_combos=max_combos,
        max_conformers=max_conformers,
        save_results=True,
        results_dir=screen_dir,
    )
    reaction_log(reaction_index, f'Done generating conformers in AutoTST...')
    reaction_log(reaction_index, f'{len(reaction.ts[direction])} conformers found')

    # -------------- Write the results as gaussiuan calculations in the shell dir
    # Check for already finished shell logfiles
    # first, return if all of them have finished
    for i in range(0, len(reaction.ts[direction])):
        if i > max_conformers:
            reaction_log(reaction_index, f'Maximum conformers reached ({max_conformers}). Moving on...')
            break

        opt_label = opt_label[:-8] + f'{i:04}.log'

        ts = reaction.ts[direction][i]

        # -------- Adjust the starting geometry to result of previous run if applicable --------------
        if opt_type in ['hfsp' or 'hfsp_shell']:
            # Use HFSP to come up with the TS starting geometry
            if reaction.rmg_reaction.family not in ['Disproportionation', 'H_Abstraction']:
                raise NotImplementedError('HFSP opt only implemented for Disproportionation and H_Abstraction reactions')
            try:
                d14, d24 = get_HFSP_bond_distances(reaction)  # <---- this takes a while and is the same for each conformer so only run once
            except KeyError:
                d14, d24 = get_HFSP_bond_distances(reaction, reverse=True)
            new_ase_molecule = get_HFSP_TS_guess(reaction, d14, d24, i)

            # update the molecule with the new coordinates
            reaction.ts[direction][i]._ase_molecule = new_ase_molecule
            reaction.ts[direction][i].update_coords_from(mol_type="ase")
        elif opt_type == 'hfsp_overall':
            # set the geometry to hfsp_shell result
            starting_geometry_file = os.path.join(hfsp_shell_dir, opt_label)
            if not os.path.exists(starting_geometry_file) or get_termination_status(starting_geometry_file) != 0:
                continue  # could just pass over this, but it seems like a waste of computation time to run the calc
            reaction.ts[direction][i]._ase_molecule = get_gaussian_file_geometry(starting_geometry_file)
            reaction.ts[direction][i].update_coords_from(mol_type="ase")
        elif opt_type == 'center':
            # set the geometry to shell result
            starting_geometry_file = os.path.join(shell_dir, opt_label)
            if not os.path.exists(starting_geometry_file) or get_termination_status(starting_geometry_file) != 0:
                continue
            reaction.ts[direction][i]._ase_molecule = get_gaussian_file_geometry(starting_geometry_file)
            reaction.ts[direction][i].update_coords_from(mol_type="ase")
        elif opt_type == 'overall':
            # set the geometry to shell result
            starting_geometry_file = os.path.join(center_dir, opt_label)
            if not os.path.exists(starting_geometry_file) or get_termination_status(starting_geometry_file) != 0:
                continue
            reaction.ts[direction][i]._ase_molecule = get_gaussian_file_geometry(starting_geometry_file)
            reaction.ts[direction][i].update_coords_from(mol_type="ase")

        gaussian = autotst.calculator.gaussian.Gaussian(conformer=ts)
        if opt_type in ['shell', 'hfsp_shell']:
            calc = gaussian.get_shell_calc()
        elif opt_type == 'center':
            calc = gaussian.get_center_calc()
        elif opt_type in ['overall', 'hfsp', 'hfsp_overall']:
            calc = gaussian.get_overall_calc()
        else:
            raise ValueError(f'opt_type must be one of shell, center, overall, hfsp, hfsp_shell, hfsp_overall. Got {opt_type}')
        calc.label = opt_label[:-4]
        calc.directory = opt_dir
        calc.parameters.pop('scratch')
        calc.parameters.pop('multiplicity')
        calc.parameters['mult'] = ts.rmg_molecule.multiplicity
        calc.write_input(ts.ase_molecule)

        # Get rid of double-space between xyz block and mod-redundant section
        delete_double_spaces(os.path.join(opt_dir, calc.label + '.com'))

    # write to the status file to indicate that the conformer screening is complete
    set_reaction_status(reaction_index, f'{opt_type}_setup', True)
    reaction_log(reaction_index, f'{opt_type} setup complete')
    return True


def run_opt(reaction_index, opt_type, direction='forward'):
    """Run a shell, center, or overall optimization
    opt_type can be 'shell', 'center', or 'overall'
    and now, HFSP
    """
    assert opt_type in ['shell', 'center', 'overall', 'hfsp', 'hfsp_shell', 'hfsp_overall']

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}')
    opt_dir = os.path.join(reaction_dir, opt_type)

    if not os.path.exists(opt_dir):
        reaction_log(reaction_index, f'{opt_type} optimization not set up yet')
        return False

    reaction_log(reaction_index, f'Starting {opt_type} optimization job')

    # manually check if the center optimizations are complete
    opt_label = 'fwd_ts_0000.log'
    if direction == 'reverse':
        opt_label = 'rev_ts_0000.log'

    # check if the run was already completed
    if get_reaction_status(reaction_index, f'{opt_type}_opt'):
        reaction_log(reaction_index, f'{opt_type} optimization already ran')
        return True
    elif conformers_done_optimizing(opt_dir, base_name=opt_label[:-8]):
        reaction_log(reaction_index, f'{opt_type} optimization already ran')
        set_reaction_status(reaction_index, f'{opt_type}_opt', True)
        return True

    com_files = glob.glob(os.path.join(opt_dir, f'{opt_label[:-8]}*.com'))
    n_conformers = len(com_files)
    rerun_indices = []
    for i in range(0, n_conformers):
        conformer_logfile = os.path.join(opt_dir, f'{opt_label[:-8]}{i:04}.log')
        if os.path.exists(conformer_logfile):
            termination_status = get_termination_status(conformer_logfile)
            if termination_status == 1 or termination_status == -1:
                rerun_indices.append(i)

    # Make slurm script to run all the conformer calculations
    slurm_run_file = os.path.join(opt_dir, 'run.sh')
    slurm_settings = {
        '--job-name': f'g16_{opt_type}_{reaction_index}',
        '--error': 'error.log',
        '--nodes': 1,
        '--partition': 'west,short',
        '--exclude': 'c5003',
        '--mem': '20Gb',
        '--time': '24:00:00',
        '--cpus-per-task': 16,
        '--array': f'0-{n_conformers - 1}%{MAX_JOBS_PER_TASK}',
    }

    # need to reformat the array to include the conformers whose previous runs worked
    if opt_type != 'shell' and opt_type != 'hfsp_shell':
        pattern = '(\d\d\d\d).com'  # get the conformer index on each .com file (last 4 digits before .com)
        to_run_indices = []
        for com_file in com_files:
            m1 = re.search(pattern, com_file)
            if not m1:
                raise OSError(f'could not find relevant .com files! for {opt_type} opt')
            to_run_indices.append(int(m1.groups()[0]))
        slurm_settings['--array'] = ordered_array_str(to_run_indices) + f'%{MAX_JOBS_PER_TASK}'

    if rerun_indices:
        slurm_run_file = os.path.join(opt_dir, 'rerun.sh')
        slurm_settings['--partition'] = 'short'
        slurm_settings['--constraint'] = 'cascadelake'
        slurm_settings['--array'] = ordered_array_str(rerun_indices) + f'%{MAX_JOBS_PER_TASK}'
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
        f'fname="{opt_label[:-8]}' + '${RUN_i}.com"\n\n',

        'g16 $fname\n',
    ]
    slurm_file_writer.write_file()

    # submit the job
    start_dir = os.getcwd()
    os.chdir(opt_dir)
    gaussian_opt_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {slurm_run_file}"

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()
    reaction_log(reaction_index, f'Running SLURM job: {slurm_cmd}')
    gaussian_opt_job.submit(slurm_cmd)
    os.chdir(start_dir)


def check_vib_irc(reaction_index, gaussian_logfile):
    """Function to check if the TS optimization was successful
    """
    # check for valid termination status
    termination_status = get_termination_status(gaussian_logfile)
    if termination_status != 0:
        reaction_log(reaction_index, 'logfile did not terminate normally')
        return False

    reaction_smiles = database_fun.reaction_index2smiles(reaction_index)
    reaction = autotst.reaction.Reaction(label=reaction_smiles)

    # rmg_reaction = database_fun.index2reaction(reaction_index)
    # reaction = autotst.reaction.Reaction(rmg_reaction=rmg_reaction)

    va = autotst.calculator.vibrational_analysis.VibrationalAnalysis(
        transitionstate=reaction.ts['forward'][0], log_file=gaussian_logfile
    )
    result, connect_the_dots_result = va.validate()

    # we'll be lenient: one large negative freq is enough
    freqs = np.array([vib[0] for vib in va.vibrations])
    one_negative = np.sum(freqs < 0)
    large_negative = freqs[0] < -600
    one_large_negative = one_negative and large_negative

    # result, connect_the_dots_result = va.validate_ts()
    if result or connect_the_dots_result or one_large_negative:
        if result or connect_the_dots_result:
            reaction_log(reaction_index, 'TS is valid')
        elif one_large_negative:
            reaction_log(reaction_index, 'TS is probably valid')
    else:
        reaction_log(reaction_index, 'TS is not valid')
    return result or connect_the_dots_result or one_large_negative


def arkane_reaction_complete(reaction_index):
    return os.path.exists(os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}', 'arkane', 'RMG_libraries', 'reactions.py'))


def setup_arkane_reaction(reaction_index, direction='forward', force_valid_ts=False, overall_dirname='overall'):
    """Function to setup the arkane job for a reaction
    overall_dirname is where to get the TS logs from, alternatives are 'hfsp' and 'hfsp_overall'
    """
    # check if the arkane job was already completed
    if get_reaction_status(reaction_index, 'arkane_calc'):
        reaction_log(reaction_index, 'Arkane job already ran')
        return True
    elif arkane_reaction_complete(reaction_index):
        set_reaction_status(reaction_index, 'arkane_setup', True)
        set_reaction_status(reaction_index, 'arkane_calc', True)
        reaction_log(reaction_index, 'Arkane job already ran')
        return True

    # # Check for overall job status completion
    # if not get_reaction_status(reaction_index, 'overall_opt'):
    #    reaction_log(reaction_index, 'Cannot run arkane until overall job is complete')
    #    return False

    reaction_smiles = database_fun.reaction_index2smiles(reaction_index)
    reaction_log(reaction_index, f'starting setup_arkane_reaction for reaction {reaction_index} {reaction_smiles}')

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}')
    overall_dir = os.path.join(reaction_dir, overall_dirname)
    arkane_dir = os.path.join(reaction_dir, 'arkane')
    os.makedirs(arkane_dir, exist_ok=True)

    species_dict_file = "/work/westgroup/harris.se/autoscience/autoscience/butane/models/rmg_model/species_dictionary.txt"
    species_dict = rmgpy.chemkin.load_species_dictionary(species_dict_file)

    def get_sp_name(smiles):
        # if smiles == '[CH2]C=CC':  # manually change to resonance structures included in model
        #     smiles = 'C=C[CH]C'
        # elif smiles == '[CH2][CH]C=C':
        #     smiles = '[CH2]C=C[CH2]'
        for entry in species_dict.keys():
            if species_dict[entry].smiles == smiles:
                return str(species_dict[entry])
        # need to look for isomorphism
        reaction_log(reaction_index, f'Failed to get species name for {smiles}')
        return smiles

    def get_reaction_label(rmg_reaction):
        label = ''
        for reactant in rmg_reaction.reactants:
            label += get_sp_name(reactant.smiles) + ' + '
        label = label[:-2]
        label += '<=> '
        for product in rmg_reaction.products:
            label += get_sp_name(product.smiles) + ' + '
        label = label[:-3]
        return label

    # Read in the reaction
    rmg_reaction = database_fun.index2reaction(reaction_index)
    reaction = autotst.reaction.Reaction(label=reaction_smiles)  # going back to this even though it's not dependable
    # reaction = autotst.reaction.Reaction(rmg_reaction=rmg_reaction)
    reaction_log(reaction_index, f'Creating arkane files for reaction {reaction_index} {reaction.label}')
    reaction.ts[direction][0].get_molecules()

    # pick the lowest energy valid transition state:
    TS_logs = glob.glob(os.path.join(overall_dir, f'fwd_ts_*.log'))
    TS_log = ''
    lowest_energy = 1e5
    for logfile in TS_logs:
        # skip if the TS is not valid
        if not force_valid_ts:
            if not check_vib_irc(reaction_index, logfile):
                continue

        # skip if the bonds don't match what's expected
        if not verify_bond_count(reaction_index, gaussian_file=logfile):
            continue

        try:
            g_reader = arkane.ess.gaussian.GaussianLog(logfile)
            energy = g_reader.load_energy()
            if energy < lowest_energy:
                lowest_energy = energy
                TS_log = logfile
        except arkane.exceptions.LogError:
            print(f'skipping bad logfile {logfile}')
            continue
    if not TS_log:
        raise ValueError('No Valid TS found')

    # -------------------- Write the input file ---------------------- #
    model_chemistry = 'M06-2X/cc-pVTZ'
    lines = [
        f'modelChemistry = "{model_chemistry}"\n',
        'useHinderedRotors = False\n',
        'useBondCorrections = False\n\n',
    ]

    completed_species = []
    for reactant in reaction.rmg_reaction.reactants + reaction.rmg_reaction.products:
        # check for duplicates
        duplicate = False
        for sp in completed_species:
            if reactant.is_isomorphic(sp):
                duplicate = True
        if duplicate:
            continue

        reaction_log(reaction_index, f'{reactant}')
        species_index = database_fun.get_unique_species_index(reactant)
        species_smiles = reactant.smiles

        # TODO add all resonance structures to the model separately

        # if species_smiles == '[CH2]C=CC':  # TODO clean up this fix where we manually switch back to other resonance structure
        #     species_smiles = 'C=C[CH]C'
        # elif species_smiles == '[CH2][CH]C=C':
        #     species_smiles = '[CH2]C=C[CH2]'
        species_name = get_sp_name(species_smiles)
        species_arkane_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'arkane')
        try:
            species_file = os.path.join(f'species_{species_index:04}', os.path.basename(glob.glob(os.path.join(species_arkane_dir, 'conformer_*.py'))[0]))
        except IndexError:
            # automatically start the process of running the missing species...
            reaction_log(reaction_index, f'Missing species conformer file {species_arkane_dir}')
            reaction_log(reaction_index, f'Starting species calculation for species {species_index}: {species_smiles}')
            screen_species_conformers(species_index)
            optimize_conformers(species_index)

            raise IndexError(f'No species conformer file found in {species_arkane_dir}')

        try:
            shutil.copytree(species_arkane_dir, os.path.join(arkane_dir, f'species_{species_index:04}'))
        except FileExistsError:
            pass

        # TODO - use adjacency list in Arkane calculation instead of SMILES
        # TODO - copy the species into the destination so the arkane calculation can be copied and redone elsewhere
        lines.append(f'species("{species_name}", "{species_file}", structure=SMILES("{species_smiles}"))\n')
        lines.append(f'thermo("{species_name}", "NASA")\n\n')

        completed_species.append(reactant)

    lines.append('\n')

    TS_name = 'TS'
    TS_file = 'TS.py'
    TS_arkane_path = os.path.join(arkane_dir, TS_file)
    shutil.copy(TS_log, arkane_dir)

    lines.append(f'transitionState("{TS_name}", "{TS_file}")\n')

    reaction_label = get_reaction_label(reaction.rmg_reaction)
    reactants = [get_sp_name(reactant.smiles) for reactant in reaction.rmg_reaction.reactants]
    products = [get_sp_name(product.smiles) for product in reaction.rmg_reaction.products]
    lines.append(f'reaction(\n')
    lines.append(f'    label = "{reaction_label}",\n')
    lines.append(f'    reactants = {reactants},\n')
    lines.append(f'    products = {products},\n')
    lines.append(f'    transitionState = "{TS_name}",\n')
    lines.append(f'#    tunneling = "Eckart",\n')
    lines.append(f')\n\n')

    lines.append(f'statmech("{TS_name}")\n')
    lines.append(f'kinetics("{reaction_label}")\n\n')

    # write the TS file
    ts_lines = [
        'energy = {"' + f'{model_chemistry}": Log("{os.path.basename(TS_log)}")' + '}\n\n',
        'geometry = Log("' + f'{os.path.basename(TS_log)}")' + '\n\n',
        'frequencies = Log("' + f'{os.path.basename(TS_log)}")' + '\n\n',
    ]
    with open(TS_arkane_path, 'w') as g:
        g.writelines(ts_lines)

    arkane_input_file = os.path.join(arkane_dir, 'input.py')
    with open(arkane_input_file, 'w') as f:
        f.writelines(lines)
    # ----------------------------------------------------------------- #

    # make the slurm script to run arkane
    run_script = os.path.join(arkane_dir, 'run_arkane.sh')
    with open(run_script, 'w') as f:
        # Run on express
        f.write('#!/bin/bash\n')
        f.write('#SBATCH --partition=express,short,west\n')
        f.write('#SBATCH --time=00:20:00\n\n')
        f.write('python ~/rmg/RMG-Py/Arkane.py input.py\n\n')

    reaction_log(reaction_index, f'finished setting up arkane for reaction {reaction_index} {reaction_label}')
    set_reaction_status(reaction_index, 'arkane_setup', True)


def run_arkane_reaction(reaction_index, direction='forward'):
    # Run the arkane job

    # check if the arkane job was already completed
    if get_reaction_status(reaction_index, 'arkane_calc'):
        reaction_log(reaction_index, 'Arkane job already ran')
        return True
    elif arkane_reaction_complete(reaction_index):
        set_reaction_status(reaction_index, 'arkane_setup', True)
        set_reaction_status(reaction_index, 'arkane_calc', True)
        reaction_log(reaction_index, 'Arkane job already ran')
        return True
    elif not get_reaction_status(reaction_index, 'arkane_setup'):
        reaction_log(reaction_index, 'Arkane job not set up.')
        return False

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}')
    arkane_dir = os.path.join(reaction_dir, 'arkane')

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()

    # Run the arkane job
    arkane_run_file = os.path.join(arkane_dir, 'run_arkane.sh')
    start_dir = os.getcwd()
    os.chdir(arkane_dir)
    arkane_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {arkane_run_file}"
    arkane_job.submit(slurm_cmd)
    os.chdir(start_dir)


def get_HFSP_bond_distances(reaction):
    """Function to estimate the bond distances for the formed and unformed bonds
    Expects an autotst.reaction.Reaction type input"""

    allowed_families = ['Disproportionation', 'H_Abstraction']
    family = reaction.rmg_reaction.family
    assert family in allowed_families, 'HFSP opt only implemented for Disproportionation and H_Abstraction reactions'

    # d14 is the bond that will form: so 1-4 for Disproportionation, and 2-3 for H_Abstraction
    # d24 is the bond that will break: so 2-4 for Disproportionation, and 1-2 for H_Abstraction
    d14 = None
    d24 = None

    H_label = {
        'Disproportionation': '*4',
        'H_Abstraction': '*2',
    }
    H_connected_to = {
        'Disproportionation': '*2',
        'H_Abstraction': '*1',
    }
    H_not_yet_connected_to = {
        'Disproportionation': '*1',
        'H_Abstraction': '*3',
    }

    reactants = []
    products = []
    reactant_indices = [database_fun.get_unique_species_index(x) for x in reaction.rmg_reaction.reactants]
    product_indices = [database_fun.get_unique_species_index(x) for x in reaction.rmg_reaction.products]
    reactant_indices.sort()
    product_indices.sort()

    for species_index in reactant_indices + product_indices:

        species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
        rotor_dir = os.path.join(species_dir, 'rotors')
        gaussian_log_file = glob.glob(os.path.join(rotor_dir, 'conformer_*.log'))[0]
        with open(gaussian_log_file, 'r') as f:
            atoms = ase.io.gaussian.read_gaussian_out(f)

        rmg_species = database_fun.index2species(species_index)
        species_smiles = rmg_species.smiles

        # make a conformer object again
        new_cf = autotst.species.Conformer(smiles=species_smiles)  # TODO make this from adjacency list?
        new_cf._ase_molecule = atoms
        new_cf.update_coords_from(mol_type="ase")
        if species_index in reactant_indices:
            reactants.append(new_cf)
        else:
            products.append(new_cf)

    ref_library_path = os.path.join(rmgpy.settings['database.directory'], 'kinetics')
    kinetics_database = rmgpy.data.kinetics.KineticsDatabase()
    kinetics_database.load(
        ref_library_path,
        libraries=[],
        families=allowed_families,
    )
    labeled_r, labeled_p = kinetics_database.families[reaction.rmg_reaction.family].get_labeled_reactants_and_products(
        [x.rmg_molecule for x in reactants],
        [x.rmg_molecule for x in products],
        relabel_atoms=False
    )
    # reorder labeled_p according to species index to match the conformers we built
    if database_fun.get_unique_species_index(labeled_p[0]) > database_fun.get_unique_species_index(labeled_p[1]):
        labeled_p = [labeled_p[1], labeled_p[0]]
    if database_fun.get_unique_species_index(labeled_r[0]) > database_fun.get_unique_species_index(labeled_r[1]):
        labeled_r = [labeled_r[1], labeled_r[0]]

    # Get the 2-4 bond distance - H and what it's already connected to
    atom_labels = labeled_r[0].get_all_labeled_atoms()
    if H_connected_to[family] in labeled_r[0].get_all_labeled_atoms():
        print(atom_labels)
        H_connected_to_index = labeled_r[0].atoms.index(atom_labels[H_connected_to[family]])
        H_label_index = labeled_r[0].atoms.index(atom_labels[H_label[family]])
        d24 = reactants[0]._ase_molecule.get_distance(H_connected_to_index, H_label_index)
    else:
        atom_labels = labeled_r[1].get_all_labeled_atoms()
        print(atom_labels)
        H_connected_to_index = labeled_r[1].atoms.index(atom_labels[H_connected_to[family]])
        H_label_index = labeled_r[1].atoms.index(atom_labels[H_label[family]])
        d24 = reactants[1]._ase_molecule.get_distance(H_connected_to_index, H_label_index)

    # Get the 1-4 bond distance - H and what it will bond to
    atom_labels = labeled_p[0].get_all_labeled_atoms()
    if H_not_yet_connected_to[family] in atom_labels:
        print(atom_labels)
        H_not_yet_connected_to_index = labeled_p[0].atoms.index(atom_labels[H_not_yet_connected_to[family]])
        H_label_index = labeled_p[0].atoms.index(atom_labels[H_label[family]])
        d14 = products[0]._ase_molecule.get_distance(H_not_yet_connected_to_index, H_label_index)
    else:
        atom_labels = labeled_p[1].get_all_labeled_atoms()
        print(atom_labels)
        H_not_yet_connected_to_index = labeled_p[1].atoms.index(atom_labels[H_not_yet_connected_to[family]])
        H_label_index = labeled_p[1].atoms.index(atom_labels[H_label[family]])
        d14 = products[1]._ase_molecule.get_distance(H_not_yet_connected_to_index, H_label_index)

    return d14, d24


def get_connected(my_molecule, start_index):
    """Function to get the indices of all atoms connected to a particular atom
    Expects and rmg molecule object and the atom index"""
    connected = []

    def get_others(start_idx):
        bonds = my_molecule.get_bonds(my_molecule.atoms[start_idx])
        for key in bonds.keys():

            atom_index = my_molecule.atoms.index(key)
            if atom_index in connected:
                continue

            connected.append(atom_index)
            get_others(atom_index)

    get_others(start_index)
    return connected


def get_energy_forces_atom_bond(atoms, ind1, ind2, k, deq):
    forces = np.zeros(atoms.positions.shape)
    bd, d = ase.geometry.get_distances([atoms.positions[ind1]], [atoms.positions[ind2]], cell=atoms.cell, pbc=atoms.pbc)
    if d != 0.0:
        forces[ind1] = 2.0 * bd * (1.0 - deq / d)
        forces[ind2] = -forces[ind1]
    else:
        forces[ind1] = bd
        forces[ind2] = bd
    energy = k * (d - deq) ** 2
    return energy, k * forces


def get_energy_forces_site_bond(atoms, ind, site_pos, k, deq):
    forces = np.zeros(atoms.positions.shape)
    bd, d = ase.geometry.get_distances([atoms.positions[ind]], [site_pos], cell=atoms.cell, pbc=atoms.pbc)
    if d != 0:
        forces[ind] = 2.0 * bd * (1.0 - deq / d)
    else:
        forces[ind] = bd
    energy = k * (d - deq) ** 2
    return energy, k * forces


class HarmonicallyForcedXTB(xtb.ase.calculator.XTB):
    """Taken and modified from Matt Johnson's Pynta https://github.com/zadorlab/pynta"""
    def get_energy_forces(self):
        energy = 0.0
        forces = np.zeros(self.atoms.positions.shape)
        if hasattr(self.parameters, "atom_bond_potentials"):
            for atom_bond_potential in self.parameters.atom_bond_potentials:
                E, F = get_energy_forces_atom_bond(self.atoms, **atom_bond_potential)
                energy += E
                forces += F

        if hasattr(self.parameters, "site_bond_potentials"):
            for site_bond_potential in self.parameters.site_bond_potentials:
                E, F = get_energy_forces_site_bond(self.atoms, **site_bond_potential)
                energy += E
                forces += F
        return energy[0][0], forces

    def calculate(self, atoms=None, properties=None, system_changes=ase.calculators.calculator.all_changes):
        xtb.ase.calculator.XTB.calculate(self, atoms=atoms, properties=properties, system_changes=system_changes)
        energy, forces = self.get_energy_forces()
        self.results["energy"] += energy
        self.results["free_energy"] += energy
        self.results["forces"] += forces


def get_s(rmg_molecule, a1, a2):
    # returns string describing connectivity of the interacting atoms
    # a1 and a2 are indices

    # A0--(A1--A2)--A3
    A0 = ''
    bonds1 = rmg_molecule.get_bonds(rmg_molecule.atoms[a1])
    for key in bonds1.keys():
        if key != rmg_molecule.atoms[a2]:
            A0 = 'R'

    A3 = ''
    bonds2 = rmg_molecule.get_bonds(rmg_molecule.atoms[a2])
    for key in bonds2.keys():
        if key != rmg_molecule.atoms[a1]:
            A3 = 'R'
    return f'{A0}--(R--R)--{A3}'


def get_dk(dwell, s, dist, hydrogen_interaction):
    # dwell is the distance between breaking bonds (or forming)
    # for Disproportionation, that's 2-4 and (1-4)
    assert dist is None or dist == 2
    if s in ["--(R--R)--"]:  # nothing connected on either end
        if dist is not None:
            return dwell * 1.25, 100.0
        else:
            if hydrogen_interaction:
                return dwell * 1.6, 100.0
            else:
                return dwell * 1.4, 100.0
    elif s in ["R--(R--R)--", "--(R--R)--R"]:  # only one atom connected
        if dist is not None:
            return dwell * 1.25, 100.0
        else:
            if hydrogen_interaction:
                return dwell * 1.6, 100.0
            else:
                return dwell * 1.4, 100.0
    elif s in ["R--(R--R)--R"]:  # atoms connected on either side
        if dist is not None:
            return dwell * 1.25, 100.0
        else:
            if hydrogen_interaction:
                return dwell * 1.6, 100.0
            else:
                return dwell * 1.4, 100.0


def get_HFSP_TS_guess(reaction, d14, d24, conformer_index):
    """Function to get the positions for an HFSP guess
    Takes in an autotst.reaction.Reaction object and returns the ase molecule
    # right now this only works on the first conformer
    """
    direction = 'forward'  # TODO find out if there's a case where we'll ever use reverse

    allowed_families = ['Disproportionation', 'H_Abstraction']
    family = reaction.rmg_reaction.family
    assert family in allowed_families, 'HFSP opt only implemented for Disproportionation reactions'

    H_label = {
        'Disproportionation': '*4',
        'H_Abstraction': '*2'
    }
    H_connected_to = {
        'Disproportionation': '*2',
        'H_Abstraction': '*1'
    }
    H_not_yet_connected_to = {
        'Disproportionation': '*1',
        'H_Abstraction': '*3'
    }

    atom_labels = reaction.ts[direction][conformer_index].rmg_molecule.get_all_labeled_atoms()
    # for Disproportionation it's 2-4 breaks and 1-4 forms

    H_not_yet_connected_to_index = reaction.ts[direction][conformer_index].rmg_molecule.atoms.index(atom_labels[H_not_yet_connected_to[family]])
    H_connected_to_index = reaction.ts[direction][conformer_index].rmg_molecule.atoms.index(atom_labels[H_connected_to[family]])
    H_label_index = reaction.ts[direction][conformer_index].rmg_molecule.atoms.index(atom_labels[H_label[family]])

    hydrogen_interaction24 = reaction.ts[direction][conformer_index].rmg_molecule.atoms[H_connected_to_index].is_hydrogen() or \
        reaction.ts[direction][conformer_index].rmg_molecule.atoms[H_label_index].is_hydrogen

    hydrogen_interaction14 = reaction.ts[direction][conformer_index].rmg_molecule.atoms[H_not_yet_connected_to_index].is_hydrogen() or \
        reaction.ts[direction][conformer_index].rmg_molecule.atoms[H_label_index].is_hydrogen

    # construct the atom bond potentials:
    # For Disproportionation family: this will be between labeled atoms 4-1 and 4-2
    atom_bond_potentials = []
    site_bond_potentials = []

    # try re-optimizing with a large d_eq, see if anything changes
    deq1, k1 = get_dk(d24, get_s(reaction.ts[direction][conformer_index].rmg_molecule, H_connected_to_index, H_label_index), 2, hydrogen_interaction24)
    deq2, k2 = get_dk(d14, get_s(reaction.ts[direction][conformer_index].rmg_molecule, H_not_yet_connected_to_index, H_label_index), None, hydrogen_interaction14)
    atom_bond_potentials = [
        {"ind1": H_not_yet_connected_to_index, "ind2": H_label_index, "k": k1, "deq": deq1},
        {"ind1": H_label_index, "ind2": H_connected_to_index, "k": k2, "deq": deq2},
    ]

    # see if anything is bonded to *1, if so, add a soft repelling harmonic potential between it and *2
    bonds1 = reaction.ts[direction][conformer_index].rmg_molecule.get_bonds(reaction.ts[direction][conformer_index].rmg_molecule.atoms[H_not_yet_connected_to_index])
    if bonds1:
        for key in bonds1.keys():
            repel_index1 = reaction.ts[direction][conformer_index].rmg_molecule.atoms.index(key)
            repel_index2 = H_connected_to_index
            atom_bond_potentials.append({"ind1": repel_index1, "ind2": repel_index2, "k": 0.1, "deq": 7})
            break
    # ------------------ Set up the HFSP run --------------------------
    hfxtb = HarmonicallyForcedXTB(
        method="GFN1-xTB",
        atom_bond_potentials=atom_bond_potentials,
        site_bond_potentials=site_bond_potentials
    )

    r1_indices = get_connected(reaction.ts[direction][conformer_index].rmg_molecule, reaction.ts[direction][conformer_index].rmg_molecule.atoms.index(atom_labels[H_label[family]]))
    r2_indices = get_connected(reaction.ts[direction][conformer_index].rmg_molecule, reaction.ts[direction][conformer_index].rmg_molecule.atoms.index(atom_labels[H_not_yet_connected_to[family]]))

    bond_labels = []
    for bond in reaction.ts[direction][conformer_index].get_bonds()[:-1]:
        if (bond.atom_indices[0] in r1_indices and bond.atom_indices[1] in r2_indices) or \
                (bond.atom_indices[1] in r1_indices and bond.atom_indices[0] in r2_indices):
            # print('Overdefined', bond.atom_indices, 'skipping bond...')
            continue
        bond_labels.append(bond.atom_indices)

    # make sure none of the atoms are bonded to something they shouldn't be
    for label in bond_labels:
        assert label[1] in get_connected(reaction.ts[direction][conformer_index].rmg_molecule, label[0])

    c_bond = ase.constraints.FixBondLengths(bond_labels)
    reaction.ts[direction][conformer_index].ase_molecule.set_constraint(c_bond)
    reaction.ts[direction][conformer_index].ase_molecule.calc = hfxtb

    opt = ase.optimize.BFGS(reaction.ts[direction][conformer_index].ase_molecule, logfile=None)
    opt.run(fmax=0.02, steps=1500)
    return opt.atoms


def verify_bond_count(reaction_index, gaussian_file=None):
    # function to count the number of each kind of bond to compare RMG's description to the optimized result coming out of Gaussian
    reaction_log(reaction_index, f'Verifying bond counts for reaction {reaction_index}')

    def get_type_bonds(ref_bond_str, autotst_ts):
        bond_list = autotst_ts.get_bonds()
        bonds_of_type = []
        for i in range(len(bond_list)):
            atoms = autotst_ts.ase_molecule[bond_list[i].atom_indices]
            symbols = [a.symbol for a in atoms]
            symbols.sort()
            bond_str = ''.join(symbols)
            if bond_str == ref_bond_str:
                bonds_of_type.append(bond_list[i].atom_indices)
        return bonds_of_type

    rmg_reaction = database_fun.index2reaction(reaction_index)
    reaction = autotst.reaction.Reaction(rmg_reaction=rmg_reaction)
    reaction.get_labeled_reaction()
    reaction.get_label()
    reaction.ts['forward'][0].get_molecules()

    # default is to use whatever gaussian TS file got copied into the arkane directory
    if not gaussian_file:
        gaussian_file = glob.glob(os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}', 'arkane', 'fwd_*.log'))[0]

    with open(gaussian_file, 'r') as f:
        atoms = ase.io.gaussian.read_gaussian_out(f)

    match = True
    autotst_bonds = reaction.ts['forward'][0].get_bonds()
    analysis = ase.geometry.analysis.Analysis(atoms)
    bond_types = [
        'CC',
        'CO',
        'CH',
        'OO',
        'HO',
        'HH',
    ]

    for b in range(len(bond_types)):
        reaction_log(reaction_index, f'Comparing {bond_types[b][0]}-{bond_types[b][1]} bonds:')
        gaussian_bonds = analysis.get_bonds(bond_types[b][0], bond_types[b][1], unique=True)
        reaction_log(reaction_index, gaussian_bonds[0])
        
        rmg_bonds = get_type_bonds(bond_types[b], reaction.ts['forward'][0])
        reaction_log(reaction_index, rmg_bonds)

        if len(rmg_bonds) != len(gaussian_bonds[0]):
            reaction_log(reaction_index, 'WARNING: RMG and ASE disagree with number of bonds')
            match = False

    return match


if __name__ == '__main__':
    # for idx in [419, 1814, 1287, 748, 370, 1103, 371]:
    for idx in [1288]:
        setup_opt(idx, 'center')
        run_opt(idx, 'center')

    exit(0)
    top_reactions = [
        915, 749, 324, 419, 1814, 1287, 748, 1288, 370, 1103,
        371, 213, 420, 581, 464, 1289, 720, 722, 1658, 574, 725, 1736,
        418, 1290, 1721, 1665, 1685, 427, 1714, 1766, 655, 1773, 1003, 650,
        985, 918, 585, 692, 1532, 1326, 1578, 1428, 916, 595, 693, 1242
    ]

    if len(sys.argv) > 1:
        reaction_index = int(sys.argv[1])
        screen_reaction_ts(reaction_index)
    else:
        for rxn in top_reactions:
            # 324 has errors, 915 and 749 are just currently running
            if rxn in [915, 749, 324]:
                continue
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
