import mplcursors
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.ticker import MultipleLocator
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
"""step by step"""
def show_f3(data1, data2=None):
    plt.ion()
    count = np.array([ct for ct in range(len(data1))])
    f3_rms = np.array([item for item in data1])
    pair = np.array([item for item in data2])

    fig, ax = plt.subplots()
    scatter = ax.scatter(count, f3_rms, c=pair, s=20, cmap='jet', alpha=1.0)
    # scatter = ax.scatter(count, f3_rms, c='blue', s=20, alpha=1.0)
    ax.set_xlabel('step', fontsize=25)
    ax.set_ylabel("f3_rms", fontsize=30)
    ax.tick_params(axis='y', labelcolor='black', labelsize=30)
    ax.tick_params(axis='x', labelcolor='black', labelsize=30)
    ax.grid('on')

    cbar = plt.colorbar(scatter, pad=0.01)
    cbar.ax.tick_params(labelsize=20)
    cbar.set_label("pair", fontsize=25)

    fig.tight_layout()
    plt.show()
    plt.ioff()

def show_chroamt(data1, data2):
    plt.ion()
    cx1 = np.array([item for item in data1])
    cy1 = np.array([item for item in data2])
    count = np.array([ct for ct in range(len(data1))])

    fig, ax = plt.subplots()
    scatter = ax.scatter(cx1, cy1, color='blue', s=10, alpha=1.0)
    ax.set_xlabel(r'$\xi_x$', fontsize=25)
    ax.set_ylabel(r"$\xi_y$", fontsize=25)
    ax.tick_params(axis='y', labelcolor='black', labelsize=30)
    ax.tick_params(axis='x', labelcolor='black', labelsize=30)
    ax.grid('on')

    cursor = mplcursors.cursor(scatter, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        sel.annotation.set_text(f"cx1={cx1[idx]:.4f}\n"
                                f"cy1={cy1[idx]:.4f}\n"
                                f"step={count[idx]}")
        sel.annotation.get_bbox_patch().set(fc="lightblue", alpha=0.9)

    fig.tight_layout()
    plt.show()
    plt.ioff()

def show_num(data1):
    plt.ion()
    count = np.array([ct for ct in range(len(data1))])
    pair = np.array([item for item in data1])

    fig, ax = plt.subplots()
    ax.scatter(count, pair, c='red', s=20, alpha=1.0)
    ax.set_xlabel('step', fontsize=25)
    ax.set_ylabel("pair", fontsize=30)
    ax.tick_params(axis='y', labelcolor='black', labelsize=30)
    ax.tick_params(axis='x', labelcolor='black', labelsize=30)
    ax.grid('on')
    ax.yaxis.set_major_locator(MultipleLocator(1))

    fig.tight_layout()
    plt.show()
    plt.ioff()