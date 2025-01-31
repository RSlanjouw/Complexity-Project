# plot start of the project 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from scipy.ndimage import label

from modules.grid_update import update_grid_withpolice, update_grid_nopolice
# from test_files.grids import grid1

grid_len = 50
grid_size = (grid_len, grid_len)
np.random.seed(123)

criminality = np.zeros(grid_size) # Define the initial criminality for every cell
criminality[np.random.randint(0, grid_len-1),np.random.randint(0, grid_len-1)] = np.random.random()

education = np.random.rand(*grid_size) # Define the education for every cell with a fixed value of 0.5
income = np.random.rand(*grid_size) # Define the income for every cell with a fixed value of 0.5
alpha = 0.3 # Assign weight for influence of criminality in own neighbourhood
beta = 1 - alpha # Assign weight for influence of criminality in other neighbourhoods 
influence_diff = 0.1 # Assign weight for difference in influence of "bad" neighbourhoods compared to "good" neighbourhoods
percolation_threshold = 0.5 # Define the percolation threshold to later calculate the giant component
redistribution_frac = 0.7 # Decide how much of the criminality is redistributed to neighbouring cells
police_units = 15 # Define the number of available police units

# plot start of the project
plt.figure()
plt.imshow(criminality, cmap='plasma', vmin=0, vmax=1)
plt.colorbar()
plt.title('Criminality')
plt.show()


# plot education
plt.figure()
plt.imshow(education, cmap='plasma', vmin=0, vmax=1)
plt.colorbar()
plt.title('Education')
plt.show()

def animate(t): # Define function to use in FuncAnimation (update grid for every timestep)
    global criminality
    criminality = update_grid_nopolice(criminality, education, income, influence_diff=0.1, alpha=0.3, beta=0.7)

    # Save the layer with the criminality levels
    cax.set_array(criminality)

    return cax

fig, ax = plt.subplots()
cax = ax.imshow(criminality, cmap='plasma', vmin=0, vmax=1)
fig.colorbar(cax, ax=ax)
ax.set_title('Criminality')
timesteps = 100
ani = FuncAnimation(fig, animate, frames=range(0,timesteps), interval=10, repeat = False)
ani.save('window.gif')

plt.show()