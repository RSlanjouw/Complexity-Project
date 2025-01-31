import numpy as np
from modules.plotter import NewPlot
from scipy.stats import sem, t
from modules.grid_update import update_grid_nopolice, update_grid_withpolice, giant_component


def simulate_emergence(grid_size=(30, 30), timesteps=70, alpha=0.3, 
                       connection_threshold=0.5, police_threshold=0.7, police_effect=0.3, 
                       redistribution_frac=0.7, police_units=15, num_simulation=30, title='Emergence', police=True, onlypolice=False, savefig=True): 
    """
    Simulates the emergence of a giant component in a social system with or without police intervention. 
    The simulation tracks how different parameters affect the size of the giant component over a series 
    of timesteps.

    The function runs the simulation multiple times and computes the average size of the giant component, along with the 
    corresponding error margins.
    """ 
    beta = 1 - alpha
    influence_diff_list = np.linspace(-beta / 2, beta / 2, 15) 
    all_giant_fractions = []
    average_giant_fractions_nop = []
    plot = NewPlot()
    # Generate data for the case without police
    if not onlypolice:
        for _ in range(num_simulation): 
            giant_fractions = []
            for influence_diff in influence_diff_list: 
                criminality = np.random.rand(*grid_size) 
                education = np.random.rand(*grid_size) 
                income = np.random.rand(*grid_size) 
                for _ in range(timesteps): 
                    criminality = update_grid_nopolice(criminality, education, income, influence_diff, alpha, beta)
                giant_fractions.append(giant_component(criminality, connection_threshold)) 
            all_giant_fractions.append(giant_fractions) 

        all_giant_fractions = np.array(all_giant_fractions)
        average_giant_fractions_nop = np.mean(all_giant_fractions, axis=0) 
        std_err = sem(all_giant_fractions, axis=0) 
        error_margin_nop = std_err * t.ppf((1 + 0.95) / 2, num_simulation - 1) 

        # Plot the size of the giant component after the fixed amount of timesteps, 
        # and a fixed threshold, for every influence difference value (with 95% CI)
        plot.add_plot(influence_diff_list, average_giant_fractions_nop, ci_min=average_giant_fractions_nop - error_margin_nop, ci_max=average_giant_fractions_nop + error_margin_nop, label = 'Giant Component size without police')
    else:
        error_margin_nop = 0

    # Generate data for the case with police
    if police:
        all_giant_fractions = []
        average_giant_fractions_withp = []

        for _ in range(num_simulation): 
            giant_fractions = []
            for influence_diff in influence_diff_list: 
                criminality = np.random.rand(*grid_size) 
                education = np.random.rand(*grid_size) 
                income = np.random.rand(*grid_size) 
                for _ in range(timesteps): 
                    criminality = update_grid_withpolice(criminality, education, income, influence_diff, police_threshold, police_effect, redistribution_frac, police_units, grid_size, alpha, beta)[0]
                giant_fractions.append(giant_component(criminality, connection_threshold)) 
            all_giant_fractions.append(giant_fractions) 

        all_giant_fractions = np.array(all_giant_fractions)
        average_giant_fractions_withp = np.mean(all_giant_fractions, axis=0) 
        std_err = sem(all_giant_fractions, axis=0) 
        error_margin_withp = std_err * t.ppf(1.95 / 2, num_simulation - 1) 

        # Plot the size of the giant component after the fixed amount of timesteps (and a fixed threshold) for every influence difference value (with 95% CI)
        plot.add_plot(influence_diff_list, average_giant_fractions_withp, ci_min=average_giant_fractions_withp - error_margin_withp, ci_max=average_giant_fractions_withp + error_margin_withp, label = 'Giant Component size with police')
    else:
        error_margin_withp = 0
        average_giant_fractions_withp = 0

    plot.add_title('Emergence of Giant Component')
    plot.add_labels('Difference in Influence', 'Fraction of Giant Component')


    if savefig:
        plot.save(f'{title}.png')
    return average_giant_fractions_nop, average_giant_fractions_withp, error_margin_nop, error_margin_withp