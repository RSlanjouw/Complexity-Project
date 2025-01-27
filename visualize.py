import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from scipy.ndimage import label

from modules.grid_update import update_grid_withpolice
# Define parameters

grid_size = (300, 300)
np.random.seed(123)
criminality = np.random.rand(*grid_size) # Define the initial criminality for every cell
education = np.random.rand(*grid_size) # Define the education for every cell (here fixed, but can be linked to data in final model)
income = np.random.rand(*grid_size) # Define the income for every cell (here fixed, but can be linked to data in final model)
alpha = 0.3 # Assign weight for influence of criminality in own neighbourhood
beta = 1 - alpha # Assign weight for influence of criminality in other neighbourhoods 
influence_diff = 0 # Assign weight for difference in influence of "bad" neighbourhoods compared to "good" neighbourhoods
percolation_threshold = 0.5 # Define the percolation threshold to later calculate the giant component
police_threshold = 0.7 # Set the threshold of criminality for police intervention
police_effect = 0.3 # Decide by how much criminality is reduced in a cell when police acts
redistribution_frac = 0.7 # Decide how much of the criminality is redistributed to neighbouring cells
police_units = 15 # Define the number of available police units


def animate(t): # Define function to use in FuncAnimation (update grid for every timestep)
    global criminality
    criminality, mask = update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units)
    # Save the layer with the criminality levels
    cax.set_array(criminality)
    # Save the layer with the police intervention
    mask_layer = np.zeros((*grid_size, 4))
    mask_layer[mask] = [0, 1, 0, 1] # Set the color of the police intervention to red and set the transparency to 0.5
    overlay_cax.set_data(mask_layer)
    return cax, overlay_cax

fig, ax = plt.subplots()
cax = ax.imshow(criminality, cmap='plasma', vmin=0, vmax=1)
overlay_cax = ax.imshow(np.zeros((*grid_size, 4)))
fig.colorbar(cax, ax=ax)
ax.set_title('Criminality')

timesteps = 10
print("Simulation started")
ani = FuncAnimation(fig, animate, frames=timesteps, interval=500)
HTML(ani.to_jshtml())
ani.save('simulation.html', writer='html')
print("Simulation finished")
