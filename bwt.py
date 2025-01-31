# BY: Bonnie and Cellulair Automata
# FOR: Complex System Simulation
# PURPOSE: Make a visualization representing the broken window theory.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from modules.grid_update import update_grid_withpolice, update_grid_nopolice

# Set-up initial parameters
grid_len = 50
grid_size = (grid_len, grid_len)
np.random.seed(123)

criminality = np.zeros(grid_size) 
criminality[np.random.randint(0, grid_len-1),np.random.randint(0, grid_len-1)] = np.random.random()

education = np.random.rand(*grid_size) 
income = np.random.rand(*grid_size) 
alpha = 0.3 
beta = 1 - alpha 
influence_diff = 0.1 
percolation_threshold = 0.5 
redistribution_frac = 0.7 
police_units = 15 

# Plot the initial conditions of the simulation
plt.figure()
plt.imshow(criminality, cmap='plasma', vmin=0, vmax=1)
plt.colorbar()
plt.title('Criminality')
plt.show()


# Plot education
plt.figure()
plt.imshow(education, cmap='plasma', vmin=0, vmax=1)
plt.colorbar()
plt.title('Education')
plt.show()

def animate(t): 
    global criminality
    criminality = update_grid_nopolice(criminality, education, income, influence_diff=0.1, alpha=0.3, beta=0.7)
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