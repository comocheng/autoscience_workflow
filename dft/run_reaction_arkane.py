import sys
import thermokinetic_fun


if len(sys.argv) > 1:
    indices = [int(sys.argv[1])]
else:
    indices = [i for i in range(0, 110)]


force_valid_ts = False
if len(sys.argv) > 2:
    if sys.argv[2].lower() == 'force_valid_ts' or sys.argv[2].lower() == '--force_valid_ts':
        force_valid_ts = True

for idx in indices:
    thermokinetic_fun.setup_arkane_reaction(idx, force_valid_ts=force_valid_ts)
    thermokinetic_fun.run_arkane_reaction(idx)
