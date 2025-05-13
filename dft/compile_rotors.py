import sys
import autotst_wrapper

rotor_dir = sys.argv[1]
rotor_index = int(sys.argv[2])
autotst_wrapper.assemble_rotor_scan_energies(rotor_dir, rotor_index=rotor_index)

