import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation, PillowWriter
from modules.grid_update import update_grid_nopolice

# Define parameters
grid_size = (100, 100)
criminality = np.random.rand(*grid_size)  # Random criminaliteit
education = np.random.rand(*grid_size)  # Random onderwijs
income = np.random.rand(*grid_size)  # Random inkomen

# Parameters
timesteps = 400
alpha = 0.5
beta = 1 - alpha
influence_diff = 0

frames = []
current_criminality = np.copy(criminality)
for _ in range(timesteps):
    current_criminality = update_grid_nopolice(
        current_criminality, education, income, influence_diff, alpha=alpha, beta=beta
    )
    frames.append(np.copy(current_criminality))

def show_up_and_down(frames):
    print(frames[0][0])

    abs_dif = []
    for i in range(1, len(frames)):
        print(i)
        positive_changes_mask = frames[i] > frames[i - 1]
        negative_changes_mask = frames[i] < frames[i - 1]
        positive_absolute_changes_with_mask = np.abs(frames[i] - frames[i - 1]) * positive_changes_mask
        negative_absolute_changes_with_mask = np.abs(frames[i] - frames[i - 1]) * negative_changes_mask
        positive = np.sum(positive_absolute_changes_with_mask)
        negative = np.sum(negative_absolute_changes_with_mask)
        print(f"Positive changes: {positive}, Negative changes: {negative}")
        abs_dif.append(positive - negative)

    return abs_dif  

abs_dif = show_up_and_down(frames)
plt.plot(abs_dif, label="Absolute difference in the system")
plt.xlabel("Time")
plt.ylabel("Absolute difference")
plt.grid()
plt.show()