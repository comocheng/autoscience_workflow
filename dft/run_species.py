import sys
import autotst_wrapper


idx = int(sys.argv[1])

autotst_wrapper.screen_species_conformers(idx)
autotst_wrapper.optimize_conformers(idx)
autotst_wrapper.setup_rotors(idx)
autotst_wrapper.run_rotors(idx)
autotst_wrapper.setup_arkane_species(idx)
autotst_wrapper.run_arkane_species(idx)
