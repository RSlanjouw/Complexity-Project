# plot start of the project 
import numpy as np
import matplotlib.pyplot as plt

grid_size = (300, 300)
np.random.seed(123)
criminality = np.random.rand(*grid_size) # Define the initial criminality for every cell
education = np.full(grid_size, 0.5) # Define the education for every cell with a fixed value of 0.5
income = np.full(grid_size, 0.5) # Define the income for every cell with a fixed value of 0.5
alpha = 0.3 # Assign weight for influence of criminality in own neighbourhood
beta = 1 - alpha # Assign weight for influence of criminality in other neighbourhoods 
influence_diff = 0 # Assign weight for difference in influence of "bad" neighbourhoods compared to "good" neighbourhoods
percolation_threshold = 0.5 # Define the percolation threshold to later calculate the giant component
police_threshold = 0.7 # Set the threshold of criminality for police intervention
police_effect = 0.3 # Decide by how much criminality is reduced in a cell when police acts
redistribution_frac = 0.7 # Decide how much of the criminality is redistributed to neighbouring cells
police_units = 15 # Define the number of available police units

# plot start of the project
plt.figure()
plt.imshow(criminality, cmap='plasma')
plt.colorbar()
plt.title('Criminality')
plt.show()


# plot education
plt.figure()
plt.imshow(education, cmap='plasma')
plt.colorbar()
plt.title('Education')
plt.show()