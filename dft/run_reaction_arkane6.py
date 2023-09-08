import sys
import autotst_wrapper


if len(sys.argv) > 1:
    indices = [int(sys.argv[1])]
else:
    print('Must supply index for arkane reaction calculation')


force_valid_ts = False
if len(sys.argv) > 2:
    if sys.argv[2].lower() == 'force_valid_ts' or sys.argv[2].lower() == '--force_valid_ts':
        force_valid_ts = True

for idx in indices:
    autotst_wrapper.setup_arkane_reaction(idx, force_valid_ts=force_valid_ts)
    autotst_wrapper.run_arkane_reaction(idx)

