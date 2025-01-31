import numpy as np


def police(criminality, police_threshold, police_effect, redistribution_frac, police_units, grid_size): # Apply police intervention to the criminality grid

    criminality_copy = criminality.copy()
    # save mask for visualization purposes
    mask = np.zeros_like(criminality, dtype=bool) 

    # Collect and sort cells with sufficient criminality
    police_candidates = np.argwhere(criminality > police_threshold) 
    police_candidates = sorted(police_candidates, key=lambda x: criminality[x[0], x[1]], reverse=True) 

    interventions = police_candidates[:police_units] 

    for x, y in interventions:
        mask[x, y] = True

        criminality_copy[x, y] = np.clip(criminality[x, y] - police_effect, 0, 1) 

        neighbors_x = range(max(0, x-1), min(grid_size[0], x+2))
        neighbors_y = range(max(0, y-1), min(grid_size[1], y+2))

        # Redistribute the criminality of the cell to its neighbours according to the redistribution fraction
        for nx in neighbors_x:
            for ny in neighbors_y:
                if (nx, ny) == (x, y):
                    continue
                criminality_copy[nx, ny] += (police_effect * redistribution_frac) / (len(neighbors_x) * len(neighbors_y) - 1)
    
    return criminality_copy, mask