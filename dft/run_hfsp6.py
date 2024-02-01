import sys
import autotst_wrapper


idx = int(sys.argv[1])

autotst_wrapper.setup_opt(idx, 'hfsp')
autotst_wrapper.run_opt(idx, 'hfsp')
autotst_wrapper.setup_arkane_reaction(idx, overall_dirname='hfsp')
autotst_wrapper.run_arkane_reaction(idx)
