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
            if v[0] < 4 and v[1] < 20:
                obj_.append(v[:] + [i + 1])
                tun_.append([tunes[i][0], tunes[i][1]])
        return tun_, obj_

    tunes, obj = limit()
    num = np.array([item[-1] for item in obj])
    # num = np.array([i + 1 for i in range(len(tunes))])
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
    ax.set_xlim(min(x) - 1, max(x) + 1)
    ax.set_ylim(min(y) - 1, max(y) + 1)

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

    # 绘制直线图
    x_min, x_max = int(min(x)) - 5, int(max(x)) + 5
    y_min, y_max = int(min(y)) - 5, int(max(y)) + 5


    plot_resonance_lines(ax, x_min, x_max, y_min, y_max)

    # 显示标题
    # plt.title(r'$emittance\ &\ f_{3,rms}\ &\ fitness$', fontsize=25)

    # 显示图形
    plt.show()
    plt.ioff()