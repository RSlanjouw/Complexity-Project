import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import threading
import time

# Parameters
grid_size = (300, 300)
data_history = []
current_step = 0
play_mode = False  

def calculate_grid(step):
    """Generate bs data"""
    return np.array([
        [np.sin(step / 5 + x / 50 + y / 50) / 2 + 0.5 for x in range(grid_size[0])]
        for y in range(grid_size[1])
    ])

# Plot setup
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.3)
im = ax.imshow(calculate_grid(current_step), cmap="RdYlGn", vmin=0, vmax=1)
ax.set_title(f"Timestep: {current_step}", fontsize=16)

# Slider setup
ax_slider = plt.axes([0.25, 0.15, 0.5, 0.03])
slider = Slider(ax_slider, 'Timestep', 0, 1, valinit=0, valstep=1)

# Functie om de plot te updaten
def update_figure(step):
    global current_step
    current_step = step
    slider.valmax = len(data_history) - 1
    slider.ax.set_xlim(0, slider.valmax)
    slider.set_val(step) 
    if len(data_history) <= step:
        while len(data_history) <= step:  
            data_history.append(calculate_grid(len(data_history)))
    im.set_data(data_history[step])
    ax.set_title(f"Timestep: {step}", fontsize=16)
    fig.canvas.draw_idle()

def on_slider_change(val):
    update_figure(int(val))

slider.on_changed(on_slider_change)

def next_step(event):
    update_figure(current_step + 1)

def previous_step(event):
    if current_step > 0:
        update_figure(current_step - 1)

def toggle_play(event):
    global play_mode
    play_mode = not play_mode
    if play_mode:
        btn_play.label.set_text("Pause")
        threading.Thread(target=auto_play, daemon=True).start()
    else:
        btn_play.label.set_text("Play")

def auto_play():
    global current_step, play_mode
    while play_mode:
        time.sleep(0.5)
        next_step(None)

ax_prev = plt.axes([0.1, 0.05, 0.1, 0.075]) 
ax_next = plt.axes([0.8, 0.05, 0.1, 0.075])
ax_play = plt.axes([0.45, 0.05, 0.1, 0.075])

btn_prev = Button(ax_prev, 'Previous')
btn_next = Button(ax_next, 'Next')
btn_play = Button(ax_play, 'Play')

btn_prev.on_clicked(previous_step)
btn_next.on_clicked(next_step)
btn_play.on_clicked(toggle_play)

plt.show()
