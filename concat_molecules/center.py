#!/usr/bin/env python
# coding: utf-8

import os
import itertools
import rmgpy.chemkin
import rmgpy.species
import rmgpy.reaction
import rmgpy.data.kinetics

import autotst.species
import autotst.reaction
import ase.calculators.gaussian
import ase.calculators.lj
import autotst.conformer.systematic

import ase.atoms
import ase.io.gaussian


import sys
DFT_DIR = '/home/moon/autoscience/reaction_calculator/dft'
DFT_DIR = '/work/westgroup/harris.se/autoscience/reaction_calculator/dft'
sys.path.append(DFT_DIR)
import thermokinetic_fun


# get reaction index from user
reaction_index = int(sys.argv[1])
reaction_smiles = thermokinetic_fun.reaction_index2smiles(reaction_index)
reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
shell_dir = os.path.join(reaction_dir, 'shell')
center_dir = os.path.join(reaction_dir, 'center')
os.makedirs(center_dir, exist_ok=True)

reaction = autotst.reaction.Reaction(label=reaction_smiles)
reaction.ts['forward'][0].get_molecules()

# confirm we're working with Disproportionation, otherwise this won't work
assert reaction.reaction_family in ['Disproportionation', 'H_Abstraction']
family = reaction.reaction_family


# load the constituent species
r0 = reaction.rmg_reaction.reactants[0]
r1 = reaction.rmg_reaction.reactants[1]
r0_index = thermokinetic_fun.species_smiles2index(r0.smiles)
r1_index = thermokinetic_fun.species_smiles2index(r1.smiles)

# ## Get the labels on the reactants
# load the Disproportionation family
thermo_library_path = os.path.join(rmgpy.settings['database.directory'], 'thermo')
thermo_database = rmgpy.data.thermo.ThermoDatabase()
thermo_database.load(
    thermo_library_path,
    libraries=['primaryThermoLibrary'],
)

# load the families
ref_library_path = os.path.join(rmgpy.settings['database.directory'], 'kinetics')
kinetics_database = rmgpy.data.kinetics.KineticsDatabase()
kinetics_database.load(
    ref_library_path,
    libraries=[],
    families=[family]
)

# load the entire database - I think this step tends to fail on discovery. Might have to generate com files on my laptop
ref_db = rmgpy.data.rmg.RMGDatabase()
ref_db.kinetics = kinetics_database
ref_db.thermo = thermo_database

# templates = ref_db.kinetics.families[family].generate_reactions([r0.molecule[0], r1.molecule[0]], relabel_atoms=True)
# templates = ref_db.kinetics.families[family].generate_reactions([r0.molecule[0], r1.molecule[0]], relabel_atoms=True)
try:
    labeled_r, labeled_p = ref_db.kinetics.families[family].get_labeled_reactants_and_products(
        [r0.molecule[0], r1.molecule[0]],
        [reaction.rmg_reaction.products[0].molecule[0], reaction.rmg_reaction.products[1].molecule[0]],
        relabel_atoms=True
    )
except AttributeError:
    labeled_r, labeled_p = ref_db.kinetics.families[family].get_labeled_reactants_and_products(
        [r0, r1],
        [reaction.rmg_reaction.products[0], reaction.rmg_reaction.products[1]],
        relabel_atoms=True
    )

#labeled_r, labeled_p = ref_db.kinetics.families[family].get_labeled_reactants_and_products(
#    [r0.molecule[0], r1.molecule[0]],
#    [reaction.rmg_reaction.products[0].molecule[0], reaction.rmg_reaction.products[1].molecule[0]],
#    relabel_atoms=True
#)

if family == 'Disproportionation':
    # Make sure *2 *3 and *4 are on labeled_r[0] and *3 is on labeled_r[1]
    try:
        labeled_r[1].get_labeled_atoms('*1')
    except ValueError:
        print('wrong order, rearranging')
        temp0 = labeled_r[0]
        temp1 = labeled_r[1]
        labeled_r[0] = temp1
        labeled_r[1] = temp0

        temp_index0 = r0_index
        temp_index1 = r1_index
        r0_index = temp_index1
        r1_index = temp_index0
        # TODO also switch out the rmg species objects...
elif family == 'H_Abstraction':
    # Make sure *1 and *2 are on labeled_r[0] and *3 is on labeled_r[1]
    try:
        labeled_r[0].get_labeled_atoms('*1')
    except ValueError:
        print('wrong order, rearranging')
        temp0 = labeled_r[0]
        temp1 = labeled_r[1]
        labeled_r[0] = temp1
        labeled_r[1] = temp0

        temp_index0 = r0_index
        temp_index1 = r1_index
        r0_index = temp_index1
        r1_index = temp_index0
        # TODO also switch out the rmg species objects...
