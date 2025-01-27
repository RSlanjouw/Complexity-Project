import numpy as np
from scipy.ndimage import label

from modules.police import police
from concurrent.futures import ThreadPoolExecutor

def update_cell(x, y, criminality, education, income, influence_diff, alpha=0.3, beta=0.7):
    current_state = criminality[x, y]
    neighbors = criminality[max(0, x-1):x+2, max(0, y-1):y+2]
    neighbors = np.delete(neighbors, (neighbors.shape[0] // 2, neighbors.shape[1] // 2))

    less_crim_influence = np.mean(neighbors[neighbors <= current_state]) if np.any(neighbors <= current_state) else 0
    more_crim_influence = np.mean(neighbors[neighbors > current_state]) if np.any(neighbors > current_state) else 0

    gamma = np.mean([education[x, y], income[x, y]])

    weight_more = (beta * np.clip(1 - gamma, 0.1, 0.9)) + influence_diff
    weight_less = (beta / 2) - influence_diff

    new_state = (
        alpha * current_state +
        weight_more * more_crim_influence +
        weight_less * less_crim_influence
    )
    return np.clip(new_state, 0, 1)

def update_grid_nopolice(criminality, education, income, influence_diff, grid_size=(300, 300), num_threads=4):
    new_criminality = np.zeros_like(criminality)

    def process_row(x):
        row_result = []
        for y in range(grid_size[1]):
            row_result.append(update_cell(x, y, criminality, education, income, influence_diff))
        return x, row_result

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(process_row, range(grid_size[0])))

    for x, row_result in results:
        new_criminality[x, :] = row_result

    return new_criminality

def update_cell_withbuildup(x, y, criminality, education, income, influence_diff, buildup, alpha=0.3,beta=0.7): # Update the criminality of a cell based on its neighbours and itself

    current_state = criminality[x, y]
    neighbors = criminality[max(0, x-1):x+2, max(0,y-1):y+2] # Get the 8 neighbours of the cell
    neighbors = np.delete(neighbors, (neighbors.shape[0] // 2, neighbors.shape[1] // 2)) # Remove the cell itself from the neighbours

    # Here we distinguish between neighbours with more criminality and neighbours with less criminality
    less_crim_influence = np.mean(neighbors[neighbors <= current_state - buildup]) if np.any(neighbors <= current_state) else 0
    more_crim_influence = np.mean(neighbors[neighbors > current_state + buildup]) if np.any(neighbors > current_state) else 0

    gamma = np.mean([education[x, y], income[x, y]]) # Here we calculate the average sensitivity of the cell to "external" criminality, so that higher education/income result in lower sensitivity (following line)

    # Here we calculate the influence of neighbors distinguishing between more and less criminality (compared to the cell itself) because higher education/income should lower the sensitivity to more criminality but not to less criminality
    weight_more = (beta * np.clip(1 - gamma, 0.1, 0.9)) + influence_diff # We clip the value to avoid the weight to be 0
    weight_less = (beta / 2) - influence_diff

    # Here we calculate the new criminality of the cell based on the criminality of the cell itself and the influence of the neighbours
    new_state = (
        alpha * current_state +
        weight_more * more_crim_influence +
        weight_less * less_crim_influence
    )
    return np.clip(new_state, 0, 1)

def update_grid_nopolice_withbuildup(criminality, education, income, influence_diff, buildup, grid_size=(300,300)): # Update the criminality of the whole grid based on the update_cell function

    new_criminality = np.zeros_like(criminality)
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            new_criminality[x, y] = update_cell_withbuildup(x, y, criminality, education, income, influence_diff, buildup)
    
    return new_criminality

def update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size=(300,300)): # Update the criminality of the whole grid based on the update_cell function and police intervention

    new_criminality = np.zeros_like(criminality)
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            new_criminality[x, y] = update_cell(x, y, criminality, education, income, influence_diff)

    new_criminality, mask = police(new_criminality, police_threshold, police_effect, redistribution_frac, police_units) # Apply police intervention and save the mask grid to visualize the intervention
    
    return new_criminality, mask

def giant_component(criminality, percolation_threshold): # Compute the size of the giant component in the criminality grid (as fraction of the grid size)

    perc_cells = criminality >= percolation_threshold # Output the grid with True value for cells with criminality above the percolation threshold
    labeled_crim, num_features = label(perc_cells) # Label the connected components in the grid (every cluster of connected cells gets a unique label)

    components = np.bincount(labeled_crim.ravel()) # Count the number of cells in each connected component
    giant_component = np.max(components[1:]) if len(components) > 1 else 0 # Get the size of the largest connected component

    return giant_component / criminality.size
