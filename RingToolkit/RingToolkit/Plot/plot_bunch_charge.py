import matplotlib
matplotlib.use('TkAgg')
from matplotlib.ticker import MultipleLocator
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def plot_bunch_charge(data):
    plt.ion()
    plt.rcParams.update({
        "font.size": 45,
        "font.family": "Times New Roman",
        "axes.titlesize": 45,
        "axes.labelsize": 42,
        "xtick.labelsize": 42,
        "ytick.labelsize": 42,
        "legend.fontsize": 38,
        "mathtext.fontset": "stix"
    })
    fig, ax1 = plt.subplots(figsize=(12, 9.0))
    plt.subplots_adjust(left=0.15, right=0.85, bottom=0.165, top=0.95)
    for spine in ax1.spines.values():
        spine.set_linewidth(1)

    x = np.array([item[0] for item in data])
    y_1 = np.array([item[1] for item in data]) * 1e9
    y_2 = np.array([item[2] for item in data]) * 1e4

    ax1.scatter(x, y_1, s=80, color='red', marker='s', label='Horizontal emittance', alpha=1.0)
    ax1.set_xlabel('Bunch charge [nC]')
    ax1.set_ylabel('Horizontal emittance [nm·rad]', color='red')
    ax1.tick_params(axis='y', labelcolor='red', direction="out", length=4, width=1)
    ax1.tick_params(axis='x', labelcolor='black', direction="out", length=4, width=1)
    ax1.set_xlim(0, 3)
    ax1.set_ylim(2.6, 3.4)
    y1_ticks = np.arange(2.6, 3.41, 0.2)
    ax1.set_yticks(y1_ticks)
    ax1.xaxis.set_major_locator(MultipleLocator(0.5))
    ax1.yaxis.set_major_locator(MultipleLocator(0.2))
    ax1.tick_params(axis='both', which='both', pad=10)

    ax1.grid('on')

    ax2 = ax1.twinx()
    ax2.scatter(x, y_2, s=80, color='blue', marker='s', label='Energy spread', alpha=1.0)
    ax2.set_ylabel(r'Energy spread [$\times10^{-4}$]', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue', direction="out", length=4, width=1)
    ax2.set_ylim(4.9, 5.7)
    y2_ticks = np.arange(4.9, 5.71, 0.2)
    ax2.set_yticks(y2_ticks)
    ax2.tick_params(axis='y', pad=10)


    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    all_handles = handles1 + handles2
    all_labels = labels1 + labels2

    legend = ax1.legend(all_handles, all_labels,
                loc='upper left',
                handlelength=1, handletextpad=0.5,
                columnspacing=1, labelspacing=0.3,
                frameon=False,
                ncol=1)
    plt.setp(legend.get_texts(), ha='left')  # ha=horizontal alignment

    # fig.tight_layout()
    plt.show()
    plt.ioff()