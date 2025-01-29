import numpy as np
from scipy.ndimage import label

from modules.police import police
from modules.grid_update import update_grid_nopolice

def detect_avelanche(criminality, new_criminality, threshold): # Detect if an avelanche happened in the grid

    diff = np.abs(new_criminality - criminality)
    affected_cells = diff > threshold # Get the cells where the difference in criminality is above the threshold

    labeled_avalanches, num_features = label(affected_cells) # Label the avelanches

    avalanche_sizes = np.bincount(labeled_avalanches.ravel())[1:] # Count the number of cells in each avelanche

    return avalanche_sizes, labeled_avalanches

def track_avalanches(criminality, education, income, influence_diff, time_steps, threshold):

    all_avelanches_sizes = []
    for step in range(time_steps): # In each time step, update the grid and detect avelanches and their sizes
        new_criminality = update_grid_nopolice(criminality, education, income, influence_diff)
        avalanche_sizes, labeled_avalanches = detect_avelanche(criminality, new_criminality, threshold)
        all_avelanches_sizes.extend(avalanche_sizes)
        criminality = new_criminality.copy()

    return all_avelanches_sizes