import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle 
from matplotlib import cycler

b = np.load("data/test.npy")

class NewPlot():
    def __init__(self):
        plt.style.use("seaborn-v0_8-colorblind")
        plt.rcParams['axes.prop_cycle'] = cycler('color',["#0d0786", "#facf28", "#cf4e72", "#ec7c4c", "#9b169f"])
        plt.rcParams['legend.fontsize'] = 8
        plt.rcParams['figure.figsize'] = (3.5,3.5)
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['lines.linewidth'] = 2
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 9
        plt.rcParams['axes.prop_cycle']
        self.fig, self.ax = plt.subplots()

    def set_logscale(self, x=False, y=False):
        if x:
            self.ax.set_xscale("log")
        else:
            self.ax.set_xscale("linear")
        if y:
            self.ax.set_yscale("log")
        else:
            self.ax.set_yscale("linear")
    
    def add_plot(self, x, y, ci_max = [], ci_min = [], label=""):
        self.ax.plot(x, y, label=f"{label}")
        if label:
            plt.legend()
        if not ((len(ci_max)==0) or (len(ci_min) == 0)):
            self.ax.fill_between(x, ci_min, ci_max, alpha=.3)

    def show(self):
        plt.show()

    def add_title(self, title):
        self.ax.set_title(f"{title}")

    def add_labels(self, x="", y=""):
        self.ax.set_xlabel(f"{x}")
        self.ax.set_ylabel(f"{y}")

    def set_ticks(self, xticks=[], yticks=[]):
        if not len(xticks) == 0:
            self.ax.set_xticks(xticks)
        if not len(yticks) == 0:
            self.ax.set_yticks(yticks)

    def set_limits(self, xlim= [], ylim=[]):
        if not len(xlim) == 0:
            self.ax.set_xlim(xlim)
        if not len(ylim) == 0:
            self.ax.set_ylim(ylim)


    def save(self, name):
        plt.tight_layout()
        plt.savefig(f"figs/{name}")

if __name__ == "__main__":
    plot = NewPlot()
    plot.set_logscale(False, True)
    plot.add_plot(b, b,  ci_max=b+.5, ci_min=b-.5)
    plot.add_plot(b, b+1)
    plot.add_plot(b, b+2)
    plot.set_limits([0,10], [1,7])
    plot.set_ticks([1,2,4,5], yticks=[1,2,5])
    plot.add_title("title")
    plot.add_labels("x", "y")
    plot.save("test")
    plot.show()