import sys
import autotst_wrapper


idx = int(sys.argv[1])

autotst_wrapper.setup_rotors(idx)
autotst_wrapper.run_rotors(idx)
