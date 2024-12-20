import sys
import autotst_wrapper


idx = int(sys.argv[1])

parallel = True
if len(sys.argv) > 2:
    option = sys.argv[2]
    if option.lower() in ['parallel=false', '--parallel=false', 'serial', '--serial', '--serial=true', 'serial=true']:
        parallel = False

autotst_wrapper.setup_single_point(idx, calc_type='reaction', force_rerun=True, parallel=parallel)
autotst_wrapper.run_single_point(idx, calc_type='reaction', force_rerun=True)
