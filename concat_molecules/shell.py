#!/usr/bin/env python
# coding: utf-8

# In[160]:


import os
import numpy as np
import glob
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


family = 'Disproportionation'
# get reaction index from user
reaction_index = int(sys.argv[1])
reaction_smiles = thermokinetic_fun.reaction_index2smiles(reaction_index)
reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
shell_dir = os.path.join(reaction_dir, 'shell')

reaction = autotst.reaction.Reaction(label=reaction_smiles)
reaction.ts['forward'][0].get_molecules()

# confirm we're working with Disproportionation, otherwise this won't work
assert reaction.reaction_family == family


# load the constituent species
r0 = reaction.rmg_reaction.reactants[0]
r1 = reaction.rmg_reaction.reactants[1]
r0_index = thermokinetic_fun.species_smiles2index(r0.smiles)
r1_index = thermokinetic_fun.species_smiles2index(r1.smiles)

# ## Get the labels on the reactants
# load the Disproportionation family
thermo_libs = [
    # 'BurkeH2O2',
    'primaryThermoLibrary',
    # 'FFCM1(-)',
    # 'CurranPentane',
    # 'Klippenstein_Glarborg2016',
    # 'thermo_DFT_CCSDTF12_BAC',
    # 'DFT_QCI_thermo',
    # 'CBS_QB3_1dHR',
]

thermo_library_path = os.path.join(rmgpy.settings['database.directory'], 'thermo')
thermo_database = rmgpy.data.thermo.ThermoDatabase()
thermo_database.load(
    thermo_library_path,
    libraries=thermo_libs
)

kinetic_libs = [
    # 'FFCM1(-)',
    # 'CurranPentane',
    # 'combustion_core/version5',
    # 'Klippenstein_Glarborg2016',
    # 'BurkeH2O2inArHe',
    # 'BurkeH2O2inN2',
]

# load the families
ref_library_path = os.path.join(rmgpy.settings['database.directory'], 'kinetics')
kinetics_database = rmgpy.data.kinetics.KineticsDatabase()
kinetics_database.load(
    ref_library_path,
    libraries=kinetic_libs,
    families=[family]
)

# load the entire database - I think this step tends to fail on discovery. Might have to generate com files on my laptop
ref_db = rmgpy.data.rmg.RMGDatabase()
ref_db.kinetics = kinetics_database
ref_db.thermo = thermo_database

# templates = ref_db.kinetics.families[family].generate_reactions([r0.molecule[0], r1.molecule[0]], relabel_atoms=True)
labeled_r, labeled_p = ref_db.kinetics.families[family].get_labeled_reactants_and_products(
    [r0.molecule[0], r1.molecule[0]],
    [reaction.rmg_reaction.products[0].molecule[0], reaction.rmg_reaction.products[1].molecule[0]],
    relabel_atoms=True
)

# # rename to make sure molecule 0 has labels *2,*3,*4 and molecule 1 has *1
# if not labeled_r[0].is_isomorphic(r0.molecule[0]):
#     print('wrong order, rearranging')
#     temp0 = labeled_r[0]
#     temp1 = labeled_r[1]
#     labeled_r[0] = temp1
#     labeled_r[1] = temp0
# ## rename to make sure molecule 0 has labels *2,*3,*4 and molecule 1 has *1
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


# load the logfiles and get geometries
r0_log = glob.glob(os.path.join(DFT_DIR, 'thermo', f'species_{r0_index:04}', 'arkane', 'conformer*.log'))[0]
r1_log = glob.glob(os.path.join(DFT_DIR, 'thermo', f'species_{r1_index:04}', 'arkane', 'conformer*.log'))[0]
with open(r0_log, 'r') as f:
    r0_atoms = ase.io.gaussian.read_gaussian_out(f)
with open(r1_log, 'r') as f:
    r1_atoms = ase.io.gaussian.read_gaussian_out(f)

atom_1_index = labeled_r[1].get_labeled_atoms('*1')[0].sorting_label
atom_2_index = labeled_r[0].get_labeled_atoms('*2')[0].sorting_label
atom_3_index = labeled_r[0].get_labeled_atoms('*3')[0].sorting_label
atom_4_index = labeled_r[0].get_labeled_atoms('*4')[0].sorting_label

# print('*1\t', atom_1_index, r1_atoms[atom_1_index])
# print('*2\t', atom_2_index, r0_atoms[atom_2_index])
# print('*4\t', atom_4_index, r0_atoms[atom_4_index])

reaction_core = ase.atoms.Atoms([r1_atoms[atom_1_index], r0_atoms[atom_2_index], r0_atoms[atom_4_index]])

# keep molecule 0 in place
my_ts = r0_atoms


# make a ray to extend from labeled atom *2 to *4
# reload geometry fresh each time
with open(r0_log, 'r') as f:
    r0_atoms = ase.io.gaussian.read_gaussian_out(f)
with open(r1_log, 'r') as f:
    r1_atoms = ase.io.gaussian.read_gaussian_out(f)
