# BY: Bonnie and Cellulair Automata
# FOR: Complex System Simulation
# Investigate the emergence of a GC by varying grid sizes

import numpy as np
from modules.plotter import NewPlot

from modules.emergence import simulate_emergence


# Define parameters common to every grid size and a list of sizes
all_y_nop = []
all_y_withp = []
all_err_nop = []
all_err_withp = []
side_size = [30, 50, 70, 90]
alpha = 0.3
beta = 1 - alpha
timesteps = 70
connection_threshold = 0.7
police_threshold = 0.6
police_effect = 0.55
redistribution_frac = 0.1
police_units = 70
num_simulation = 10
influence_diff_list = np.linspace(-beta / 2, beta / 2, 15)

for L in side_size: # Plot the emergence curve for different grids of size LxL
    # Simulate emergence
    avg_nop, avg_withp, err_nop, err_withp = simulate_emergence(grid_size=(L, L), timesteps=timesteps, alpha=alpha, 
                       connection_threshold=connection_threshold, police_threshold=police_threshold, police_effect=police_effect, 
                       redistribution_frac=redistribution_frac, police_units=police_units, num_simulation=num_simulation, title=f'Emergence_grid_{L}')
    
    all_y_nop.append(avg_nop)
    all_y_withp.append(avg_withp)
    all_err_nop.append(err_nop)
    all_err_withp.append(err_withp)

handles, labels = [], []
plot = NewPlot()
for ind in range(len(side_size)): 
    line1, = plot.add_plot(influence_diff_list, all_y_nop[ind], ci_min=all_y_nop[ind] - all_err_nop[ind], ci_max=all_y_nop[ind] + all_err_nop[ind], color="#0d0786")
    line2, = plot.add_plot(influence_diff_list, all_y_withp[ind], ci_min=all_y_withp[ind] - all_err_withp[ind], ci_max=all_y_withp[ind] + all_err_withp[ind], color='#facf28')
    if ind == 0:
        handles.extend([line1, line2])
        labels.extend(["No Police", "With Police"])

plot.add_labels('Difference in Influence', 'Fraction of Giant Component')
plot.add_title('Joint Plot for Different Grid Sizes')
plot.custom_legend(handles, labels)
plot.save('different_grid_size_emergence.png')