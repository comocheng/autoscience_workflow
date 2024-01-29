import sys
import autotst_wrapper


idx = int(sys.argv[1])

autotst_wrapper.setup_opt(idx, 'overall')
autotst_wrapper.run_opt(idx, 'overall')
