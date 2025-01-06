import os
import numpy as np
import sys
import glob
import autotst.species
import ase.atoms

import xtb.ase.calculator
import ase.calculators.gaussian


DFT_DIR = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'dft')
sys.path.append(DFT_DIR)
sys.path.append(os.environ['DATABASE_DIR'])
import autotst_wrapper
import database_fun


# Make the species
reaction_index = int(sys.argv[1])
rotor_index = int(sys.argv[2])
angle_index = int(sys.argv[3])
autotst_wrapper.reaction_log(reaction_index, f'Running fixed rotor scan for reaction {reaction_index}, rotor {rotor_index}, angle_index {angle_index}')


force_rerun = True
reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:06}')
overall_dir = os.path.join(reaction_dir, 'overall')
rigid_rotor_dir = os.path.join(reaction_dir, 'rigid_rotors')
os.makedirs(rigid_rotor_dir, exist_ok=True)

rotor_str = 'rotor'

# check if the rotors were already set up
rotor_logfiles = glob.glob(os.path.join(rigid_rotor_dir, f'{rotor_str}_*.com'))
if force_rerun:
    autotst_wrapper.reaction_log(reaction_index, 'forcing rerun of ts rotors')
else:
    if rotor_logfiles:
        autotst_wrapper.reaction_log(reaction_index, 'TS rotors already set up')
        raise ValueError
autotst_wrapper.reaction_log(reaction_index, f'Starting TS rotor setup')

# # ------------------ Use Hotbit to screen the conformers ------------------
# Build the reaction TS complex
autotst_wrapper.reaction_log(reaction_index, f'Building TS complex')
direction = 'forward'
rmg_reaction = database_fun.index2reaction(reaction_index)
reaction_smiles = database_fun.reaction_index2smiles(reaction_index)
reaction = autotst.reaction.Reaction(label=reaction_smiles)  # going back to this even though it's not dependable

# Get the lowest energy conformer from the overall result -- look in the arkane folder
autotst_wrapper.reaction_log(reaction_index, f'Loading TS geometry from gaussian log file')
starting_geometry_file = autotst_wrapper.get_lowest_energy_gaussian_file(overall_dir)
if not os.path.exists(starting_geometry_file) or autotst_wrapper.get_termination_status(starting_geometry_file) != 0:
    raise OSError('Could not find TS geometry file')
reaction.ts[direction][0]._ase_molecule = autotst_wrapper.get_gaussian_file_geometry(starting_geometry_file)
reaction.ts[direction][0].update_coords_from(mol_type="ase")

# get the rotors
torsions = reaction.ts[direction][0].get_torsions()
n_rotors = len(torsions)
if n_rotors == 0:
    no_rotor_file = os.path.join(rigid_rotor_dir, 'NO_ROTORS.txt')
    with open(no_rotor_file, 'w') as f:
        f.write('NO ROTORS')
    print(reaction_index, "no rotors to calculate")
    raise ValueError

new_cf = reaction.ts[direction][0]

os.chdir(rigid_rotor_dir)

if rotor_index >= n_rotors:
    raise ValueError('Rotor index is higher than number of rotors')

atoms = new_cf.get_ase_mol()
angles = np.linspace(0, 360, 21)
energies = np.zeros(len(angles))


atoms.set_dihedral(
    new_cf.torsions[rotor_index].atom_indices[0],
    new_cf.torsions[rotor_index].atom_indices[1],
    new_cf.torsions[rotor_index].atom_indices[2],
    new_cf.torsions[rotor_index].atom_indices[3],
    angles[angle_index],
    mask=new_cf.torsions[rotor_index].mask
)
# atoms.calc = xtb.ase.calculator.XTB(method="GFN2-xTB")

atoms.calc = ase.calculators.gaussian.Gaussian(
    label=f'rotor_{rotor_index:04}_{angle_index:04}',
    method='m062x',
    basis='cc-pVTZ',
    scf='maxcycle=100',
    mult=new_cf.rmg_molecule.multiplicity
)

energy = atoms.get_potential_energy()
print(energy)
