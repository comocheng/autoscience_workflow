import sys
import thermokinetic_fun


if len(sys.argv) > 1:
    indices = [int(sys.argv[1])]
else:
    #indices = [i for i in range(0, 110)]
    #indices = [i for i in range(10, 110)]
    #indices = [i for i in range(67, 110)]
    indices = [i for i in range(71, 110)]


for idx in indices:
    thermokinetic_fun.setup_arkane_species(idx)
    thermokinetic_fun.run_arkane_species(idx)

