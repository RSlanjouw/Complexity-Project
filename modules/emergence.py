import numpy as np
from plotter import NewPlot
from scipy.stats import sem, t

from modules.grid_update import update_grid_nopolice, update_grid_withpolice, giant_component


def simulate_emergence(grid_size=(30, 30), timesteps=70, alpha=0.3, 
                       connection_threshold=0.5, police_threshold=0.7, police_effect=0.3, 
                       redistribution_frac=0.7, police_units=15, num_simulation=30, title='Emergence', police=True, onlypolice=False, savefig=True): # Function to plot emergence of giant component for different influence differences
    
    beta = 1 - alpha
    influence_diff_list = np.linspace(-beta / 2, beta / 2, 15) # Generate a list of influence differences (the x-axis of the plot)
    # print(influence_diff_list)
    all_giant_fractions = []
    average_giant_fractions_nop = []
    plot = NewPlot()
    # Generate data for the case without police
    if not onlypolice:
        for i in range(num_simulation): # Repeat the simulation a few times to get an average curve for the emergence graph
            giant_fractions = []
            for influence_diff in influence_diff_list: # Loop through the influence difference values
                criminality = np.random.rand(*grid_size) # Reset the criminality grid
                education = np.random.rand(*grid_size) # Reset the education grid
                income = np.random.rand(*grid_size) # Reset the income grid
                for _ in range(timesteps): # Run the simulation for a long enough time
                    criminality = update_grid_nopolice(criminality, education, income, influence_diff, alpha, beta)
                giant_fractions.append(giant_component(criminality, connection_threshold)) # Get the size of the giant component
            all_giant_fractions.append(giant_fractions) # Store the giant component sizes for every influence difference value

        all_giant_fractions = np.array(all_giant_fractions)
        average_giant_fractions_nop = np.mean(all_giant_fractions, axis=0) # Compute the average giant component size for every influence difference value
        std_err = sem(all_giant_fractions, axis=0) # Compute the standard error of the mean for every influence difference value
        error_margin_nop = std_err * t.ppf((1 + 0.95) / 2, num_simulation - 1) # Compute the error margin for the confidence interval

        # Plot the size of the giant component after the fixed amount of timesteps (and a fixed threshold) for every influence difference value (with 95% CI)
        plot.add_plot(influence_diff_list, average_giant_fractions_nop, ci_min=average_giant_fractions_nop - error_margin_nop, ci_max=average_giant_fractions_nop + error_margin_nop, label = 'Giant Component size without police')
    else:
        error_margin_nop = 0

    # Generate data for the case with police
    if police:
        all_giant_fractions = []
        average_giant_fractions_withp = []

        for i in range(num_simulation): # Repeat the simulation a few times to get an average curve for the emergence graph
            giant_fractions = []
            for influence_diff in influence_diff_list: # Loop through the influence difference values
                criminality = np.random.rand(*grid_size) # Reset the criminality grid
                education = np.random.rand(*grid_size) # Reset the education grid
                income = np.random.rand(*grid_size) # Reset the income grid
                for _ in range(timesteps): # Run the simulation for a long enough time
                    criminality = update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size, alpha, beta)[0]
                giant_fractions.append(giant_component(criminality, connection_threshold)) # Get the size of the giant component
            all_giant_fractions.append(giant_fractions) # Store the giant component sizes for every influence difference value

        all_giant_fractions = np.array(all_giant_fractions)
        average_giant_fractions_withp = np.mean(all_giant_fractions, axis=0) # Compute the average giant component size for every influence difference value
        std_err = sem(all_giant_fractions, axis=0) # Compute the standard error of the mean for every influence difference value
        error_margin_withp = std_err * t.ppf(1.95 / 2, num_simulation - 1) # Compute the error margin for the confidence interval

        # Plot the size of the giant component after the fixed amount of timesteps (and a fixed threshold) for every influence difference value (with 95% CI)
        plot.add_plot(influence_diff_list, average_giant_fractions_withp, ci_min=average_giant_fractions_withp - error_margin_withp, ci_max=average_giant_fractions_withp + error_margin_withp, label = 'Giant Component size with police')
    else:
        error_margin_withp = 0
        average_giant_fractions_withp = 0

    plot.add_title('Emergence of Giant Component')
    plot.add_labels('Difference in Influence', 'Fraction of Giant Component')

    # if police:
    #     plt.figtext(0.5, 0.01, f'Emergence of the Giant component in a {grid_size[0]}x{grid_size[1]} grid. Measurements are taken after {timesteps} timesteps and are averaged out {num_simulation} runs. The colored area around the line represents the 95% CI. Alpha is set to {alpha}; the connection threshold to {connection_threshold}; the police threshold (to take action) is set to {police_threshold}; the police effect to {police_effect} of which a fraction of {redistribution_frac} is redistributed to neighbours; the number of police units is {police_units}.',
    #                 wrap=True, horizontalalignment='center', fontsize=9)
    # else:
    #     plt.figtext(0.5, 0.01, f'Emergence of the Giant component in a {grid_size[0]}x{grid_size[1]} grid. Measurements are taken after {timesteps} timesteps and are averaged out {num_simulation} runs. The colored area around the line represents the 95% CI. Alpha is set to {alpha}; the connection threshold to {connection_threshold}. No police intervention is considered.',
    #                 wrap=True, horizontalalignment='center', fontsize=9)
                
    # plt.legend()

    if savefig:
        plot.save(f'{title}.png')
    # plot.show()
    return average_giant_fractions_nop, average_giant_fractions_withp, error_margin_nop, error_margin_withp