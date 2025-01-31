# Investigate the emergence of a GC by varying the amount of police
import numpy as np
from modules.plotter import NewPlot
from modules.emergence import simulate_emergence

# To explain the variance in the experiment including police, 
# we plot the emergence of the giant component for different amounts of police units

# Define parameters common to every simulation and a list of police units and grid sizes
all_y_withp = []
all_err_nop = []
all_err_withp = []
alpha = 0.3
beta = 1 - alpha
timesteps = 70
connection_threshold = 0.7
police_threshold = 0.6
police_effect = 0.55
redistribution_frac = 0.1
police_units = [70, 200, 400, 600]
side_size = [30, 50, 70, 90]
num_simulation = 15
influence_diff_list = np.linspace(-beta / 2, beta / 2, 15)

for ind, units in enumerate(police_units):
    # Run emergence simulation
    onlypolice = False if ind == 0 else True

    avg_nop, avg_withp, err_nop, err_withp = simulate_emergence(grid_size=(side_size[ind], side_size[ind]), timesteps=timesteps, alpha=alpha, 
                       connection_threshold=connection_threshold, police_threshold=police_threshold, police_effect=police_effect, 
                       redistribution_frac=redistribution_frac, police_units=units, num_simulation=num_simulation, title=f'Emergence_grid_units_{units}', police=True, onlypolice=onlypolice, savefig=False)
    
    if ind == 0:
        plot_avg_nop, plot_err_nop = avg_nop, err_nop
    all_y_withp.append(avg_withp)
    all_err_withp.append(err_withp)

handles, labels = [], []
plot = NewPlot()
for ind in range(len(police_units)):
    if ind == 0:
        line1, = plot.add_plot(influence_diff_list, plot_avg_nop, ci_min=plot_avg_nop - plot_err_nop, ci_max=plot_avg_nop + plot_err_nop, color="#0d0786")
    line2, = plot.add_plot(influence_diff_list, all_y_withp[ind], ci_min=all_y_withp[ind] - all_err_withp[ind], ci_max=all_y_withp[ind] + all_err_withp[ind], label=f'With Police', color='#facf28')
    if ind == 0:
        handles.extend([line1, line2])
        labels.extend(["No Police", "With Police"])

plot.add_labels('Difference in Influence', 'Fraction of Giant Component')
plot.add_title('Joint Plot for Different Amounts of Police Units')
plot.custom_legend(handles, labels)
plot.save('different_police_amounts_emergence.png')