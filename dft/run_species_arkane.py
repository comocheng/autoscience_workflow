import sys
import autotst_wrapper


idx = int(sys.argv[1])
autotst_wrapper.setup_arkane_species(idx, force_rerun=True)
autotst_wrapper.run_arkane_species(idx, force_rerun=True)
