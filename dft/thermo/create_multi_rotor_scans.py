# script to generate more rotor files that will scan the rotor at a different starting point
# you must manually set the species index and rotor number

import re
import os

import numpy as np

import ase.io.gaussian
import ase.io.zmatrix

species_index = 75
rotor_index = 1

DFT_DIR = os.environ['DFT_DIR']


# read the job file:
original_rotor_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'rotors', f'rotor_{rotor_index:04}.com')
with open(original_rotor_file, 'r') as f:
    lines = f.readlines()
    
    for i in range(1, 5):
        pattern = 'D\s(\d \d \d \d) S '
        m1=re.search(pattern, lines[-i])
        if m1:
            scanline_index = i
            scanline = lines[-i]
            break

dihedral_indices = [int(x) for x in scanline.split()[1:5]]
print('dihedral indices: ', dihedral_indices)

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
    m1=re.search(bond_pattern, z_value_row)
    if m1:        
        bond_name = z_value_row.split()[0]
        bond_value = float(z_value_row.strip().split()[-1])
        bonds[bond_name] = bond_value
        continue
    
    # look for angle
    angle_pattern = 'A\d\s*'
    m1=re.search(angle_pattern, z_value_row)
    if m1:        
        angle_name = z_value_row.split()[0]
        angle_value = float(z_value_row.strip().split()[-1])
        angles[angle_name] = angle_value
        
    # look for dihedral
    dihedral_pattern = 'D\d\s*'
    m1=re.search(dihedral_pattern, z_value_row)
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

assert len(my_dihedral) == 1

print(f'Changing dehedral {my_dihedral[0]}: {dihedrals[my_dihedral[0]]}')


splice_dir = os.path.join(os.path.dirname(original_rotor_file), 'spliced_rotors')
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

    file_name_rev = os.path.join(splice_dir, f'rotor_{rotor_index:04}_rev_{i:04}.com')
    with open(file_name_rev, 'w') as f:
        file_lines[scanline_index] = file_lines[scanline_index].replace('20.0', '-20.0')
        f.writelines(file_lines)
    
# Make slurm scripts to run all the rotors
fwd_label = f'rotor_{rotor_index:04}_fwd_'
slurm_run_file = os.path.join(splice_dir, 'run_many_fwd.sh')
slurm_settings = {
    '--job-name': f'g16_rot_{species_index}',
    '--error': 'error.log',
    '--nodes': 1,
    '--partition': 'west,short',
    '--exclude': 'c5003',
    '--mem': '20Gb',
    '--time': '24:00:00',
    '--cpus-per-task': 16,
    '--array': f'0-8',
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

# ----------------------- repeat for reverse -----------------------------
rev_label = f'rotor_{rotor_index:04}_rev_'
slurm_run_file_rev = os.path.join(splice_dir, 'run_many_rev.sh')
slurm_file_writer_rev = job_manager.SlurmJobFile(full_path=slurm_run_file_rev)
slurm_file_writer_rev.settings = slurm_settings
slurm_file_writer_rev.content = [
    'export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch\n',
    'mkdir -p $GAUSS_SCRDIR\n',
    'module load gaussian/g16\n',
    'source /shared/centos7/gaussian/g16/bsd/g16.profile\n\n',

    'RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))\n',
    f'fname="{rev_label}' + '${RUN_i}.com"\n\n',

    'g16 $fname\n',
]
slurm_file_writer_rev.write_file() 

