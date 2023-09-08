import sys
import autotst_wrapper


idx = int(sys.argv[1])

autotst_wrapper.setup_opt(idx, 'center')
autotst_wrapper.run_opt(idx, 'center')

