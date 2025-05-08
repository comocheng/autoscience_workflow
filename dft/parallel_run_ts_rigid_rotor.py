import sys
import autotst_wrapper


idx = int(sys.argv[1])

outsource_root = '/scratch/harris.se/guassian_scratch/rotor_calcs'
autotst_wrapper.setup_ts_rotors(idx, outsource_dir=outsource_root, force_rerun=True, relaxed=False)
#autotst_wrapper.run_ts_rotors(idx)
