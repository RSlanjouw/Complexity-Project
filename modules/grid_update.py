import numpy as np

from scipy.ndimage import label
from numpy.lib.stride_tricks import sliding_window_view

from modules.police import police

def update_grid_nopolice(criminality, education, income, influence_diff, alpha=0.3, beta=0.7):
    padded_crim = np.pad(criminality, pad_width=1, mode='constant', constant_values=np.nan)
    neighborhoods = sliding_window_view(padded_crim, (3, 3))
    neighbors = neighborhoods.reshape(*criminality.shape, 9)
    neighbors = np.delete(neighbors, 4, axis=2)
    
    current = criminality[..., np.newaxis]
    
    more_mask = neighbors > current
    less_mask = neighbors <= current
    sum_more = np.nansum(neighbors * more_mask, axis=2)
    count_more = np.nansum(more_mask, axis=2)
    more_infl = np.divide(sum_more, count_more, out=np.zeros_like(sum_more), where=count_more!=0)
    sum_less = np.nansum(neighbors * less_mask, axis=2)
    count_less = np.nansum(less_mask, axis=2)
    less_infl = np.divide(sum_less, count_less, out=np.zeros_like(sum_less), where=count_less!=0)
    # calculate gamma for each cell avr of income and education
    gamma = (income + education) / 2
    w_more = beta * np.clip(1 - gamma, 0.1, 0.9) + influence_diff
    w_less = beta/2 - influence_diff
    new_crim = alpha*criminality + w_more*more_infl + w_less*less_infl
    
    return np.clip(new_crim, 0, 1)



def update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size=(300,300), alpha=0.3, beta=0.7): # Update the criminality of the whole grid based on the update_cell function and police intervention

    new_criminality = update_grid_nopolice(criminality, education, income, influence_diff,alpha=alpha,beta=beta) # Update the criminality of the whole grid without police intervention

    new_criminality, mask = police(new_criminality, police_threshold, police_effect, redistribution_frac, police_units, grid_size=grid_size) # Apply police intervention and save the mask grid to visualize the intervention
    
    return new_criminality, mask

def giant_component(criminality, percolation_threshold): # Compute the size of the giant component in the criminality grid (as fraction of the grid size)
    perc_cells = criminality >= percolation_threshold # Output the grid with True value for cells with criminality above the percolation threshold
    labeled_crim, num_features = label(perc_cells) # Label the connected components in the grid (every cluster of connected cells gets a unique label)
    components = np.bincount(labeled_crim.ravel()) # Count the number of cells in each connected component
    giant_component = np.max(components[1:]) if len(components) > 1 else 0 # Get the size of the largest connected component

    return giant_component / criminality.size
