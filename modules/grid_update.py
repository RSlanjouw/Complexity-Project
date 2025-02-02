# BY: Bonnie and Cellulair Automata
# FOR: Complex System Simulation
# PURPOSE: To update the grid based on the criminality, education, income, influence difference, alpha and beta values

import numpy as np

from scipy.ndimage import label
from numpy.lib.stride_tricks import sliding_window_view

from modules.police import police

def update_grid_nopolice(criminality, education, income, influence_diff, alpha, beta):
    # function to update the grid using numpy vectors, unbelievable fast and efficient
    padded_crim = np.pad(criminality, pad_width=1, mode='constant', constant_values=np.nan)
    neighborhoods = sliding_window_view(padded_crim, (3, 3))
    neighbors = neighborhoods.reshape(*criminality.shape, 9)
    neighbors = np.delete(neighbors, 4, axis=2)
    
    current = criminality[..., np.newaxis]
    
    more_mask = neighbors >= current
    less_mask = neighbors <= current
    sum_more = np.nansum(neighbors * more_mask, axis=2)
    count_more = np.nansum(more_mask, axis=2)
    more_infl = np.divide(sum_more, count_more, out=np.zeros_like(sum_more), where=count_more!=0)
    sum_less = np.nansum(neighbors * less_mask, axis=2)
    count_less = np.nansum(less_mask, axis=2)
    less_infl = np.divide(sum_less, count_less, out=np.zeros_like(sum_less), where=count_less!=0)
    # calculate gamma for each cell avr of income and education
    gamma = (income + education) / 2
    w_more = (beta * np.clip(1 - gamma, 0.1, 0.9) + influence_diff) 
    w_less = beta/2 - influence_diff

    m = w_more * more_infl
    m = np.where(count_less == 0, m*2, m)

    l = w_less * less_infl

    l = np.where(count_more == 0, l*2, l)

    new_crim = alpha*criminality + m + l
    return np.clip(new_crim, 0, 1)



def update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size=(300,300), alpha=0.3, beta=0.7): 
    # yes this function updates the grid with police what wonder. not readable in the tile of the function
    new_criminality = update_grid_nopolice(criminality, education, income, influence_diff,alpha=alpha,beta=beta)
    new_criminality, mask = police(new_criminality, police_threshold, police_effect, redistribution_frac, police_units, grid_size=grid_size)
    
    return new_criminality, mask

def giant_component(criminality, connection_threshold): 
    # funciton to calculate the giant component in the grid. 
    perc_cells = criminality >= connection_threshold 
    labeled_crim, num_features = label(perc_cells)
    components = np.bincount(labeled_crim.ravel()) 
    giant_component = np.max(components[1:]) if len(components) > 1 else 0 

    return giant_component / criminality.size
