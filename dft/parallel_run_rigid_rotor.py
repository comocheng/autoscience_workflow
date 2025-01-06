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
species_index = int(sys.argv[1])
rotor_index = int(sys.argv[2])
angle_index = int(sys.argv[3])
print(f'Running fixed rotor scan for species {species_index}, rotor {rotor_index}, angle_index {angle_index}')

species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
conformer_dir = os.path.join(species_dir, 'conformers')
rotor_dir = os.path.join(species_dir, 'rotors')
rigid_rotor_dir = os.path.join(species_dir, 'rigid_rotors')
os.makedirs(rotor_dir, exist_ok=True)
os.makedirs(rigid_rotor_dir, exist_ok=True)

rmg_species = database_fun.index2species(species_index)
species_smiles = rmg_species.smiles

valid_conformer = False
conformer_blacklist = []
while not valid_conformer:
    conformer_file = autotst_wrapper.get_lowest_energy_gaussian_file(conformer_dir, blacklist=conformer_blacklist)
    if not conformer_file:
        species_log(species_index, f'Failed to find lowest energy gaussian file in {conformer_dir}')
        species_log(species_index, f'Conformer blacklist is {conformer_blacklist}')

    if autotst_wrapper.bonds_too_large(conformer_file, species_index):
        conformer_blacklist.append(conformer_file)
        species_log(species_index, f'Bonds too large for conformer {conformer_file}, blacklisting...')
    else:
        valid_conformer = True
        print(species_index, f'Lowest energy conformer is {conformer_file}')

    if len(conformer_blacklist) >= len(glob.glob(os.path.join(conformer_dir, 'conformer_*.log'))):
        print(species_index, f'No valid conformers found. Quitting...')
        raise ValueError

new_conformer_loc = os.path.join(rotor_dir, os.path.basename(conformer_file))
# get the rotors
with open(new_conformer_loc, 'r') as f:
    atoms = ase.io.gaussian.read_gaussian_out(f)

smiles = database_fun.index2species(species_index).smiles
new_cf = autotst.species.Conformer(smiles=smiles)  # TODO make this from adjacency list?
new_cf._ase_molecule = atoms
new_cf.update_coords_from(mol_type="ase")
torsions = new_cf.get_torsions()  # TODO - is this only the nonterminal ones?
n_rotors = len(torsions)

rotor_str = 'rotor'


os.chdir(rigid_rotor_dir)

if rotor_index >= n_rotors:
    raise ValueError('Rotor index is higher than number of rotors')

atoms = new_cf.get_ase_mol()
angles = np.linspace(0, 360, 21)
energies = np.zeros(len(angles))


atoms.rotate_dihedral(
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
