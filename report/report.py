# module for making pdf reports explaining the difference between two mechanisms

import sys
import os
import glob


import numpy as np
import pandas as pd

import arkane.ess.gaussian


import matplotlib.pyplot as plt


DFT_DIR = os.environ['DFT_DIR']
sys.path.append(DFT_DIR)
import autotst_wrapper

import autotst.species
import ase.atoms


sys.path.append(os.environ['DATABASE_DIR'])
import database_fun

N_improve = 10

def get_projected_freqs(logfile):
    species_index = autotst_wrapper.get_species_index_from_path(logfile)
    
    gl = arkane.ess.gaussian.GaussianLog(logfile)
    conformer, unscaled_freq = gl.load_conformer()
    coordinates, number, mass = gl.load_geometry()
    conformer.coordinates = (coordinates, "angstroms")
    conformer.number = number
    conformer.mass = (mass, "amu")
    linear = None
    is_ts = False
    hessian = gl.load_force_constant_matrix()
    
    
    rmg_species = database_fun.index2species(species_index)
    species_smiles = rmg_species.smiles

    # make a conformer object again
    new_cf = autotst.species.Conformer(smiles=species_smiles)  # TODO make this from adjacency list?
    new_cf._ase_molecule = ase.Atoms(number, coordinates)
    new_cf.update_coords_from(mol_type="ase")
    assert not autotst_wrapper.bonds_too_large(None, species_index, atoms=new_cf._ase_molecule)

    torsions = new_cf.get_torsions()
    rotors = []
    for i in range(len(torsions)):
        rotor_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'arkane', f'rotor_{i:04}.log')
        backup_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'arkane', f'rotor_{i:04}_scan_energies.txt')
        try:
            rl = arkane.ess.gaussian.GaussianLog(rotor_file)
            vlist, angles = rl.load_scan_energies()
        except (arkane.exceptions.LogError, FileNotFoundError):
            rl = None
        if rl is None:
            try:
                rl = arkane.statmech.ScanLog(backup_file)
                angles, vlist = rl.load()
                # try to read the scan_energies version
            except (FileNotFoundError, arkane.exceptions.LogError):
                return unscaled_freq, np.zeros_like(unscaled_freq)
        
        symmetry = arkane.statmech.determine_rotor_symmetry(vlist, '', '')

        pivots, tops = autotst_wrapper.get_pivots_tops(new_cf, torsions[i], i)
        rotors.append((pivots, tops, symmetry))

    new_freqs = arkane.statmech.project_rotors(conformer, hessian, rotors, linear, is_ts)
    
    assert len(new_freqs) + len(rotors) == len(unscaled_freq)
    
    return unscaled_freq, new_freqs
    
def plot_proj_rotors(original_freqs, new_freqs, title=None):
    # Frequencies to start
    n_rotors = len(original_freqs) - len(new_freqs)
    plt.figure(figsize=(5, 3))
    plt.scatter(np.arange(len(original_freqs)), original_freqs, marker='+', label='Before')
    plt.scatter(np.arange(n_rotors, n_rotors + len(new_freqs)), new_freqs, marker='x', label='After')
    plt.legend()
    plt.ylabel('Freq (cm^-1)')
    plt.xlabel('Frequency Index')
    plt.title(title)
    plt.show()


def get_prev_run_folders(chemkin_file):
    fuel_name = os.path.basename(os.path.dirname(chemkin_file)).split('_')[0]
    run_dirs = sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(chemkin_file)), f'{fuel_name}_*')))
    prev_run_dirs = []
    for i in range(len(run_dirs)):
        if run_dirs[i] > os.path.dirname(chemkin_file):
            continue
        prev_run_dirs.append(run_dirs[i])
    return prev_run_dirs


def get_changelists(chemkin_file):
    # relies on the fuel_YYYYMMDD structure
    # returns the list of changelists. What was supposed to be calculated each round
    fuel_name = os.path.basename(os.path.dirname(chemkin_file)).split('_')[0]

    # keep only the ones that appear in the top 10 of a mech_summary
    mech_files = sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(chemkin_file)), f'{fuel_name}_*/mech_summary*.csv')))
    # print(mech_files)
    total_rxn_include_list = []
    total_sp_include_list = []
    list_include_lists_sp = []
    list_include_lists_rxn = []
    for mech_file in mech_files:
        if os.path.dirname(mech_file) > os.path.dirname(chemkin_file):
            print('skipping', mech_file)
            continue
            # only include mech files that came before

        rxn_include_list = []
        sp_include_list = []
        mech_summary = pd.read_csv(mech_file, index_col=0)
        # get the first 10 reactions to attempt for every iteration of this
        for i in range(len(mech_summary)):
            if len(rxn_include_list) + len(sp_include_list) >= N_improve:
                break
            
            db_index = mech_summary['db_index'].values[i]
            if mech_summary['possible'].values[i] and mech_summary['family'].values[i] != 'species':
                # make sure it wasn't in a previous include list
                
                if db_index in total_rxn_include_list:
                    print(f'not counting failed (or PDEP) reaction {db_index}')
                    continue
                
                rxn_include_list.append(db_index)
            elif mech_summary['possible'].values[i] and mech_summary['family'].values[i] == 'species':
                if db_index in total_sp_include_list:
                    print(f'not counting failed species {db_index}')
                    continue
                
                sp_include_list.append(db_index)
            if len(rxn_include_list) + len(sp_include_list) >= N_improve:
                break

                
        total_rxn_include_list += rxn_include_list
        total_sp_include_list += sp_include_list
        
        list_include_lists_sp.append(sp_include_list)
        list_include_lists_rxn.append(rxn_include_list)
    return list_include_lists_sp, list_include_lists_rxn




