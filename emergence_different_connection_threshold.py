import numpy as np
import matplotlib.pyplot as plt
from plotter import NewPlot

from modules.emergence import simulate_emergence

# For robustness, we analyze the emergence of the giant component for different connection thresholds

# Define parameters common to every grid size and a list of sizes
all_y_nop = []
all_err_nop = []
grid_size = (50, 50)
alpha = 0.3
beta = 1 - alpha
timesteps = 200
connection_threshold_list = [0.3, 0.5, 0.7, 0.9]
police_threshold = 0.6
police_effect = 0.5
redistribution_frac = 0.3
police_units = 70
num_simulation = 30
influence_diff_list = np.linspace(-beta / 2, beta / 2, 15)
police = False
save_fig = False
onlypolice = False

for connection_threshold in connection_threshold_list: # Plot the emergence curve for different grids of size LxL

    avg_nop, avg_withp, err_nop, err_withp = simulate_emergence(grid_size=grid_size, timesteps=timesteps, alpha=alpha, 
                       connection_threshold=connection_threshold, police_threshold=police_threshold, police_effect=police_effect, 
                       redistribution_frac=redistribution_frac, police_units=police_units, num_simulation=num_simulation, title=f'Emergence_perc_thr_{connection_threshold}', police=police, onlypolice=onlypolice, savefig=save_fig)
    
    all_y_nop.append(avg_nop)
    all_err_nop.append(err_nop)

colors = ['b', 'g', 'r', 'c']
plot = NewPlot()
for ind, thr in enumerate(connection_threshold_list): 
    plot.add_plot(influence_diff_list, all_y_nop[ind], label=f'Connect. thr. = {thr}', ci_min=all_y_nop[ind] - all_err_nop[ind], ci_max=all_y_nop[ind] + all_err_nop[ind])

plot.add_labels('Difference in Influence', 'Fraction of Giant Component')
plot.add_title('Emergence of Giant Component for Different Connection Thresholds')
# plt.legend()
# plt.subplots_adjust(bottom=0.28)
# plt.figtext(0.5, 0.01, f'Emergence of the Giant component in a {grid_size[0]}x{grid_size[1]} grid. Measurements are taken after {timesteps} timesteps and are averaged out {num_simulation} runs. The colored area around the line represents the 95% CI. Alpha is set to {alpha}; the police threshold (to take action) is set to {police_threshold}; the police effect to {police_effect} of which a fraction of {redistribution_frac} is redistributed to neighbours; the number of police units is {police_units}.',
#             wrap=True, horizontalalignment='center', fontsize=9)
plot.save('different_connection_thr.png')
# plt.show()