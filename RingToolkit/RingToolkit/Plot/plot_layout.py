import matplotlib
matplotlib.use('TkAgg')
from .base_plot import *
from matplotlib.ticker import MultipleLocator
# ----------------------------------------------------------------------------------------------------------------------
def plot_layout(lattice, cell_or_ring: str = "cell"):
    plt.ion()
    plt.rcParams.update({
        "font.size": 45,
        "font.family": "Times New Roman",
        "axes.titlesize": 45,
        "axes.labelsize": 45,
        "xtick.labelsize": 42,
        "ytick.labelsize": 42,
        "legend.fontsize": 38,
        "mathtext.fontset": "stix"
    })
    fig, ax = plt.subplots(figsize=(21, 3))
    plt.subplots_adjust(left=0.14, right=0.86, bottom=0.19, top=0.95)
    for spine in ax.spines.values():
        spine.set_linewidth(1)

    ax.set_ylim(-1.1, 0.0)
    ax.set_xlabel("s [m]")
    ax.set_ylabel(f"{lattice.name}")
    ax.xaxis.set_major_locator(MultipleLocator(int(lattice.cell_length/4)))
    ax.tick_params(axis='x', labelcolor='black', direction="out", length=6, width=1)
    ax.tick_params(axis='y', which='both', labelleft=False)

    if cell_or_ring == "cell":
        ax.set_xlim(0.0, lattice.cell_length)
        magnet(ax, 1, lattice.cell)
    elif cell_or_ring == "ring":
        ax.set_xlim(0.0, lattice.circumference)
        magnet(ax, 1, lattice.ring)

    plt.show()
    plt.ioff()