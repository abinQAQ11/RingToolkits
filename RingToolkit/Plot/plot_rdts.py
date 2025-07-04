import matplotlib
matplotlib.use('TkAgg')
from matplotlib.ticker import MultipleLocator
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def plot_rdts(lattice):
    plt.ion()
    plt.rcParams.update({
        "font.size": 45,
        "font.family": "Times New Roman",
        "axes.titlesize": 45,
        "axes.labelsize": 42,
        "xtick.labelsize": 42,
        "ytick.labelsize": 42,
        "legend.fontsize": 34,
        "mathtext.fontset": "stix"
    })
    fig, ax = plt.subplots(figsize=(12, 12 * 0.618))
    plt.subplots_adjust(left=0.14, right=0.98, bottom=0.18, top=0.97)
    for spine in ax.spines.values():
        spine.set_linewidth(1)

    data = lattice.rdts

    s = np.array([item[0] for item in data["h_21000"]])
    f_21000 = np.array([item[1]['C_t'] for item in data['h_21000']])
    f_30000 = np.array([item[1]['C_t'] for item in data['h_30000']])
    f_10110 = np.array([item[1]['C_t'] for item in data['h_10110']])
    f_10020 = np.array([item[1]['C_t'] for item in data['h_10020']])
    f_10200 = np.array([item[1]['C_t'] for item in data['h_10200']])

    ax.plot(s, f_21000, color='green', linewidth=4, label=r'$f_{21000}$')
    ax.plot(s, f_30000, color='blue', linewidth=4, label=r'$f_{30000}$')
    ax.plot(s, f_10110, color='purple', linewidth=4, label=r'$f_{10110}$')
    ax.plot(s, f_10020, color='red', linewidth=4, label=r'$f_{10020}$')
    ax.plot(s, f_10200, color='cyan', linewidth=4, label=r'$f_{10200}$')

    ax.set_xlabel('s [m]')
    ax.set_ylabel(r'3rd-order RDTs [$\text{m}^{-1/2}$]', color='black', labelpad=10)
    ax.tick_params(axis='y', labelcolor='black', direction="out", length=4, width=1)
    ax.tick_params(axis='x', labelcolor='black', direction="out", length=4, width=1)
    high = max(max(f_21000), max(f_30000), max(f_10110), max(f_10020), max(f_10200))
    height = high / 20
    ax.set_ylim(-height, high * 1.45)
    ax.set_xlim(0, max(s))
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(2))

    magnet(ax, height, lattice.cell)

    ax.legend(ncol=3, loc='upper center', frameon=False)
    # plt.savefig("rdts.png", dpi=600, bbox_inches="tight")
    plt.show()
    plt.ioff()