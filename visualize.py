import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider
from scipy.ndimage import label
from modules.grid_update import update_grid_nopolice

# Define parameters
grid_size = (300, 300)

criminality = np.random.rand(*grid_size)  # Random criminaliteit



# education = np.full(grid_size, 0.5)  # Vaste waarde voor onderwijs
# income = np.full(grid_size, 0.5)  # Vaste waarde voor inkomen
education = np.random.rand(*grid_size)  # Random onderwijs
income = np.random.rand(*grid_size)  # Random inkomen
# Parameters
timesteps = 500
alpha = 0.50
beta = 1 - alpha
influence_diff = 0.0

# Initialize figure
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)  # Ruimte maken voor slider

# Criminality heatmap
im = ax.imshow(criminality, cmap='hot', interpolation='nearest')
plt.colorbar(im, label='Criminality Level')
plt.title('Criminality Evolution')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# Slider voor handmatige controle
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # Positie slider (x, y, breedte, hoogte)
slider = Slider(ax_slider, 'Frame', 0, timesteps - 1, valinit=0, valstep=1)

# Vooraf criminaliteitsdata genereren voor alle frames
frames = []
current_criminality = np.copy(criminality)
for _ in range(timesteps):
    current_criminality = update_grid_nopolice(current_criminality, education, income, influence_diff, alpha=alpha, beta=beta)
    frames.append(np.copy(current_criminality))

# Update functie voor slider
def update(val):
    frame = int(slider.val)
    im.set_array(frames[frame])  # Toon criminaliteitstoestand van geselecteerd frame
    fig.canvas.draw_idle()

slider.on_changed(update)  # Koppel de slider aan de update-functie

plt.show()
