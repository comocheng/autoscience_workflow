import sys
import thermokinetic_fun


if len(sys.argv) > 1:
    idx = int(sys.argv[1])
else:
    idx = 749

thermokinetic_fun.setup_opt(idx, 'overall')
thermokinetic_fun.run_opt(idx, 'overall')

