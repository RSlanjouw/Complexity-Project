import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider
from scipy.ndimage import label
from modules.grid_update import update_grid_nopolice, update_grid_withpolice

# Define parameters

grid_size = (100, 100)
np.random.seed(1)
criminality = np.random.rand(*grid_size) # Define the initial criminality for every cell
education = np.random.rand(*grid_size) # Define the education for every cell (here fixed, but can be linked to data in final model)
income = np.random.rand(*grid_size) # Define the income for every cell (here fixed, but can be linked to data in final model)
# education = np.full(grid_size, 0.5) # Define the education for every cell with a fixed value of 0.5
# income = np.full(grid_size, 0.5) # Define the income for every cell with a fixed value of 0.5
alpha = 0.3 # Assign weight for influence of criminality in own neighbourhood
beta = 1 - alpha # Assign weight for influence of criminality in other neighbourhoods 
influence_diff = 0.1 # Assign weight for difference in influence of "bad" neighbourhoods compared to "good" neighbourhoods
percolation_threshold = 0.5 # Define the percolation threshold to later calculate the giant component
police_threshold = 0.8 # Set the threshold of criminality for police intervention
police_effect = 0.3 # Decide by how much criminality is reduced in a cell when police acts
redistribution_frac = 0.7 # Decide how much of the criminality is redistributed to neighbouring cells
police_units = 15 # Define the number of available police units



def animate(t): # Define function to use in FuncAnimation (update grid for every timestep)
    global criminality
    criminality, mask = update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size)

# Initialize figure
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)  # Ruimte maken voor slider

# Criminality heatmap
im = ax.imshow(criminality, cmap='hot', interpolation='nearest')
plt.colorbar(im, label='Criminality Level')
plt.title('Criminality Evolution')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# Slider voor handmatige controle
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # Positie slider (x, y, breedte, hoogte)
slider = Slider(ax_slider, 'Frame', 0, timesteps - 1, valinit=0, valstep=1)

timesteps = 100

ani = FuncAnimation(fig, animate, frames=timesteps, interval=100, repeat = False)

plt.show()
