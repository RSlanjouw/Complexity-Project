import numpy as np
import matplotlib.pyplot as plt

from modules.grid_update import update_grid_nopolice, update_grid_withpolice, giant_component

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


# Plot the size of the giant component for different values of influence difference between "good" and "bad" neighbourhoods (without police)

timesteps = 70
influence_diff_list = np.linspace(-beta/2, beta/2, 30) # Define the range of influence difference (of "bad" influence compared to the "good" one) to study the emergence of the giant component
average_giant_fractions = []
init_criminality = np.random.rand(*grid_size)

for i in range(5): # Repeat the simulation a few times to get an average curve for the emergence graph
    print(f"Simulation {i+1}/5")
    giant_fractions = []
    for influence_diff in influence_diff_list: # Loop through the influence difference values
        criminality = init_criminality # Reset the criminality grid
        for t in range(timesteps): # Run the simulation for a long enough time
            print(f"Time step {t+1}/{timesteps}")
            criminality = update_grid_nopolice(criminality, education, income,influence_diff)
        print(f"Finished influence difference {influence_diff}")
        giant_fractions.append(giant_component(criminality, percolation_threshold)) # Get the size of the giant component
    average_giant_fractions.append(giant_fractions) # Store the giant component sizes for every influence difference value

average_giant_fractions = np.mean(average_giant_fractions, axis=0) # Compute the average giant component size for every influence difference value

# Plot the size of the giant component after the fixed amount of timesteps (and a fixed threshold) for every influence difference value
plt.plot(influence_diff_list, average_giant_fractions)
plt.title('Emergence of Giant Component')
plt.xlabel('Difference in Influence')
plt.ylabel('Fraction of Giant Component')
# save in figs folder
plt.savefig('figs/emergence.png')