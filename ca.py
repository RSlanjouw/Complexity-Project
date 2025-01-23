import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from perlin_numpy import generate_perlin_noise_2d


class CellularAutomaton:
    def __init__(self, gridDimensions, k, useInertia):
        rng = np.random.default_rng()
        noise = generate_perlin_noise_2d(gridDimensions, (2, 2))
        self.useInertia = useInertia
        self.inertiaMap = (generate_perlin_noise_2d(gridDimensions, (2, 2)) + 1)/2
        self.grid = (noise + 1)/2
        self.k = k

    def update_grid(self):
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                localGrid = self.grid[max(0, i-1):min(i+2, self.grid.shape[0]),
                                      max(0, j-1):min(j+2, self.grid.shape[1])]
                differenceTerm = np.sum(localGrid - self.grid[i, j]) * self.k / (localGrid.size - 1)
                if self.useInertia:
                    if differenceTerm > 0:
                        self.grid[i, j] += differenceTerm * self.inertiaMap[i, j]**2
                    else:
                        self.grid[i, j] += differenceTerm / 4
                else: self.grid[i, j] += differenceTerm
                self.grid[i, j] = max(0, min(self.grid[i, j], 1))

    def draw_image(self, iter):
        self.update_grid()
        self.colors.set_array(self.grid)

    def iterate(self, n):
        fig, ax = plt.subplots()
        self.colors = ax.pcolormesh(self.grid, vmin=0, vmax=1)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(self.colors)
        animation = anim.FuncAnimation(fig, self.draw_image, interval=100//6, frames=300, repeat=False)
        # animation.save("trippy.gif")
        plt.show()

if __name__ == "__main__":
    ca = CellularAutomaton((128, 128), 2, False)
    ca.update_grid()
    ca.iterate(1)
