import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem, t

from modules.grid_update import update_grid_nopolice, update_grid_withpolice, giant_component

def simulate_emergence_if(grid_size=(30, 30), timesteps=70, alpha=0.3, 
                       percolation_threshold=0.5, police_threshold=0.7, police_effect=0.3, 
                       redistribution_frac=0.7, police_units=15, num_simulation=30, title='Emergence'):
    
    beta = 1 - alpha
    influence_diff_list = np.linspace(-beta / 2, beta / 2, 30)
    print(influence_diff_list)
    all_giant_fractions = []
    average_giant_fractions = []

    # Generate data for the case without police
    for i in range(num_simulation): # Repeat the simulation a few times to get an average curve for the emergence graph
        giant_fractions = []
        for influence_diff in influence_diff_list: # Loop through the influence difference values
            criminality = np.random.rand(*grid_size) # Reset the criminality grid
            education = np.random.rand(*grid_size) # Reset the education grid
            income = np.random.rand(*grid_size) # Reset the income grid
            for _ in range(timesteps): # Run the simulation for a long enough time
                criminality = update_grid_nopolice(criminality, education, income, influence_diff, alpha, beta)
            giant_fractions.append(giant_component(criminality, percolation_threshold)) # Get the size of the giant component
        all_giant_fractions.append(giant_fractions) # Store the giant component sizes for every influence difference value

    all_giant_fractions = np.array(all_giant_fractions)
    average_giant_fractions = np.mean(all_giant_fractions, axis=0) # Compute the average giant component size for every influence difference value
    std_err = sem(all_giant_fractions, axis=0) # Compute the standard error of the mean for every influence difference value
    error_margin = std_err * t.ppf((1 + 0.95) / 2, num_simulation - 1) # Compute the error margin for the confidence interval

    # Plot the size of the giant component after the fixed amount of timesteps (and a fixed threshold) for every influence difference value (with 95% CI)
    plt.plot(influence_diff_list, average_giant_fractions, color = 'b', label = 'Giant Component size without police')
    plt.fill_between(influence_diff_list, average_giant_fractions - error_margin, average_giant_fractions + error_margin, color = 'b', alpha = 0.2)

    # Generate data for the case with police
    police_threshold = 0.6 # Set the threshold of criminality for police intervention
    police_effect = 0.45 # Decide by how much criminality is reduced in a cell when police acts
    redistribution_frac = 0.01 # Decide how much of the criminality is redistributed to neighbouring cells
    police_units = 40 # Define the number of available police units

    all_giant_fractions = []
    average_giant_fractions = []

    for i in range(num_simulation): # Repeat the simulation a few times to get an average curve for the emergence graph
        giant_fractions = []
        for influence_diff in influence_diff_list: # Loop through the influence difference values
            criminality = np.random.rand(*grid_size) # Reset the criminality grid
            education = np.random.rand(*grid_size) # Reset the education grid
            income = np.random.rand(*grid_size) # Reset the income grid
            for _ in range(timesteps): # Run the simulation for a long enough time
                criminality = update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size, alpha, beta)[0]
            giant_fractions.append(giant_component(criminality, percolation_threshold)) # Get the size of the giant component
        all_giant_fractions.append(giant_fractions) # Store the giant component sizes for every influence difference value

    all_giant_fractions = np.array(all_giant_fractions)
    average_giant_fractions = np.mean(all_giant_fractions, axis=0) # Compute the average giant component size for every influence difference value
    std_err = sem(all_giant_fractions, axis=0) # Compute the standard error of the mean for every influence difference value
    error_margin = std_err * t.ppf(1.95 / 2, num_simulation - 1) # Compute the error margin for the confidence interval

    # Plot the size of the giant component after the fixed amount of timesteps (and a fixed threshold) for every influence difference value (with 95% CI)
    plt.plot(influence_diff_list, average_giant_fractions, color = 'r', label = 'Giant Component size with police')
    plt.fill_between(influence_diff_list, average_giant_fractions - error_margin, average_giant_fractions + error_margin, color = 'r', alpha = 0.2)
    plt.title('Emergence of Giant Component')
    plt.xlabel('Difference in Influence')
    plt.ylabel('Fraction of Giant Component')
    plt.subplots_adjust(bottom=0.28)
    plt.figtext(0.5, 0.01, f"""Emergence of the Giant component in a {grid_size[0]}x{grid_size[1]} grid. Measurements are taken after {timesteps} timesteps and are averaged out {num_simulation} runs. The colored area around the line represents the 95% CI. Alpha is set to {alpha}; the percolation threshold to {percolation_threshold}; the police threshold (to take action) is set to {police_threshold}; the police effect to {police_effect} of which a fraction of {redistribution_frac} is redistributed to neighbours; the number of police units is {police_units}.""",
                            wrap=True, horizontalalignment='center', fontsize=9)
    plt.legend()
    plt.savefig(f'figs/{title}.png')

# giant_component_for_different_alpha
def simulate_emergence_a(grid_size=(30, 30), timesteps=70, alpha_l=(0,1), influence_diff=0, 
                       percolation_threshold=0.5, police_threshold=0.7, police_effect=0.3, 
                       redistribution_frac=0.7, police_units=15, police=False, amount_of_runs=1, title='Emergence of Giant Component', save_values=False):
    np.random.seed(123)
    alpha_list = np.linspace(alpha_l[0],alpha_l[1], 30)
    average_giant_fractions = []
    init_criminality = np.random.rand(*grid_size)
    education = np.random.rand(*grid_size)
    income = np.random.rand(*grid_size)

    for i in range(amount_of_runs):
        print(f"Simulation {i+1}/30")
        giant_fractions = []
        for alpha in alpha_list:
            print(alpha)
            beta = 1 - alpha
            criminality = init_criminality
            for ts in range(timesteps):
                criminality = update_grid_withpolice(criminality, education, income, influence_diff, 
                                                         police_threshold, police_effect, redistribution_frac, police_units, alpha, beta, grid_size)[0]
            giant_fractions.append(giant_component(criminality, percolation_threshold))
        average_giant_fractions.append(giant_fractions)

    if save_values:
        np.save(f'averages_giant_fractions_alpha_fluct.npy', average_giant_fractions)
    average_giant_fractions = np.mean(average_giant_fractions, axis=0)

    plt.plot(alpha_list, average_giant_fractions)
    plt.title('Emergence of Giant Component')
    plt.xlabel('Difference in Influence')
    plt.ylabel('Fraction of Giant Component')
    plt.savefig('figs/emergence.png')



simulate_emergence_if()