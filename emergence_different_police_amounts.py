import numpy as np
import matplotlib.pyplot as plt

from modules.emergence import simulate_emergence

# To explain the variance in the red line, we plot the emergence of the giant component for different amounts of police units

# Define parameters common to every simulation and a list of police units and grid sizes
all_y_withp = []
all_err_nop = []
all_err_withp = []
alpha = 0.3
beta = 1 - alpha
timesteps = 70
percolation_threshold = 0.5
police_threshold = 0.7
police_effect = 0.3 
redistribution_frac = 0.7
police_units = [30, 100, 200, 300]
side_size = [30, 50, 70, 90]
num_simulation = 30
influence_diff_list = np.linspace(-beta / 2, beta / 2, 15)

for ind, units in enumerate(police_units):

    onlypolice = False if ind == 0 else True

    avg_nop, avg_withp, err_nop, err_withp = simulate_emergence(grid_size=(side_size[ind], side_size[ind]), timesteps=timesteps, alpha=alpha, 
                       percolation_threshold=percolation_threshold, police_threshold=police_threshold, police_effect=police_effect, 
                       redistribution_frac=redistribution_frac, police_units=units, num_simulation=num_simulation, title=f'Emergence_grid_units_{units}', police=True, onlypolice=onlypolice, savefig=False)
    
    if ind == 0:
        plot_avg_nop, plot_err_nop = avg_nop, err_nop
    all_y_withp.append(avg_withp)
    all_err_withp.append(err_withp)

handles, labels = [], []

for ind in range(len(police_units)):

    if ind == 0:
        line1, = plt.plot(influence_diff_list, plot_avg_nop, label=f'No Police', color='b')
        plt.fill_between(influence_diff_list, plot_avg_nop - plot_err_nop, plot_avg_nop + plot_err_nop, color = 'b', alpha = 0.2)
    line2, = plt.plot(influence_diff_list, all_y_withp[ind], label=f'With Police', color='r')
    plt.fill_between(influence_diff_list, all_y_withp[ind] - all_err_withp[ind], all_y_withp[ind] + all_err_withp[ind], color = 'r', alpha = 0.2)

    if ind == 0:
        handles.extend([line1, line2])
        labels.extend(["No Police", "With Police"])

plt.xlabel('Difference in Influence')
plt.ylabel('Fraction of Giant Component')
plt.title('Data Collapse for Different Amounts of Police Units')
plt.legend(handles, labels)
plt.subplots_adjust(bottom=0.28)
plt.figtext(0.5, 0.01, f'Emergence of the Giant component in a {side_size[0]}x{side_size[0]} grid (for the blue line). The cases with police are simulated on grids with side lentgh of {police_units} (red lines). Measurements are taken after {timesteps} timesteps and are averaged out {num_simulation} runs. The colored area around the line represents the 95% CI. Alpha is set to {alpha}; the percolation threshold to {percolation_threshold}; the police threshold (to take action) is set to {police_threshold}; the police effect to {police_effect} of which a fraction of {redistribution_frac} is redistributed to neighbours; the number of police units is {police_units}.',
            wrap=True, horizontalalignment='center', fontsize=9)
plt.savefig('figs/different_police_amounts_emergence.png')
plt.show()