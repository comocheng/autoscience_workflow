# script to automatically run reaction all of the post-processing from the RMG run
#
# 0. Estimate the uncertainties of the mechanism parameters and save as .npy
# 1. Add the new species/reactions to the database
# 2. Get species delays
# 3. Run base sensitivity (do species first)
# 4. Run reaction sensitivity
# 5. Compile everything into one big .npy

import os
import sys
import time
import datetime
import subprocess
import job_manager


working_dir = sys.argv[1]
if working_dir.endswith('.inp'):
    working_dir = os.path.dirname(working_dir)
elif working_dir.endswith('.yaml'):
    working_dir = os.path.dirname(working_dir)
chemkin_file = os.path.join(working_dir, 'chem_annotated.inp')
if working_dir == '':
    working_dir = '.'

start_dir = os.getcwd()
os.chdir(working_dir)

logfile = os.path.join(working_dir, 'analysis.log')

AUTOSCIENCE_REPO = os.environ['AUTOSCIENCE_REPO']
assert AUTOSCIENCE_REPO != ''


def printlog(message):
    """Function to print log messages to the official log file and stdout"""
    print(f'{datetime.datetime.now()} {message}')
    with open(logfile, 'a') as f:
        f.write(f'{datetime.datetime.now()} {message}' + '\n')


# Step 0. Estimate parameter uncertainties and save as .npy file
printlog(f'Estimating Parameter Uncertainties')
species_uncertainty_file = os.path.join(os.path.dirname(chemkin_file), 'gao_species_uncertainty.npy')
reaction_uncertainty_file = os.path.join(os.path.dirname(chemkin_file), 'gao_reaction_uncertainty.npy')
if os.path.exists(species_uncertainty_file) and os.path.exists(reaction_uncertainty_file):
    printlog('Skipping uncertainty estimation because uncertainty files already exist')
else:
    export_uncertainty_script = os.path.join(AUTOSCIENCE_REPO, 'analysis', 'export_uncertainty.sh')
    job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {export_uncertainty_script} {chemkin_file}"
    job.submit(slurm_cmd)
    time.sleep(2.0)
    job.wait(check_interval=1.0)
    printlog(f'Done estimating parameter uncertainties')


# Step 1. Add the mechanism to the database
printlog(f'Launching Add Mechanism to Database')
add_mech_script = os.path.join(AUTOSCIENCE_REPO, 'database', 'add_mechanism_to_database.sh')
job = job_manager.SlurmJob()
slurm_cmd = f"sbatch {add_mech_script} {chemkin_file}"
job.submit(slurm_cmd)
time.sleep(2.0)
job.wait(check_interval=1.0)

printlog(f'Done adding Mechanism to Database')


# Step 2. Run the species delays if they're not all done
if not os.path.exists(os.path.join(working_dir, 'table_0007', 'species_delays_0007.npy')):
    printlog('Running the species delays')
    run_species_delays_script = os.path.join(AUTOSCIENCE_REPO, 'analysis', 'make_sp_delay_npys.sh')
    job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {run_species_delays_script} {chemkin_file}"
    job.submit(slurm_cmd)
    time.sleep(2.0)
    job.wait(check_interval=10.0)
    printlog(f'Done running species delays')
else:
    printlog('Species delays already ran')


# Step 3. Run the base delays if they're not all done
if not os.path.exists(os.path.join(working_dir, 'table_0007', 'base_delays_0007.npy')):
    printlog('Running the base delays')
    run_base_delays_script = os.path.join(AUTOSCIENCE_REPO, 'analysis', 'run_base_delays.sh')
    job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {run_base_delays_script} {chemkin_file}"
    job.submit(slurm_cmd)
    time.sleep(2.0)
    job.wait(check_interval=10.0)
    printlog(f'Done running base delays')
else:
    printlog('Base delays already ran')


# Step 4. Run the reaction delays if they're not all done
if not os.path.exists(os.path.join(working_dir, 'table_0007', 'reaction_delays_0007_1200.npy')):
    printlog('Running the base delays')
    run_rxn_delays_script = os.path.join(AUTOSCIENCE_REPO, 'analysis', 'make_rxn_delay_npys.sh')
    job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {run_rxn_delays_script} {chemkin_file}"
    job.submit(slurm_cmd)
    time.sleep(2.0)
    job.wait(check_interval=10.0)
    printlog(f'Done running reaction delays')
else:
    printlog('Reaction delays already ran')

# Step 5. Compile the sensitivity
if not os.path.exists(os.path.join(working_dir, 'total_perturbed_mech_delays.npy')) or \
        not os.path.exists(os.path.join(working_dir, 'total_base_delays.npy')):
    printlog('Compiling sensitivity results')
    compile_sensitivity_script = os.path.join(AUTOSCIENCE_REPO, 'analysis', 'compile_sensitivity.sh')
    job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {compile_sensitivity_script} {chemkin_file}"
    job.submit(slurm_cmd)
    time.sleep(2.0)
    job.wait(check_interval=10.0)
    printlog(f'Done compiling sensitivity results')
else:
    printlog('Sensitivity already compiled')

# Step 6. Calculate and save the improvement scores using sensitivity and uncertainty
printlog('Calculating Improvement Scores')
export_improvement_script = os.path.join(AUTOSCIENCE_REPO, 'analysis', 'export_improvement_scores.sh')
job = job_manager.SlurmJob()
slurm_cmd = f"sbatch {export_improvement_script} {chemkin_file}"
job.submit(slurm_cmd)
time.sleep(2.0)
job.wait(check_interval=10.0)
printlog(f'Done calculating improvement score')

os.chdir(start_dir)
