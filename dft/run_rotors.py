import sys
import autotst_wrapper


idx = int(sys.argv[1])
if len(sys.argv) > 2:
    increment_deg = float(sys.argv[2])
else:
    increment_deg = 20

autotst_wrapper.setup_rotors(idx, increment_deg=increment_deg)
autotst_wrapper.run_rotors(idx, increment_deg=increment_deg)
