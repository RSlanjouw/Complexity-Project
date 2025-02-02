# BY: Bonnie and Cellulair Automata
# FOR: Complex System Simulation
# PURPOSE: To animate the model on a random grid.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from modules.grid_update import update_grid_withpolice, update_grid_nopolice

# Define parameters
grid_size = (50, 50)
np.random.seed(1)
criminality = np.random.rand(*grid_size) 
education = np.random.rand(*grid_size) 
income = np.random.rand(*grid_size) 


alpha = 0.9 
beta = 1 - alpha 
influence_diff = 0 
percolation_threshold = 0.5 
police_threshold = 0.8 
police_effect = 0.3 
redistribution_frac = 0.7 
police_units = 2 

def animate(t): 
    global criminality
    criminality, mask = update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size)
    cax.set_array(criminality)

    # Animate police
    mask_layer = np.zeros((*grid_size, 4))
    mask_layer[mask] = [0, 1, 0, 1] 
    overlay_cax.set_data(mask_layer)
    return cax, overlay_cax

fig, ax = plt.subplots()
cax = ax.imshow(criminality, cmap='plasma', vmin=0, vmax=1)
overlay_cax = ax.imshow(np.zeros((*grid_size, 4)))
fig.colorbar(cax, ax=ax)
ax.set_title('Criminality')

timesteps = 100

ani = FuncAnimation(fig, animate, frames=timesteps, interval=100, repeat = False)

plt.show()
