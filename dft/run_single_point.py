import sys
import autotst_wrapper

# for i in range(150, 250):
#     idx = i
#     autotst_wrapper.setup_species_single_point(idx, force_rerun=True)
#     autotst_wrapper.run_species_single_point(idx, force_rerun=True)
idx = int(sys.argv[1])

parallel = True
if len(sys.argv) > 2:
    option = sys.argv[2]
    if option.lower() in ['parallel=false', '--parallel=false', 'serial', '--serial', '--serial=true', 'serial=true']:
        parallel = False

autotst_wrapper.setup_single_point(idx, calc_type='species', force_rerun=True, parallel=parallel)
autotst_wrapper.run_single_point(idx, calc_type='species', force_rerun=True)
