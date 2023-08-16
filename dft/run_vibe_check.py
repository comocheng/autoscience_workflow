import re
import os
import sys
import glob
import thermokinetic_fun




try:
    reaction_index = int(sys.argv[1])
    DFT_DIR = '/work/westgroup/harris.se/autoscience/reaction_calculator/dft'
    logfiles = glob.glob(os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}', 'overall', 'fwd_ts_*.log'))
except ValueError:
    logfiles = [os.path.abspath(sys.argv[1])]
    
    rm_text = 'reaction_calculator'
    if rm_text in logfile[0]:
        logfile[0] = logfile[0].split(rm_text)[-1]

    reaction_index = int(re.search('reaction_(.*?)/', logfile[0]).group(1))

for logfile in logfiles:
    if thermokinetic_fun.check_vib_irc(reaction_index, logfile):
        print(f'{logfile} is valid')
    
