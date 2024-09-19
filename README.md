# Autoscience Workflow 1.0

# About
The autoscience workflow is a software repository that enables the automated development of detailed kinetic models for gas-phase combustion applications. It uses RMG to generate a mechanism, identifies the most important parameters of the mechanism to improve, calculates them with DFT, and then uses the updated parameters for the next round of model generation. This way the workflow iteratively improves the model accuracy without requiring any experimental data to learn from.

# Overview
The cycle of model improvement works as follows:
1. Generate the model in [RMG](https://rmg.mit.edu/)
2. Run uncertainty and sensitivity analysis (uses [Cantera](https://cantera.org/) for reactor simulations) to rank model parameters for improvement
3. Calculate top 10 thermodynamic or kinetic parameters using DFT (uses [AutoTST](https://github.com/ReactionMechanismGenerator/AutoTST) for conformer and transition-state geometry guessing, [Gaussian 16](https://gaussian.com/gaussian16/) for electronic structure calculations, and [Arkane](https://reactionmechanismgenerator.github.io/RMG-Py/users/arkane/index.html) for statistical thermodynamics and TST calculations)
4. Compile new calculations into a library for RMG to use in the next iteration of model generation
5. Repeat model generation (step 1) and check for convergence
6. Compare converged mechanism simulations to experimental data in literature

# Instructions
## 0. Installation
- Set the `$AUTOSCIENCE_REPO` environment variable to point to your local copy of the autoscience_workflow repository. You can add the following line to your .bashrc to do it for you: `export AUTOSCIENCE_REPO="/path/to/your/copy/of/autoscience_workflow"` Many of the scripts depend on this.
- Install [RMG](https://rmg.mit.edu/) (Arkane is a component of RMG, and Cantera gets installed with the default RMG instructions, so no need to worry about those separately). Checkout the [autoscience_uncertainties](https://github.com/sevyharris/RMG-Py/tree/autoscience_uncertainties) branch to be able to export the uncertainty estimates of model parameters.
- Scripts assume access to Gaussian 16 and SLURM workload manager. They also use this [job manager](https://github.com/sevyharris/job_manager) package which contains many helper functions related to starting and waiting for SLURM jobs.
- Install [AutoTST](https://github.com/ReactionMechanismGenerator/AutoTST), set the branch to [autotst_workflow](https://github.com/sevyharris/AutoTST/tree/autoscience_workflow)
- Install [hotbit](https://github.com/pekkosk/hotbit). This does the fast/approximate geometry optimizations to narrow down the list of conformers to calculate with higher level of theory methods. If there is difficulty installing this, we recommend modifying the code to use [xtb](https://github.com/grimme-lab/xtb) as an alternative.
## 1. Model Generation with RMG
Users are referred to the [RMG website](https://rmg.mit.edu/) for more complete instructions on how to use RMG, but the basic gist is this:
- Copy RMG_example_fuel_YYYYMMDD to a new location and modify the input.py file (or create your own) to specify the reactants you are investigating, the reactor conditions of interest, and which libraries to include.
- Run rmg.py with the command `python-jl /path/to/RMG-Py/rmg.py input.py` to generate the mechanism. This will probably take on the order of days, depending on the size of the mechanism you intend to build. RMG will generate many files, but these three RMG outputs are required for the autoscience workflow. An example of each has been copied into the example folder (NOTE that RMG is not completely deterministic and the same input file can result in slightly different mechanisms):
  - chem_annotated.inp - contains the list of species and reactions for the mechanism along with thermodynamic and kinetic parameter values
  - tran.dat - contains transport data
  - species_dictionary.txt - contains bond connectivity information for each species

Once the model is generated you can do a quick check of the ignition delay results with the [plotting/check_mech.ipynb](https://github.com/comocheng/autoscience_workflow/blob/main/plotting/check_mech.ipynb) Jupyter Notebook.
    
## 2. Uncertainty and Sensitivity Analysis
Update the libraries in the [analysis/export_uncertainty.py](https://github.com/comocheng/autoscience_workflow/blob/main/analysis/export_uncertainty.py) script to match the exact order of libraries that were used to generate the mechanism.

Run the [analysis/run_analysis.py](https://github.com/comocheng/autoscience_workflow/blob/main/analysis/run_analysis.py) script by calling `sbatch analysis/run_analysis.sh path/to/chem_annotated.inp` It does the following:
- Uncertainty Analysis
  - Runs export_uncertainty.py, which generates two numpy files containing the list of species and reaction uncertainties:
    - gao_species_uncertainties.npy
    - gao_reaction_uncertainties.npy
- Sensitivity Analysis (sensitivity of ignition delay to model parameters)
  - Runs the baseline ignition delay simulation across temperature and pressure conditions
  - Perturbs every species and reaction parameter and runs an ignition delay simulation to compute the ignition delay sensitivity
- Ranks Parameters
  - Uses the sensitivity and uncertainty results with the uncertainty of the DFT method to create an Improvement score, a measure of how calculating the parameter is expected to improve the model
  - Negative improvement score means calculating the parameter and replacing the existing value will make the model worse
  - Saves top 200 ordered parameters to a mech_summary.csv file

## 3. Calculate Parameters
Run the [dft/autorunner.py](https://github.com/comocheng/autoscience_workflow/blob/main/dft/autorunner.py) script by calling `sbatch dft/autorunner.sh path/to/mech_summary.csv` It does the following:
- Uses AutoTST to make guesses about species or reaction transition-state geometries
- Uses Gaussian 16 to run geometry optimizations and then energy and frequency calculations
- Uses Arkane to compute thermodynamic and kinetic parameter values from Gaussian 16 logs and save in RMG library format

You can also run calculations for an individual reaction with the [dft/run_whole_reaction.py](https://github.com/comocheng/autoscience_workflow/blob/main/dft/run_whole_reaction.py) script: `sbatch dft/run_whole_reaction.sh REACTION_INDEX` where REACTION_INDEX is the that reaction's index in the [reaction database](https://github.com/comocheng/autoscience_workflow/blob/main/database/reaction_database.csv)

Or calculations for an individual species with the [dft/run_species.py](https://github.com/comocheng/autoscience_workflow/blob/main/dft/run_species.py) script: `sbatch dft/run_species.sh SPECIES_INDEX` where SPECIES_INDEX is the that species's index in the [species database](https://github.com/comocheng/autoscience_workflow/blob/main/database/species_database.csv)

## 4. Compile Calculations into Library for RMG
- Run the compile_lib.ipynb Jupyter Notebook to generate the thermodynamics and kinetics library files.
- This copies them into the RMG-database for use during the next phase of model generation

## 5. Repeat Model Generation
Return to step 1, but be sure to include the latest libraries in the input.py file

To check if the model has converged (ignition delays are within 10% of previous values at all temperatures), run the plotting/check_converged.ipynb Notebook

## 6. Compare to Experiments
See plotting plotting/check_mech.ipynb and plotting/plot_subset_delays.ipynb Notebooks for examples of plotting ignition delays.

Some other plots of interest:
- local uncertainty
- global uncertainty (have to run the Monte Carlo sampling script)
- species flux comparison diagram
- individual species thermodynamics
- individual reaction kinetics
- comparison of top sensitivities

