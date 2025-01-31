# BY: Bonnie and Cellulair Automata
# FOR: Complex System Simulation
# PURPOSE: To disprove the power law in the system

import powerlaw
import numpy as np
import matplotlib.pyplot as plt
from modules.avelanches import track_avalanches

alpha = 0.5
beta = 1 - alpha
influence_diff = 0.0
threshold = 0.2
side_lengths = [50, 100, 200]  
time_steps = 2000


for side in side_lengths:
    grid_size = (side, side)
    
    criminality = np.random.rand(*grid_size)
    education = np.random.rand(*grid_size)
    income = np.random.rand(*grid_size)
    
    avalanche_sizes = track_avalanches(criminality, education, income, influence_diff, time_steps, threshold)
    
    sizes, counts = np.unique(avalanche_sizes, return_counts=True)
    frequencies = counts / np.sum(counts)

    results = powerlaw.Fit(avalanche_sizes)

    print(f'Alpha for {side}x{side}: {results.alpha}')
    print(f'Xmin for {side}x{side}: {results.xmin}')
    print(f"KS p-value for power law in {side}x{side}: {results.power_law.KS()}")
    plt.plot(sizes, frequencies, 'o-', label=f'{side}x{side}')

plt.yscale('log')
plt.xscale('log')
plt.title('Powerlaw Plot for Different Grid Sizes')
plt.xlabel('Size of Avalanche')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()
