import sys
import thermokinetic_fun


if len(sys.argv) > 1:
    idx = int(sys.argv[1])
else:
    idx = 110

thermokinetic_fun.screen_species_conformers(idx)
thermokinetic_fun.optimize_conformers(idx)

