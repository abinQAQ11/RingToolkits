import mplcursors
import matplotlib
matplotlib.use('TkAgg')
from .base_plot import *
# ----------------------------------------------------------------------------------------------------------------------
def plot_tunes(tunes, obj, var: str = "emittance", var_index: int = 0):
    plt.ion()

    def limit():
        obj_ = []
        tun_ = []
        for i, v in enumerate(obj):
            if v[0] < 2.8:
                obj_.append(v[:] + [i + 1])
                tun_.append([tunes[i][0], tunes[i][1]])
        return tun_, obj_

    # tunes, obj = limit()
    # num = np.array([item[-1] for item in obj])
    num = np.array([i + 1 for i in range(len(tunes))])
    x = np.array([item[0] for item in tunes])  # x 坐标
    y = np.array([item[1] for item in tunes])  # y 坐标

    fig, ax = plt.subplots(figsize=(10, 10))
    sizes = np.array([item[var_index] for item in obj])
    scatter = ax.scatter(x, y, s=30, c=sizes, cmap='jet', alpha=1.0)

    x0 = np.array([7.165])
    y0 = np.array([2.614])
    ax.scatter(x0, y0, color='red', s=50, marker='^')

    cbar = plt.colorbar(scatter, pad=0.01)
    cbar.ax.tick_params(labelsize=20)
    cbar.set_label(var, fontsize=25)

    ax.set_xlabel(r'$\nu_{x}$', fontsize=30)
    ax.set_ylabel(r'$\nu_{y}$', fontsize=30)
    ax.tick_params(axis='both', labelsize=25)

    x_min = math.floor(min(x))
    x_max = math.ceil(max(x))
    y_min = math.floor(min(y))
    y_max = math.ceil(max(y))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    cursor = mplcursors.cursor(scatter, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        sel.annotation.set_text(f"nux={x[idx]:.4f}\n"
                                f"nuy={y[idx]:.4f}\n"
                                f"emit={obj[idx][0]:.4f}\n"
                                f"value={obj[idx][1]:.4f}\n"
                                f"num={num[idx]}")
        sel.annotation.get_bbox_patch().set(fc="lightblue", alpha=0.9)

    plot_resonance_lines(ax, x_min, x_max, y_min, y_max)

    # 显示标题
    # plt.title(r'$emittance\ &\ f_{3,rms}\ &\ fitness$', fontsize=25)

    # 显示图形
    plt.show()
    plt.ioff()