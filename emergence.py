import numpy as np
import matplotlib.pyplot as plt

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
        print(f"Simulation {i+1}/30")
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

    plt.plot(influence_diff_list, average_giant_fractions)
    plt.title('Emergence of Giant Component')
    plt.xlabel('Difference in Influence')
    plt.ylabel('Fraction of Giant Component')
    plt.savefig('figs/emergence.png')

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

    plt.plot(alpha_list, average_giant_fractions)
    plt.title('Emergence of Giant Component')
    plt.xlabel('Difference in Influence')
    plt.ylabel('Fraction of Giant Component')
    plt.savefig('figs/emergence.png')



simulate_emergence_if()