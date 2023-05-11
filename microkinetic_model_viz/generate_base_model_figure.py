
from rmgpy.tools import fluxdiagram

chemkin = "/home/moon/autoscience/reaction_calculator/models/base_rmg_1week/chem_annotated.inp"
spec_dict = "/home/moon/autoscience/reaction_calculator/models/base_rmg_1week/species_dictionary.txt"
input_file = "/home/moon/autoscience/reaction_calculator/models/base_rmg_1week/input_one_setting.py"
output_path = "/home/moon/autoscience/reaction_calculator/microkinetic_model_viz/"
fluxdiagram.create_flux_diagram(input_file, chemkin, spec_dict, save_path=output_path, settings={'max_edge_pen_width': 20})

# I went into fluxdiagram and manually set the pen_size to 0 for species
# and increased the scale of the images to 1.1
