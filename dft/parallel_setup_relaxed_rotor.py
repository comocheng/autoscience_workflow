import os
import copy
import numpy as np
import sys
import glob
import autotst.species
import ase.atoms

import ase.calculators.gaussian


DFT_DIR = os.path.join(os.environ['AUTOSCIENCE_REPO'], 'dft')
sys.path.append(DFT_DIR)
sys.path.append(os.environ['DATABASE_DIR'])
import autotst_wrapper
import database_fun
import zmatrix_ase
import ase.io.gaussian
from simtk import unit


ENVIRONMENT = 'explorer'

# Make the species
species_index = int(sys.argv[1])
print(f'Running relaxed rotor scan for species {species_index}')

species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
conformer_dir = os.path.join(species_dir, 'conformers')
rotor_dir = os.path.join(species_dir, 'rotors')
relaxed_rotor_dir = os.path.join(species_dir, 'relaxed_rotors')
os.makedirs(rotor_dir, exist_ok=True)
os.makedirs(relaxed_rotor_dir, exist_ok=True)

rmg_species = database_fun.index2species(species_index)
smiles = rmg_species.smiles

conformer_file = autotst_wrapper.get_lowest_valid_conformer(conformer_dir, species_index)

new_cf = autotst.species.Conformer(smiles=smiles)

# fill in the atom coordinates
with open(conformer_file, 'r') as f:
    atoms = ase.io.gaussian.read_gaussian_out(f)
    if autotst_wrapper.bonds_too_large(None, species_index, atoms=atoms):
        raise ValueError('Bonds too large')
new_cf._ase_molecule = atoms
new_cf.update_coords_from(mol_type="ase")
torsions = new_cf.get_torsions() 
n_rotors = len(torsions)

rotor_str = 'rotor'
os.chdir(relaxed_rotor_dir)


scan_angles = np.linspace(0, 360, 21)
start_atoms = copy.deepcopy(new_cf.get_ase_mol())
for rotor_index, torsion in enumerate(new_cf.torsions):
    for angle_index in range(len(scan_angles)):
        # reset the atoms
        new_cf._ase_molecule = start_atoms
        new_cf.update_coords_from(mol_type="ase")
        atoms = new_cf.get_ase_mol()

        # and rotate to desired increment
        atoms.rotate_dihedral(
            new_cf.torsions[rotor_index].atom_indices[0],
            new_cf.torsions[rotor_index].atom_indices[1],
            new_cf.torsions[rotor_index].atom_indices[2],
            new_cf.torsions[rotor_index].atom_indices[3],
            scan_angles[angle_index],
            mask=new_cf.torsions[rotor_index].mask
        )
        new_cf._ase_molecule = atoms
        new_cf.update_coords_from(mol_type="ase")
    
        fname = os.path.join(f'rotor_{rotor_index:04}_{angle_index:04}.com')

        scan_job_lines = [
            "%mem=5GB",
            "%nprocshared=16",
            "#P m062x/cc-pVTZ",
            "Opt=(CalcFC,ModRedun,noeig,maxcycles=900)" + " scf=(tight, direct, maxcycle=900) integral=(grid=ultrafine, Acc2E=12) iop(2/9=2000)",  # TS if freeze_core
            "",
            "Gaussian input for a rotor scan",
            "",
            f"0 {new_cf.rmg_molecule.multiplicity}",
        ]
        rdmol = new_cf._rdkit_molecule
        cart_crds = np.array(rdmol.GetConformers()[0].GetPositions()) * unit.angstrom
        zm = zmatrix_ase.ZMatrix(new_cf.get_ase_mol())
        
        if None in zm.ordered_atom_list:
            # failed to build zmatrix, probably because the distance between atoms in TS is not found as a bond
            # and so it thinks there are two separate molecules
            multipliers = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
            for i in range(len(multipliers)):
                zm = zmatrix_ase.ZMatrix(new_cf.get_ase_mol(), cutoff_multiplier=multipliers[i])
                if None not in zm.ordered_atom_list:
                    break
            else:
                raise ValueError('Could not build zmatrix')
        
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
        
        # dihedral to scan
        indices = new_cf.torsions[rotor_index].atom_indices
        
        
        # convert to z-matrix index
        first = zm.a2z(indices[0]) + 1
        second = zm.a2z(indices[1]) + 1
        third = zm.a2z(indices[2]) + 1
        fourth = zm.a2z(indices[3]) + 1

        # freeze the dihedral in question since we're doing the scan externally and not within Gaussian
        scan_job_lines.append(f"D {first} {second} {third} {fourth} F")
        
        scan_job_lines.append("")
        with open(fname, 'w') as f:
            for line in scan_job_lines:
                f.write(line + '\n')

    # write the run.sh file
    runfile = os.path.join(f'run_{rotor_index:04}.sh')
    base_script = os.path.join(DFT_DIR, 'slurm_scripts', f'unrelaxed_ts_rotors_{ENVIRONMENT.lower()}.sh')
    with open(base_script, 'r') as f:
        base_script_text = f.read()
    base_script_text = base_script_text.format(
        job_name=f'rot_{rotor_index:04}',
        rotor_dir='.',
        rotor_index=f'{rotor_index:04}',
    )
    with open(runfile, 'w') as f:
        f.write(base_script_text)
