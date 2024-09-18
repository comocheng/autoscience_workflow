import re
import os
import sys
import glob
import autotst_wrapper


try:
    reaction_index = int(sys.argv[1])
    DFT_DIR = '$AUTOSCIENCE_REPO/dft'
    logfiles = glob.glob(os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}', 'overall', 'fwd_ts_*.log'))
except ValueError:
    logfiles = [os.path.abspath(sys.argv[1])]

    rm_text = 'reaction_calculator'
    if rm_text in logfile[0]:
        logfile[0] = logfile[0].split(rm_text)[-1]

    reaction_index = int(re.search('reaction_(.*?)/', logfile[0]).group(1))

for logfile in logfiles:
    if autotst_wrapper.check_vib_irc(reaction_index, logfile):
        print(f'{logfile} is valid')
