import matplotlib
matplotlib.use('TkAgg')
# from matplotlib.ticker import MultipleLocator
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def plot_tune(lattice):
    plt.ion()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 50

    fig, ax = plt.subplots(figsize=(12, 9))

    x0 = np.array([lattice.tune_x])
    y0 = np.array([lattice.tune_y])
    ax.scatter(x0, y0, color='red', s=150, marker='^')

    x_min = math.floor(x0)
    x_max = math.ceil(x0)
    y_min = math.floor(y0)
    y_max = math.ceil(y0)

    ax.set_xlabel(r'$\nu_{x}$')
    ax.set_ylabel(r'$\nu_{y}$')
    ax.tick_params(axis='both')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    plot_resonance_lines(ax, x_min, x_max, y_min, y_max)

    for spine in ax.spines.values():
        spine.set_linewidth(3)

    fig.tight_layout()
    plt.show()
    plt.ioff()