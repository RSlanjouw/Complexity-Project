import numpy as np
from modules.plotter import NewPlot
from modules.avelanches import track_avalanches

side_lenght = [30, 50, 70, 90, 150]
time_steps = 400000
threshold = 0.05
influence_diff = 0
all_sizes = []
all_frequencies = []

for side in side_lenght:
    grid_size = (side, side)
    # Initialize the grids
    criminality = np.random.rand(*grid_size)
    education = np.random.rand(*grid_size)
    income = np.random.rand(*grid_size)

    all_avelanches_sizes = track_avalanches(criminality, education, income, influence_diff, time_steps, threshold, alpha=0.5) # Track all the avelancehs events and their sizes
    sizes, counts = np.unique(all_avelanches_sizes, return_counts=True) # Extract the size and number of events per size
    frequencies = counts / np.sum(counts) # Compute the frequency of each size

    all_sizes.append(sizes)
    all_frequencies.append(frequencies)

    plot = NewPlot()
    plot.add_plot(sizes, frequencies)
    plot.set_logscale(True, True)
    plot.add_title(f'Avalanche Size Distribution on a {side}x{side} grid')
    plot.add_labels('Size of Avalanche', 'Frequency')
    plot.save(f'power_law_{side}')


scaled_sizes = []
scaled_frequencies = []
D = 0.1
tau = 0.8

for sizes, frequencies, side in zip(all_sizes, all_frequencies, side_lenght):
    scaled_sizes.append(sizes / (side ** D))
    scaled_frequencies.append(frequencies * (side ** tau))

plot = NewPlot()
for scaled_size, scaled_frequency, side in zip(scaled_sizes, scaled_frequencies, side_lenght):
    print(scaled_size)
    plot.add_plot(scaled_size, scaled_frequency, label=f'{side}x{side}')

plot.add_title('Data Collapse of Avalanche Size Distribution')
plot.add_labels('Scaled Avelanche Size (s / L^D)', 'Scaled Frequency (P(s) * L^tau)')
plot.set_logscale(True, True)
plot.save("Data Collapse")