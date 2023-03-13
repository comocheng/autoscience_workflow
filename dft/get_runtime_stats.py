import re
import os
import glob

import numpy as np


#DFT_DIR = '/work/westgroup/harris.se/autoscience/reaction_calculator/dft'
DFT_DIR = '/work/westgroup/harris.se/autoscience/autoscience/butane/dft'


def get_runtime(log_file):
    """Analyze a Gaussian run by reading in reverse (allegedly faster than reading from start)

    Elapsed time:       0 days  1 hours 27 minutes 57.7 seconds.
    """
    error_termination = False
    with open(log_file, 'rb') as f:
        f.seek(0, os.SEEK_END)
        for i in range(0, 20):
            try:
                f.seek(-2, os.SEEK_CUR)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            saved_position = f.tell()
            last_line = f.readline().decode()
            f.seek(saved_position, os.SEEK_SET)
            if 'elapsed time' in last_line.lower():
                days = float(re.search('Elapsed time:(.*?)days', last_line).group(1).strip())
                hours = float(re.search('days(.*?)hours', last_line).group(1).strip())
                minutes = float(re.search('hours(.*?)minutes', last_line).group(1).strip())
                total_hours = 24 * days + hours + minutes / 60.0
                return total_hours
    return np.nan


def get_runtimes(search_type='shell'):
    """ get the runtimes for shell calculations in DFT dir
    """
    shell_files = glob.glob(os.path.join(DFT_DIR, 'kinetics', 'reaction_*', search_type, 'fwd_ts_*.log'))
    print(f'{len(shell_files)} {search_type} files found')

    times = []
    for i in range(0, len(shell_files)):
        hrs = get_runtime(shell_files[i])
        #if np.isnan(hrs):
        #    print(f'incomplete {shell_files[i]}')
        times.append(hrs)

    average = np.nanmean(times)
    min_time = np.nanmin(times)
    max_time = np.nanmax(times)
    med_time = np.nanmedian(times)
    completed = len(times) - np.sum(np.isnan(times))
    missing = np.sum(np.isnan(times))
    print("Average runtime: {:.2f}".format(average))
    print("Median runtime: {:.2f}".format(med_time))
    print("Minimum runtime: {:.2f}".format(min_time))
    print("Maximum runtime: {:.2f}".format(max_time))
    print(f'{missing} missing time summary')
    print(f'{completed} completed')
    #print(f'Average runtime: {np.nanmean(times)}')
    np.save(f'{search_type}_times.npy', times)


if __name__ == '__main__':
    get_runtimes('shell')
    get_runtimes('overall')


