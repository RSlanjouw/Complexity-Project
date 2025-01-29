import numpy as np
import matplotlib.pyplot as plt
from plotter import NewPlot
from itertools import product

from modules.grid_update import update_grid_nopolice,update_grid_withpolice, giant_component

def simulate_emergence_if(grid_size=(50, 50), timesteps=70, alpha=0.3, influence_diff_range=(-0.3, 0.5), 
                       percolation_threshold=0.5, police_threshold=0.7, police_effect=0.3, 
                       redistribution_frac=0.7, police_units=15, police=False, amount_of_runs=10, title='Emergence of Giant Component', save_values=False):
    # np.random.seed(123)
    beta = 1 - alpha
    influence_diff_list = np.linspace(influence_diff_range[0], influence_diff_range[1], 30)
    print(influence_diff_list)
    average_giant_fractions = []
    init_criminality = np.random.rand(*grid_size)
    education = np.random.rand(*grid_size)
    income = np.random.rand(*grid_size)

    for i in range(amount_of_runs):
        print(f"Simulation {i+1}/{amount_of_runs}")
        giant_fractions = []
        for influence_diff in influence_diff_list:
            criminality = init_criminality
            for t in range(timesteps):
                if police:
                    criminality = update_grid_withpolice(criminality, education, income, influence_diff, 
                                                         police_threshold, police_effect, redistribution_frac, police_units, alpha=alpha, beta=beta, grid_size=grid_size)[0]
                else:
                    criminality = update_grid_nopolice(criminality, education, income, influence_diff, alpha=alpha, beta=beta)
            giant_fractions.append(giant_component(criminality, percolation_threshold))
        average_giant_fractions.append(giant_fractions)

    if save_values:
        #convert to numpy array and save
        average_giant_fraction = np.array(average_giant_fractions) 
        np.save(f'averages_giant_fractions_if.npy', average_giant_fraction)
    average_giant_fractions = np.mean(average_giant_fractions, axis=0)

    plot = NewPlot()
    plot.add_plot(influence_diff_list, average_giant_fractions)
    plot.add_title('Emergence of Giant Component')
    plot.add_labels('Difference in Influence','Fraction of Giant Component')
    plot.save('emergence.png')

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
        print(f"Simulation {i+1}/{amount_of_runs}")
        giant_fractions = []
        for alpha in alpha_list:
            print(alpha)
            beta = 1 - alpha
            criminality = init_criminality
            for t in range(timesteps):
                print(t)
                if police:
                    criminality = update_grid_withpolice(criminality, education, income, influence_diff, 
                                                         police_threshold, police_effect, redistribution_frac, police_units, alpha=alpha, beta=beta, grid_size=grid_size)[0]
                else:
                    criminality = update_grid_nopolice(criminality, education, income, influence_diff, alpha=alpha, beta=beta)
            giant_fractions.append(giant_component(criminality, percolation_threshold))
        average_giant_fractions.append(giant_fractions)

    if save_values:
        np.save(f'averages_giant_fractions_alpha_fluct.npy', average_giant_fractions)
    average_giant_fractions = np.mean(average_giant_fractions, axis=0)

    plot = NewPlot()
    plot.add_plot(alpha_list, average_giant_fractions)
    plot.add_title('Emergence of Giant Component')
    plot.add_labels('Difference in Influence', 'Fraction of Giant Component')
    plot.save('emergence_alpha.png')

def simulate_average_crime(grid_size=(50, 50), timesteps=100, alpha_range=(.1, .9), influence_diff_range=(-.25, .25), 
                           percolation_threshold=0.5, police_threshold=0.7, police_effect=0.3, redistribution_frac=0.7,
                           police_units=15, police=False, amount_of_runs=10, title='Emergence of Giant Component', save_values=False):
    n = 5
    criminality_over_time = np.zeros((n*n, amount_of_runs, timesteps + 1))
    alphas = np.linspace(alpha_range[0], alpha_range[1], n)
    influence_diffs = np.linspace(influence_diff_range[0], influence_diff_range[1], n)
    iteration_parameters = np.array(list(product(alphas, influence_diffs))).round(3)

    for j in range(amount_of_runs):
        init_criminality = np.random.rand(*grid_size)
        education = np.random.rand(*grid_size)
        income = np.random.rand(*grid_size)
        print(f"Simulation {j+1}/{amount_of_runs}")
        criminality = init_criminality
        for i, (alpha, influence_diff) in enumerate(iteration_parameters):
            criminality_over_time[i, j, 0] = np.mean(init_criminality)
            beta = 1 - alpha
            for t in range(timesteps):
                if police:
                    criminality = update_grid_withpolice(criminality, education, income, influence_diff, 
                                                            police_threshold, police_effect, redistribution_frac, police_units, alpha=alpha, beta=beta, grid_size=grid_size)[0]
                else:
                    criminality = update_grid_nopolice(criminality, education, income, influence_diff, alpha=alpha, beta=beta)
                criminality_over_time[i, j, t+1] = np.mean(criminality)

    plot = NewPlot()
    a_prime = np.inf
    for i, line in enumerate(criminality_over_time):
        a, b = iteration_parameters[i]
        if a != a_prime and i != 0:
            plot.add_title(r'Average criminality $\alpha$: {a}'.format(a=a_prime))
            plot.add_labels('Iteration', 'Average criminality')
            plot.set_logscale(False, True)
            plot.save(f'average_criminality_alpha_{a_prime}.png')
            plot = NewPlot()
        a_prime = a
        min_ci = np.min(line, axis=0)
        max_ci = np.max(line, axis=0)
        plot.add_plot(np.linspace(0, timesteps+1, timesteps + 1), np.mean(line, axis=0), ci_max=max_ci, ci_min=min_ci, label=r"$\alpha$: {a}, id: {b}".format(a=a, b=b))
    plot.add_title(r'Average criminality $\alpha$: {a}'.format(a=a_prime))
    plot.add_labels('Iteration', 'Average criminality')
    plot.set_logscale(False, True)
    plot.save(f'average_criminality_alpha_{a_prime}.png')


# simulate_emergence_if()
# simulate_emergence_a()
simulate_average_crime()