import numpy as np


def police(criminality, police_threshold, police_effect, redistribution_frac, police_units, grid_size): # Apply police intervention to the criminality grid

    criminality_copy = criminality.copy()
    mask = np.zeros_like(criminality, dtype=bool) # Generate an equal grid to save location of police interventions to visualize later

    police_candidates = np.argwhere(criminality > police_threshold) # Get the coordinates of cells with criminality above the police threshold
    police_candidates = sorted(police_candidates, key=lambda x: criminality[x[0], x[1]], reverse=True) # Sort the cells by descending criminality

    interventions = police_candidates[:police_units] # Select the cells where police will act based on the number of available police units

    for x, y in interventions:
        mask[x, y] = True
        criminality_copy[x, y] = np.clip(criminality[x, y] - police_effect, 0, 1) # Reduce the criminality of the cell by the police effect

        neighbors_x = range(max(0, x-1), min(grid_size[0], x+2))
        neighbors_y = range(max(0, y-1), min(grid_size[1], y+2))

        # Redistribute the criminality of the cell to its neighbours according to the redistribution fraction
        for nx in neighbors_x:
            for ny in neighbors_y:
                if (nx, ny) == (x, y):
                    continue
                criminality_copy[nx, ny] += (police_effect * redistribution_frac) / (len(neighbors_x) * len(neighbors_y) - 1)
    
    return criminality_copy, mask