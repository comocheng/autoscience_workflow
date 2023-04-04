import os
import sys
import glob
import shutil
# import arkane
import arkane.ess.gaussian

import ase.io.gaussian
import rmgpy.chemkin
import autotst.species


DFT_DIR = '/home/moon/autoscience/reaction_calculator/dft'
DFT_DIR = '/work/westgroup/harris.se/autoscience/reaction_calculator/dft'
sys.path.append(DFT_DIR)
import thermokinetic_fun


def arkane_species_complete(species_index):
    """Function to check whether the arkane job is complete for a species
    Expects to find the following directory structure:
    DFT_DIR/thermo/species_XXXX/arkane/RMG_libraries/thermo.py
    Returns True if complete, False otherwise
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    arkane_result = os.path.join(species_dir, 'arkane', 'RMG_libraries', 'thermo.py')
    return os.path.exists(arkane_result)


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
    # species_log(species_index, f'Setting up Arkane species')
    if arkane_species_complete(species_index):
        # species_log(species_index, f'Arkane species already complete')
        return True

    species_smiles = thermokinetic_fun.species_index2smiles(species_index)
    # make a conformer object from the SMILES
    new_cf = autotst.species.Conformer(smiles=species_smiles)
    # read the conformer geometry from the file
    conformer_file = thermokinetic_fun.get_lowest_energy_gaussian_file(conformer_dir)

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
    thermokinetic_fun.write_arkane_conformer_file(new_cf, conformer_file, arkane_dir, include_rotors=include_rotors)

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


def setup_arkane_reaction(reaction_index, direction='forward', force_valid_ts=False):
    """Function to setup the arkane job for a reaction
    """
    # check if the arkane job was already completed
    if thermokinetic_fun.arkane_reaction_complete(reaction_index):
        thermokinetic_fun.reaction_log(reaction_index, 'Arkane job already ran')
        return True

    reaction_smiles = thermokinetic_fun.reaction_index2smiles(reaction_index)
    thermokinetic_fun.reaction_log(reaction_index, f'starting setup_arkane_reaction for reaction {reaction_index} {reaction_smiles}')

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    overall_dir = os.path.join(reaction_dir, 'overall')
    arkane_dir = os.path.join(reaction_dir, 'arkane')
    os.makedirs(arkane_dir, exist_ok=True)

    species_dict_file = "/work/westgroup/harris.se/autoscience/autoscience/butane/models/rmg_model/species_dictionary.txt"
    species_dict = rmgpy.chemkin.load_species_dictionary(species_dict_file)

    def get_sp_name(smiles):
        if smiles == '[CH2]C=CC':  # manually change to resonance structures included in model
            smiles = 'C=C[CH]C'
        elif smiles == '[CH2][CH]C=C':
            smiles = '[CH2]C=C[CH2]'
        for entry in species_dict.keys():
            if species_dict[entry].smiles == smiles:
                return str(species_dict[entry])
        # need to look for isomorphism
        print(f'Failed to get species name for {smiles}')
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
    reaction_smiles = thermokinetic_fun.reaction_index2smiles(reaction_index)
    reaction = autotst.reaction.Reaction(label=reaction_smiles)
    thermokinetic_fun.reaction_log(reaction_index, f'Creating arkane files for reaction {reaction_index} {reaction.label}')
    reaction.ts[direction][0].get_molecules()

    # pick the lowest energy valid transition state:
    TS_logs = glob.glob(os.path.join(overall_dir, f'ase_*.log'))
    TS_log = ''
    lowest_energy = 1e5
    for logfile in TS_logs:
        # skip if the TS is not valid
        if not force_valid_ts:
            pass  # TODO check if the TS is valid
            # if not check_vib_irc(reaction_index, logfile):
            #     continue

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

        species_smiles = reactant.smiles
        if species_smiles == '[CH2]C=CC':  # TODO clean up this fix where we manually switch back to other resonance structure
            species_smiles = 'C=C[CH]C'
        elif species_smiles == '[CH2][CH]C=C':
            species_smiles = '[CH2]C=C[CH2]'
        species_name = get_sp_name(species_smiles)
        species_index = thermokinetic_fun.species_smiles2index(species_smiles)
        species_arkane_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'arkane')
        try:
            species_file = os.path.join(f'species_{species_index:04}', os.path.basename(glob.glob(os.path.join(species_arkane_dir, 'conformer_*.py'))[0]))
        except IndexError:
            raise IndexError(f'No species conformer file found in {species_arkane_dir}')        

        try:
            shutil.copytree(species_arkane_dir, os.path.join(arkane_dir, f'species_{species_index:04}'))
        except FileExistsError:
            pass

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

    thermokinetic_fun.reaction_log(reaction_index, f'finished setting up arkane for reaction {reaction_index} {reaction_label}')
    # set_reaction_status(reaction_index, 'arkane_setup', True)


reaction_index = int(sys.argv[1])
setup_arkane_reaction(reaction_index)


