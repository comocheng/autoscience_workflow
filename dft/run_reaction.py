import sys
import thermokinetic_fun


if len(sys.argv) > 1:
    idx = int(sys.argv[1])
else:
    raise ValueError('Must specify reaction index')


status = thermokinetic_fun.setup_opt(idx, 'shell')
if status:
    status = thermokinetic_fun.run_opt(idx, 'shell')
else:
    exit(1)


if status:
    status = thermokinetic_fun.setup_opt(idx, 'center')
else:
    exit(1)

if status:
    status = thermokinetic_fun.run_opt(idx, 'center')
else:
    exit(1)


if status:
    status = thermokinetic_fun.setup_opt(idx, 'overall')
else:
    exit(1)

if status:
    status = thermokinetic_fun.run_opt(idx, 'overall')
else:
    exit(1)


if status:
    status = thermokinetic_fun.setup_arkane_reaction(idx)
else:
    exit(1)

if status:
    status = thermokinetic_fun.run_arkane_reaction(idx)
else:
    exit(1)

