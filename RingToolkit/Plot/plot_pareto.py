import mplcursors
import matplotlib
matplotlib.use('TkAgg')
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def plot_pareto(data, x: float = 2.821083468527769,
                      y: float = 11.040034362932325):
    plt.ion()
    emit = np.array([item[0] for item in data])
    f3_rms = np.array([item[1] for item in data])
    s_num = np.array([i + 1 for i in range(len(data))])

    e0 = np.array([x])
    f0 = np.array([y])

    fig, ax = plt.subplots()
    scatter_1 = ax.scatter(emit, f3_rms, color='blue')

    ax.axhline(y=f0.item(), color='gray', linestyle='--')
    ax.axvline(x=e0.item(), color='gray', linestyle='--')
    ax.scatter(e0, f0, color='red')

    ax.set_xlabel(r'$\epsilon_{x}\ [nm]$', fontsize=25)
    ax.set_ylabel(r'$f_{3,rms}$', fontsize=30)
    ax.tick_params(axis='y', labelcolor='black', labelsize=30)
    ax.tick_params(axis='x', labelcolor='black', labelsize=30)

    cursor = mplcursors.cursor(scatter_1, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        sel.annotation.set_text(f'emit={emit[idx]:.2f}, f3_rms={f3_rms[idx]:.2f}, s_num={s_num[idx]}')
        sel.annotation.get_bbox_patch().set(fc="lightblue", alpha=0.9)

    plt.show()
    plt.ioff()