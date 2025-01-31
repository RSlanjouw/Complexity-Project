# BY: Bonnie and Cellulair Automata
# FOR: Complex System Simulation
# PURPOSE: To calculate the transient length of the system

import numpy as np
from modules.grid_update import update_grid_nopolice

criminality =  np.random.rand(300,300)
education = np.random.rand(300,300)
income = np.random.rand(300,300)

timesteps = 5000
influence_diff = 0.0 
alpha = 0.5
beta = 1 - alpha
frames = []
current_criminality = np.copy(criminality)
for _ in range(timesteps):
    current_criminality = update_grid_nopolice(current_criminality, education, income, influence_diff, alpha=alpha, beta=beta)
    frames.append(np.copy(current_criminality))


transient_lengths = []
list_of_random_pixels = np.random.randint(0, 300, size=(10, 2))
print(list_of_random_pixels)

def get_list_of_values_in_timesteps(pixel):
    list_of_values = []
    for frame in frames:
        list_of_values.append(frame[pixel[0], pixel[1]])
    return list_of_values


def find_cycle(seq):
    seen = {}
    for i, num in enumerate(seq):
        if num in seen:
            cycle_start = seen[num]
            cycle = seq[cycle_start:i]
            
            if np.allclose(seq[cycle_start:cycle_start + len(cycle)], seq[cycle_start + len(cycle):cycle_start + 2 * len(cycle)], atol=1e-2):
                return cycle_start, len(cycle)
    return len(seq), 0

for pixel in list_of_random_pixels:
    list_of_values = get_list_of_values_in_timesteps(pixel)
    print(list_of_values[-80:])
    cycle_start, cycle_length = find_cycle(list_of_values)
    transient_lengths.append(cycle_start)

print("Transient Lengths:", transient_lengths)