ray = r0_atoms[atom_4_index].position - r0_atoms[atom_2_index].position
ray /= np.linalg.norm(ray)  # normalize

# move the Hydrogen (*4) to be d23 away from the other atom (*2)
# d23 represents labels *2 - *4 from Disproportionation
H_distance_2_4 = reaction.ts['forward'][0].distance_data.distances['d23']
H_position = r0_atoms[atom_2_index].position + H_distance_2_4 * ray
r0_atoms[atom_4_index].position = H_position

# translate molecule 1's (*1) to be d12 from the H(*4) on molecule 0
d14 = reaction.ts['forward'][0].distance_data.distances['d12']
a1_new_position = H_position + d14 * ray
translation = a1_new_position - r1_atoms[atom_1_index].position
r1_atoms.translate(translation)

# use law of cosines to get angle of rotation required to match distance data
a = H_distance_2_4
b = reaction.ts['forward'][0].distance_data.distances['d13']
c = d14
assert b > a
assert b > c
angle_rad = np.arccos((c * c - a * a - b * b) / (-2 * a * b))
angle_deg = angle_rad * 180 / np.pi

# rotate the entire molecule ~5 degrees
# vector is arbitrary, but we can try experimenting with this to see what gets best results
r1_atoms.rotate(angle_deg, v='x', center=r0_atoms[atom_4_index].position)

ase.io.write(os.path.join(shell_dir, 'm0.xyz'), r0_atoms)
ase.io.write(os.path.join(shell_dir, 'm1.xyz'), r1_atoms)

# now rotate in 5 degree increments
angles = np.arange(0, 360, 5)
energies = np.zeros(len(angles))
lowest_energy = 1e5
lowest_index = -1
for i in range(0, len(angles)):
    m0 = ase.io.read(os.path.join(shell_dir, 'm0.xyz'))
    m1 = ase.io.read(os.path.join(shell_dir, 'm1.xyz'))

    m1.rotate(angles[i], v=ray, center=H_position)
    total = m0 + m1
    total.calc = ase.calculators.lj.LennardJones()
    energies[i] = total.get_potential_energy()
    if energies[i] < lowest_energy:
        lowest_energy = energies[i]
        lowest_index = i

m0 = ase.io.read(os.path.join(shell_dir, 'm0.xyz'))
m1 = ase.io.read(os.path.join(shell_dir, 'm1.xyz'))

m1.rotate(angles[lowest_index], v=ray, center=H_position)
ts_guess = m0 + m1
ase.io.write(os.path.join(shell_dir, 'ts_guess.xyz'), ts_guess)

# 1, 2, and 4 are the main reactants but 3 should be kept nearby?
ind1 = len(m0) + atom_1_index
ind2 = atom_2_index
ind4 = atom_4_index

combos = f"{(ind1 + 1)} {(ind2 + 1)} F\n"
combos += f"{(ind2 + 1)} {(ind4 + 1)} F\n"
combos += f"{(ind1 + 1)} {(ind2 + 1)} {(ind4 + 1)} F"

# write the gaussian job
ase_gaussian = ase.calculators.gaussian.Gaussian(
    mem='5GB',
    nprocshared=24,
    label='ase_systematic',
    scratch='.',
    method="m062x",
    basis="cc-pVTZ",
    extra="Opt=(ModRedun,Loose,maxcycles=900) Int(Grid=SG1) scf=(maxcycle=900)",
    multiplicity=reaction.ts['forward'][0].rmg_molecule.multiplicity,
    addsec=[combos]
)

ase_gaussian.label = 'ase_systematic'
ase_gaussian.directory = shell_dir
ase_gaussian.parameters.pop('scratch')
ase_gaussian.parameters.pop('multiplicity')
ase_gaussian.parameters['mult'] = reaction.ts['forward'][0].rmg_molecule.multiplicity
ase_gaussian.write_input(ts_guess)

# Get rid of double-space between xyz block and mod-redundant section
thermokinetic_fun.delete_double_spaces(os.path.join(shell_dir, 'ase_systematic.com'))

shell_slurm_file = os.path.join(shell_dir, 'run_shell.sh')
lines = []
lines.append('#!/bin/bash')
lines.append(f'#SBATCH --job-name=concat_{reaction_index}')
lines.append('#SBATCH --error=error.log')
lines.append('#SBATCH --nodes=1')
lines.append('#SBATCH --partition=short')
lines.append('#SBATCH --mem=20Gb')
lines.append('#SBATCH --time=24:00:00')
lines.append('#SBATCH --cpus-per-task=32')
lines.append('\n')
lines.append('export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch')
lines.append('mkdir -p $GAUSS_SCRDIR')
lines.append('module load gaussian/g16')
lines.append('source /shared/centos7/gaussian/g16/bsd/g16.profile')
lines.append('\n')
lines.append('g16 ase_systematic.com')

with open(shell_slurm_file, 'w') as f:
    f.writelines(lines)
