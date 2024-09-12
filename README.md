# Autoscience Workflow 1.0

# About
The autoscience workflow is a software repository that enables the automated development of detailed kinetic models for gas-phase combustion applications. It uses RMG to generate a mechanism, identifies the most important parameters of the mechanism to improve, calculates them with DFT, and then uses the updated parameters for the next round of model generation. This way the workflow iteratively improves the model accuracy without requiring any experimental data to learn from.

# Overview
The cycle of model improvement works as follows:
1. Generate the model in [RMG](https://rmg.mit.edu/)
2. Run uncertainty and sensitivity analysis (uses [Cantera](https://cantera.org/) for reactor simulations)
3. Rank model parameters by importance
4. Calculate top 10 thermodynamic or kinetic parameters using DFT (uses [AutoTST](https://github.com/ReactionMechanismGenerator/AutoTST) for conformer and transition-state geometry guessing, [Gaussian 16](https://gaussian.com/gaussian16/) for electronic structure calculations, and [Arkane](https://reactionmechanismgenerator.github.io/RMG-Py/users/arkane/index.html) for statistical thermodynamics and TST calculations)
5. Compile new calculations into a library for RMG to use in the next iteration of model generation
6. Repeat model generation (step 1) and check for convergence
7. Compare converged mechanism simulations to experimental data in literature



