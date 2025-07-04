import matplotlib
matplotlib.use('TkAgg')
from .base_plot import *
from matplotlib.ticker import MultipleLocator
# ----------------------------------------------------------------------------------------------------------------------
def plot_lattice(lattice, high_1=25, high_2=0.5, cell_or_ring: str = "cell"):
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
    fig, ax1 = plt.subplots(figsize=(12, 12 * 0.618))
    plt.subplots_adjust(left=0.14, right=0.86, bottom=0.19, top=0.95)
    for spine in ax1.spines.values():
        spine.set_linewidth(1)

    data = None
    if cell_or_ring == "cell":
        data = lattice.twiss
    elif cell_or_ring == "ring":
        data = lattice.twiss * lattice.periodicity

    s = np.array([item[0] for item in data])
    beta_x = np.array([item[1]['Beta_X'] for item in data])
    beta_y = np.array([item[1]['Beta_Y'] for item in data])
    disp_x = np.array([item[1]['Disp_X'] for item in data])

    ax1.plot(s, beta_x, color='blue', label=r'$\beta_x$', linewidth=5, alpha=1.0)
    ax1.plot(s, beta_y, color='red', label=r'$\beta_y$', linewidth=5, alpha=1.0)

    ax1.set_xlabel('s [m]')
    ax1.set_ylabel('Beta functions [m]', labelpad=10, color='black')
    ax1.tick_params(axis='y', labelcolor='black', direction="out", length=6, width=1)
    ax1.tick_params(axis='x', labelcolor='black', direction="out", length=6, width=1)
    # high_1 = math.ceil(max(max(beta_x), max(beta_y), max(disp_x)*100) / 10) * 10
    high_1 = high_1
    height_1 = high_1 / 20
    ax1.set_xlim(min(s), max(s))
    ax1.set_ylim(-height_1, high_1)
    # ax1.xaxis.set_major_locator(MultipleLocator(4))
    ax1.yaxis.set_major_locator(MultipleLocator(5))

    ax2 = ax1.twinx()
    ax2.plot(s, disp_x, color='green', label=r'$\eta_x$', linewidth=5, alpha=1.0)
    ax2.set_ylabel('Dispersion [m]', labelpad=10, color='black')
    ax2.tick_params(axis='y', labelcolor='black', direction="out", length=6, width=1)
    # high_2 = math.ceil(max(max(beta_x), max(beta_y), max(disp_x*100)) / 10) * 0.1
    high_2 = high_2
    height_2 = high_2 / 20
    ax2.set_ylim(-height_2, high_2)
    ax2.yaxis.set_major_locator(MultipleLocator(0.1))
    if cell_or_ring == "cell":
        magnet(ax1, height_1, lattice.cell)
    elif cell_or_ring == "ring":
        magnet(ax1, height_1, lattice.ring)

    ax1.legend(ncol=2, loc='upper left', frameon=False)
    ax2.legend(loc='upper right', frameon=False)

    # fig.suptitle(r'$\beta_x$, $\beta_y$ and Disp_x', fontsize=20)
    # plt.savefig("lattice.png", dpi=600, bbox_inches="tight")
    plt.show()
    plt.ioff()