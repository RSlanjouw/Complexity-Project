# Functions for detecting and tracking the number of avelanches
import numpy as np
from scipy.ndimage import label
from modules.grid_update import update_grid_nopolice

def detect_avelanche(criminality, new_criminality, threshold): 

    diff = np.abs(new_criminality - criminality)
    affected_cells = diff > threshold 

    labeled_avalanches, _ = label(affected_cells) 

    avalanche_sizes = np.bincount(labeled_avalanches.ravel())[1:] 

    return avalanche_sizes, labeled_avalanches

def track_avalanches(criminality, education, income, influence_diff, time_steps, threshold, alpha=0.3):

    all_avelanches_sizes = []
    beta = 1 - alpha
    for _ in range(time_steps): 
        new_criminality = update_grid_nopolice(criminality, education, income, influence_diff, alpha=alpha, beta=beta)
        avalanche_sizes, _ = detect_avelanche(criminality, new_criminality, threshold)
        all_avelanches_sizes.extend(avalanche_sizes)
        criminality = new_criminality.copy()

    return all_avelanches_sizes