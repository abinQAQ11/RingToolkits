import matplotlib
matplotlib.use('TkAgg')
from matplotlib.ticker import MultipleLocator
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def plot_fma(fma_name: str, mode: str='da', off_mom = 0):
    plt.ion()
    plt.rcParams.update({
        "font.size": 24,
        "font.family": "Times New Roman",
        "axes.titlesize": 24,
        "axes.labelsize": 24,
        "xtick.labelsize": 24,
        "ytick.labelsize": 24,
        "legend.fontsize": 24,
        "mathtext.fontset": "stix"
    })
    fig, ax = plt.subplots(figsize=(8, 7 * 0.618))
    plt.subplots_adjust(left=0.15, right=0.90, bottom=0.20, top=0.95)
    for spine in ax.spines.values():
        spine.set_linewidth(1)

    import pysdds
    fma = pysdds.read(fma_name)

    def da(_fma):
        x = _fma.col('x')[0]
        y = _fma.col('y')[0]
        c = _fma.col('diffusionRate')[0]
        if off_mom:
            p_idx = np.where(np.abs(fma.col('y')[0] - (off_mom / 100)) < 1e-4)[0]
            scatter = ax.scatter(x[p_idx] * 1000, y[p_idx] * 1000, c=c[p_idx], s=30, marker='s', cmap='jet', alpha=1.0,
                             vmax=-3, vmin=-12)
        else:
            scatter = ax.scatter(x * 1000, y * 1000, s=10, c=c, marker='s', cmap='jet', alpha=1.0,
                             vmax=-3, vmin=-12)

        ax.set_xlabel('x [mm]')
        ax.set_ylabel('y [mm]')
        ax.set_xlim(-50, 50)
        ax.set_ylim(0, 20)
        ax.tick_params(axis='x', labelcolor='black', direction="out", length=4, width=1)
        ax.tick_params(axis='y', labelcolor='black', direction="out", length=4, width=1)
        ax.xaxis.set_major_locator(MultipleLocator(20))

        cbar = fig.colorbar(scatter, pad=0.01)
        cbar.ax.tick_params(length=4, width=1)
        cbar.set_label('Diffusion rate')
        cbar.ax.yaxis.set_major_locator(MultipleLocator(2))

    def tune(_fma):
        # plt.subplots_adjust(left=0.12, right=0.94, bottom=0.18, top=0.95)
        x = _fma.col('nux')[0]
        y = _fma.col('nuy')[0]
        c = _fma.col('diffusionRate')[0]
        if off_mom:
            p_idx = np.where(np.abs(fma.col('y')[0] - off_mom / 100) < 1e-4)[0]
            scatter = ax.scatter(x[p_idx], y[p_idx], c=c[p_idx], s=5, marker='s', cmap='jet', alpha=1.0,
                             vmax=-3, vmin=-12)
        else:
            scatter = ax.scatter(x, y, c=c, s=5, marker='s', cmap='jet', alpha=1.0,
                             vmax=-3, vmin=-12)

        ax.set_xlabel(r'$\nu_{x}$')
        ax.set_ylabel(r'$\nu_{y}$')
        ax.tick_params(axis='x', labelcolor='black', direction="out", length=4, width=1)
        ax.tick_params(axis='y', labelcolor='black', direction="out", length=4, width=1)

        cbar = fig.colorbar(scatter, pad=0.01)
        cbar.ax.tick_params(length=4, width=1)
        cbar.set_label('Diffusion rate')
        cbar.ax.yaxis.set_major_locator(MultipleLocator(2))

        plot_resonance_lines(ax, min(x), max(x), min(y), max(y))

    match mode:
        case "da":
            da(fma)
        case "tune":
            tune(fma)

    # plt.savefig("fma.png", dpi=600, bbox_inches="tight")
    plt.show()
    plt.ioff()