import numpy as np
import matplotlib.pyplot as plt

from modules.emergence import simulate_emergence

# For robustness, we analyze the emergence of the giant component for different grid sizes

# Define parameters common to every grid size and a list of sizes
all_y_nop = []
all_y_withp = []
all_err_nop = []
all_err_withp = []
side_size = [30, 50, 70, 90]
alpha = 0.3
beta = 1 - alpha
timesteps = 70
percolation_threshold = 0.5
police_threshold = 0.6
police_effect = 0.5
redistribution_frac = 0.3
police_units = 70
num_simulation = 30
influence_diff_list = np.linspace(-beta / 2, beta / 2, 15)

for L in side_size: # Plot the emergence curve for different grids of size LxL

    avg_nop, avg_withp, err_nop, err_withp = simulate_emergence(grid_size=(L, L), timesteps=timesteps, alpha=alpha, 
                       percolation_threshold=percolation_threshold, police_threshold=police_threshold, police_effect=police_effect, 
                       redistribution_frac=redistribution_frac, police_units=police_units, num_simulation=num_simulation, title=f'Emergence_grid_{L}')
    
    all_y_nop.append(avg_nop)
    all_y_withp.append(avg_withp)
    all_err_nop.append(err_nop)
    all_err_withp.append(err_withp)

handles, labels = [], []

for ind in range(len(side_size)): 
    line1, = plt.plot(influence_diff_list, all_y_nop[ind], label=f'No Police', color='b')
    plt.fill_between(influence_diff_list, all_y_nop[ind] - all_err_nop[ind], all_y_nop[ind] + all_err_nop[ind], color = 'b', alpha = 0.2)
    line2, = plt.plot(influence_diff_list, all_y_withp[ind], label=f'With Police', color='r')
    plt.fill_between(influence_diff_list, all_y_withp[ind] - all_err_withp[ind], all_y_withp[ind] + all_err_withp[ind], color = 'r', alpha = 0.2)

    if ind == 0:
        handles.extend([line1, line2])
        labels.extend(["No Police", "With Police"])

plt.xlabel('Difference in Influence')
plt.ylabel('Fraction of Giant Component')
plt.title('Data Collapse for Different Grid Sizes')
plt.legend(handles, labels)
plt.subplots_adjust(bottom=0.28)
plt.figtext(0.5, 0.01, f'Emergence of the Giant component in different size grids (for reference, the side of each grid is {side_size} going from right to left, for both colors). Measurements are taken after {timesteps} timesteps and are averaged out {num_simulation} runs. The colored area around the line represents the 95% CI. Alpha is set to {alpha}; the percolation threshold to {percolation_threshold}; the police threshold (to take action) is set to {police_threshold}; the police effect to {police_effect} of which a fraction of {redistribution_frac} is redistributed to neighbours; the number of police units is {police_units}.',
                            wrap=True, horizontalalignment='center', fontsize=9)
plt.savefig('figs/different_grid_size_emergence.png')
plt.show()