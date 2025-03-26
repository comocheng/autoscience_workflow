import sys
import autotst_wrapper


idx = int(sys.argv[1])
autotst_wrapper.setup_freq(idx, calc_type='reaction', force_rerun=True)
autotst_wrapper.run_freq(idx, calc_type='reaction', force_rerun=True)
