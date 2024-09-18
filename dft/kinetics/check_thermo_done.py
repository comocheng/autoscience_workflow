import sys
import pandas as pd
import os

reaction_index = int(sys.argv[1])


df = pd.read_csv(os.path.join(os.environ['AUTOSCIENCE_REPO'], 'dft', 'reaction_database.csv'))


unique_string = df.loc[df['i'] == reaction_index]['unique_string'].values[0]

reactants = [int(x) for x in unique_string.split('=')[0].split('+')]
products = [int(x) for x in unique_string.split('=')[1].split('+')]

incomplete = False
for species_index in reactants + products:
    if not os.path.exists(os.path.join(os.environ['AUTOSCIENCE_REPO'], 'dft', 'thermo', f'species_{species_index:04}', 'arkane', 'RMG_libraries', 'thermo.py')):
        print(species_index, 'is not done')

        incomplete = True

if not incomplete:
    print('All species are done', unique_string)
