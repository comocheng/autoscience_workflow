# script to take a run.sh file where only some of the
import os
import sys
import glob
import random
import autotst_wrapper


input_script = os.path.abspath(sys.argv[1])

# needs at least one .com at the same level.
rotor_dir = os.path.dirname(input_script)
coms = glob.glob(os.path.join(rotor_dir, '*.com'))

rotor_index = int(os.path.basename(coms[0])[len('rotor_'):len('rotor_0000')])
incomplete_indices = []
for angle_index in range(21):
    logname = os.path.join(rotor_dir, f'rotor_{rotor_index:04}_{angle_index:04}.log')
    if not os.path.exists(logname):
        incomplete_indices.append(angle_index)
    elif autotst_wrapper.get_termination_status(logname) != 0:
        incomplete_indices.append(angle_index)

array_str = autotst_wrapper.ordered_array_str(incomplete_indices)


rerun_file = os.path.join(rotor_dir, 'rerun.sh')
with open(input_script, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    # replace the array line
    if '#SBATCH --array' in lines[i]:
        lines[i] = f'#SBATCH --array={array_str}%5' + '\n'
with open(rerun_file, 'w') as f:
    f.writelines(lines)
