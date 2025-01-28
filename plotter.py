import numpy as np
import matplotlib.pyplot as plt

b = np.load("data/test.npy")

class NewPlot():
    def __init__(self):
        plt.style.use("seaborn-v0_8-colorblind")
        plt.rcParams['figure.figsize'] = (3.5,3.5)
        plt.rcParams['figure.dpi'] = 300
        self.fig, self.ax = plt.subplots()
    
    def add_plot(self, x, y, log=False, ci_max = [], ci_min = []):
        if log:
            self.ax.loglog(x, y)
        else:
            self.ax.plot(x, y)
        if not ((len(ci_max)==0) or (len(ci_min) == 0)):
            self.ax.fill_between(x, ci_min, ci_max, alpha=.3)

    def show(self):
        plt.show()

    def add_title(self, title):
        self.ax.set_title(f"{title}")

    def add_labels(self, x, y):
        self.ax.set_xlabel(f"{x}")
        self.ax.set_ylabel(f"{y}")

    def save(self, name):
        plt.savefig(f"figures/{name}")

if __name__ == "__main__":
    plot = NewPlot()
    plot.add_plot(b, b, log=True, ci_max=b+.5, ci_min=b-.5)
    plot.add_plot(b, b+1, log=True)
    plot.add_plot(b, b+2, log=True)
    plot.add_title("title")
    plot.add_labels("x", "y")
    plot.save("test")
    plot.show()