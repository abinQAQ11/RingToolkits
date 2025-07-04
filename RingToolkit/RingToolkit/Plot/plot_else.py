import re
import random
import mplcursors
import matplotlib
matplotlib.use('TkAgg')
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def show_relation(obj, data):
    plt.ion()

    emit = np.array([item[0] for item in obj])
    f3_rms = np.array([item[1] for item in obj])
    value = np.array([item for item in data])

    fig, ax = plt.subplots()
    scatter1 = ax.scatter(emit, f3_rms, c=value, s=30, cmap="jet", alpha=1.0)

    ax.set_xlabel(r'$\epsilon_{x}\ [nm]$', fontsize=25)
    ax.set_ylabel(r'$f_{3,rms}$', fontsize=25)
    ax.tick_params(axis='y', labelcolor='black', labelsize=30)
    ax.tick_params(axis='x', labelcolor='black', labelsize=30)

    cbar = plt.colorbar(scatter1, pad=0.01)
    cbar.ax.tick_params(labelsize=20)
    # cbar.set_label(r"$\eta_X$ at mid", fontsize=25)

    cursor = mplcursors.cursor(scatter1, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        sel.annotation.set_text(f'emit={emit[idx]:.2f}, f3_rms={f3_rms[idx]:.2f}, value={value[idx]}')
        sel.annotation.get_bbox_patch().set(fc="lightblue", alpha=0.9)

    plt.show()
    plt.ioff()
# ----------------------------------------------------------------------------------------------------------------------
def show_constraint(file_path, pat: str="bound", n_cst: int=10):
    values = []
    pattern = None
    match pat:
        case "bound":
            pattern = r"bound=\[(.*?)\],"
        case "obj":
            pattern = r"obj=\[(.*?)\],"
        case "x":
            pattern = r"x=\[(.*?)\]"

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            bound_match = re.search(pattern, line)
            if bound_match:
                bound_data = bound_match.group(1)
                values.append([float(x) for x in bound_data.split(", ")])

    count = np.array([ct for ct in range(len(values))])
    colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(n_cst)]
    plt.ion()
    fig, ax = plt.subplots()
    for i in range(n_cst):
        val = np.array([item[i] for item in values])
        ax.scatter(count, val, c=colors[i], s=10, alpha=1.0,label=f"{i}")

    # ax.set_ylim(0, 10)
    ax.set_xlabel('solutions', fontsize=25)
    ax.set_ylabel("values", fontsize=25)
    ax.tick_params(axis='y', labelcolor='black', labelsize=25)
    ax.tick_params(axis='x', labelcolor='black', labelsize=25)
    ax.legend(fontsize=30, ncol=2, scatterpoints=1, markerscale=2)
    plt.show()
    plt.ioff()