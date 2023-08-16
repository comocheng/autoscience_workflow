import sys
import thermokinetic_fun


if len(sys.argv) > 1:
    idx = int(sys.argv[1])
else:
    idx = 749

thermokinetic_fun.setup_opt(idx, 'center')
thermokinetic_fun.run_opt(idx, 'center')