else:
    raise ValueError(f'family {family} not supported')

N = 10
for k in range(N):
    # load the geometries from the shell runs
    shell_run = os.path.join(shell_dir, f'ase_systematic_{k:04}.log')
    if not os.path.exists(shell_run):
        print('no shell run found')
        exit(1)
    with open(shell_run, 'r') as f:
        ts_guess = ase.io.gaussian.read_gaussian_out(f)

    if family == 'Disproportionation':
        atom_1_index = labeled_r[1].get_labeled_atoms('*1')[0].sorting_label  # H_notR group - steals H
        atom_2_index = labeled_r[0].get_labeled_atoms('*2')[0].sorting_label  # H_R group
        atom_3_index = labeled_r[0].get_labeled_atoms('*3')[0].sorting_label
        atom_4_index = labeled_r[0].get_labeled_atoms('*4')[0].sorting_label  # H atom

        H_atom_index = atom_4_index
        H_R_index = atom_2_index
        H_notR_index = atom_1_index

        H_distance_R = reaction.ts['forward'][0].distance_data.distances['d23']
        d_new_bond = reaction.ts['forward'][0].distance_data.distances['d12']

    elif family == 'H_Abstraction':
        atom_1_index = labeled_r[0].get_labeled_atoms('*1')[0].sorting_label  # H_R group
        atom_2_index = labeled_r[0].get_labeled_atoms('*2')[0].sorting_label  # H atom
        atom_3_index = labeled_r[1].get_labeled_atoms('*3')[0].sorting_label  # H_notR group - steals H

        H_atom_index = atom_2_index
        H_R_index = atom_1_index
        H_notR_index = atom_3_index

        H_distance_R = reaction.ts['forward'][0].distance_data.distances['d12']
        d_new_bond = reaction.ts['forward'][0].distance_data.distances['d23']
    else:
        raise NotImplementedError(f'family {family} not supported')

    # 1, 2, and 4 are the main reactants but 3 should be kept nearby?
    ind1 = len(labeled_r[0].atoms) + H_notR_index
    ind2 = H_R_index
    ind4 = H_atom_index

    indicies = []
    for i in range(0, len(ts_guess)):
        if i not in [ind1, ind2, ind4]:
            indicies.append(i)

    addsec = ""
    for combo in list(itertools.combinations(indicies, 2)):
        a, b = combo
        addsec += f"{(a + 1)} {(b + 1)} F\n"

    reaction.ts['forward'][0].rmg_molecule.update_multiplicity()

    # write the gaussian center job
    ase_gaussian = ase.calculators.gaussian.Gaussian(
        mem='5GB',
        nprocshared=24,
        label=f'ase_systematic_{k:04}',
        scratch='.',
        method="m062x",
        basis="cc-pVTZ",
        extra="Opt=(ts,calcfc,noeigentest,ModRedun,maxcycles=900) scf=(maxcycle=900)",
        multiplicity=reaction.ts['forward'][0].rmg_molecule.multiplicity,
        addsec=[addsec[:-1]]
    )

    ase_gaussian.label = f'ase_systematic_{k:04}'
    ase_gaussian.directory = center_dir
    ase_gaussian.parameters.pop('scratch')
    ase_gaussian.parameters.pop('multiplicity')
    ase_gaussian.parameters['mult'] = reaction.ts['forward'][0].rmg_molecule.multiplicity
    ase_gaussian.write_input(ts_guess)

    # Get rid of double-space between xyz block and mod-redundant section
    thermokinetic_fun.delete_double_spaces(os.path.join(center_dir, f'ase_systematic_{k:04}.com'))

center_slurm_file = os.path.join(center_dir, 'run_center.sh')
lines = []
lines.append('#!/bin/bash\n')
lines.append(f'#SBATCH --job-name=concat_center_{reaction_index}' + '\n')
lines.append('#SBATCH --error=error.log\n')
lines.append('#SBATCH --nodes=1\n')
lines.append('#SBATCH --partition=short\n')
lines.append('#SBATCH --mem=20Gb\n')
lines.append('#SBATCH --time=24:00:00\n')
lines.append('#SBATCH --cpus-per-task=32\n')
lines.append(f'#SBATCH --array=0-{N}\n')
lines.append('\n\n')
lines.append('export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch\n')
lines.append('mkdir -p $GAUSS_SCRDIR\n')
lines.append('module load gaussian/g16\n')
lines.append('source /shared/centos7/gaussian/g16/bsd/g16.profile\n')
lines.append('\n\n')
lines.append('RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))\n')
lines.append('fname="ase_systematic_${RUN_i}.com"\n\n')
lines.append('g16 $fname\n')

with open(center_slurm_file, 'w') as f:
    f.writelines(lines)
