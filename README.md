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
- Install [RMG](https://rmg.mit.edu/) (Arkane is a component of RMG, and Cantera gets installed with the default RMG instructions, so no need to worry about those separately)
- Scripts assume access to Gaussian 16 and SLURM workload manager
- Install [AutoTST](https://github.com/ReactionMechanismGenerator/AutoTST), set the branch to [autotst_workflow](https://github.com/sevyharris/AutoTST/tree/autoscience_workflow)
- Install [hotbit](https://github.com/pekkosk/hotbit). This does the fast/approximate geometry optimizations to narrow down the list of conformers to calculate with higher level of theory methods. If there is difficulty installing this, we recommend modifying the code to use [xtb](https://github.com/grimme-lab/xtb) as an alternative.
## 1. Model Generation with RMG
- Copy the example folder RMG_example_fuel_YYYYMMDD to a new location (some of the scripts use the date format, so we recommend keeping that)
- Users are referred to the [RMG website](https://rmg.mit.edu/) for more complete instructions on how to use RMG, but the basic gist is this:
  - Create/modify the input.py file like the one in RMG_example_fuel_YYYYMMDD to specify the reactants you are investigating and which libraries to include
  - Run RMG to generate the following additional files:
    - chem_annotated.inp - contains the list of species and reactions for the mechanism along with thermodynamic and kinetic parameter values
    - tran.dat - contains transport data
    - species_dictionary.txt - contains bond connectivity information for each species
    - (RMG generates a lot more files than these three, but these are the important ones for the autoscience workflow)
- Modify the export_uncertainty.py script to include whichever libraries were included in the input.py file
    
## 2. Uncertainty and Sensitivity Analysis
Run the "run_analysis.sh" script. It does the following:
- Uncertainty Analysis
  - runs export_uncertainty.py, which generates two numpy files containing the list of species and reaction uncertainties:
    - gao_species_uncertainties.npy
    - gao_reaction_uncertainties.npy
- Sensitivity Analysis (sensitivity of ignition delay to model parameters)
  - Runs the baseline ignition delay simulation across temperature and pressure conditions
  - Perturbs every species and reaction parameter and runs an ignition delay simulation to compute the ignition delay sensitivity
- Ranks Parameters
  - Uses the sensitivity and uncertainty results with the uncertainty of the DFT method to create an Improvement score, a measure of how calculating the parameter is expected to improve the model
  - Negative improvement score means calculating the parameter and replacing the existing value will make the model worse
  - Saves top 200 ordered parameters to mechanism_YYYYMMDD.csv

## 3. Calculate top 10 thermodynamic or kinetic parameters using DFT
Run the run_autorunner.sh script. It does the following:
- Uses AutoTST to make guesses about species or reaction transition-state geometries
- Uses Gaussian 16 to run geometry optimizations and then energy and frequency calculations
- Uses Arkane to compute thermodynamic and kinetic parameter values from Gaussian 16 logs and save in RMG library format


