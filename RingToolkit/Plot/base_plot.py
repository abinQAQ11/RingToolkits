import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
# ----------------------------------------------------------------------------------------------------------------------
def magnet(ax, height, lattice):
    current_s = 0.0
    for item in lattice.ring:
        l = item.length
        if item.type == 'drift':
            current_s += l
        elif item.type == 'quadrupole':
            ax.add_patch(plt.Rectangle((current_s, -height*1.1), l, height, color='red', alpha=0.8))
            current_s += l
        elif item.type == 'bending':
            ax.add_patch(plt.Rectangle((current_s, -height*1.1), l, height * 0.8, color='blue', alpha=1.0))
            current_s += l
        elif item.type == 'sextupole':
            ax.add_patch(plt.Rectangle((current_s, -height*1.1), l, height, color='green', alpha=1.0))
            current_s += l
# ----------------------------------------------------------------------------------------------------------------------
def plot_resonance_lines(ax, x_min, x_max, y_min, y_max):
    if not type(x_min) == int:
        x_min = int(x_min)
        x_max = int(x_max) + 1
        y_min = int(y_min)
        y_max = int(y_max) + 1

    """一阶共振"""
    for i in range(x_min, x_max + 1):
        """x=N"""
        ax.axvline(x=i, color='black', alpha=1.0, zorder=1, linewidth=4.0)

    for i in range(y_min, y_max + 1):
        """y=N"""
        ax.axhline(y=i, color='black', alpha=1.0, zorder=1, linewidth=4.0)

    """二阶共振"""
    for i in np.arange(x_min - 0.5, x_max + 0.5, 1):
        """2x=N"""
        ax.axvline(x=float(i), color='gray', alpha=1.0, zorder=2, linewidth=3.0)

    for i in np.arange(y_min - 0.5, y_max + 0.5, 1):
        """2y=N"""
        ax.axhline(y=float(i), color='gray', alpha=1.0, zorder=2, linewidth=3.0)

    for i in range(x_min + y_min, x_max + y_max + 1):
        """x+y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), i - np.linspace(x_min, x_max, 1000),
                color='gray', alpha=1.0, zorder=2, linewidth=3.0)

    for i in range(x_min - y_max, x_max - y_min + 1):
        """x-y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), np.linspace(x_min, x_max, 1000) - i,
                color='gray', alpha=1.0, zorder=2, linewidth=3.0)

    """三阶共振"""
    for i in np.arange(x_min - 1 / 3, x_max + 1 / 3, 1 / 3):
        """3x=N"""
        ax.axvline(x=float(i), color='red', alpha=0.6, zorder=3, linewidth=2.0)

    for i in range(x_min + 2 * y_min, x_max + 2 * y_max + 1):
        """x+2y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (i - np.linspace(x_min, x_max, 1000)) / 2,
                color='red', alpha=0.6, zorder=3, linewidth=2.0)

    for i in range(x_min - 2 * y_max, x_max - 2 * y_min + 1):
        """x-2y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (np.linspace(x_min, x_max, 1000) - i) / 2,
                color='red', alpha=0.6, zorder=3, linewidth=2.0)
    # ----------------------------------------------------------

    # for i in np.arange(y_min - 1 / 3, y_max + 1 / 3, 1 / 3):
    #     """3y=N"""
    #     ax.axhline(y=float(i), color='red', alpha=0.6, zorder=3, linewidth=2.0)

    # for i in range(2 * x_min + y_min, 2 * x_max + y_max + 1):
    #     """2x+y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), i - 2 * np.linspace(x_min, x_max, 1000),
    #             color='red', alpha=0.6, zorder=3, linewidth=2.0)
    #
    # for i in range(2 * x_min - y_max, 2 * x_max - y_min + 1):
    #     """2x-y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), 2 * np.linspace(x_min, x_max, 1000) - i,
    #             color='red', alpha=0.6, zorder=3, linewidth=2.0)

    """四阶共振"""
    for i in np.arange(x_min - 0.25, x_max + 0.25, 0.5):
        """4x=N"""
        ax.axvline(x=float(i), color='brown', alpha=0.9, zorder=4, linewidth=1.0)

    for i in np.arange(y_min - 0.25, y_max + 0.25, 0.5):
        """4y=N"""
        ax.axhline(y=float(i), color='brown', alpha=0.9, zorder=4, linewidth=1.0)

    for i in range(2 * x_min + 2 * y_min, 2 * x_max + 2 * y_max + 1):
        """2x+2y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (i - 2 * np.linspace(x_min, x_max, 1000)) / 2,
                color='brown', alpha=0.9, zorder=4, linewidth=1.0)

    for i in range(2 * x_min - 2 * y_max, 2 * x_max - 2 * y_min + 1):
        """2x-2y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (2 * np.linspace(x_min, x_max, 1000) - i) / 2,
                color='brown', alpha=0.9, zorder=4, linewidth=1.0)
    # ----------------------------------------------------------

    # for i in range(x_min + 3 * y_min, x_max + 3 * y_max + 1):
    #     """x+3y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), (i - np.linspace(x_min, x_max, 1000)) / 3,
    #             color='brown', alpha=0.9, zorder=4, linewidth=1.0)
    #
    # for i in range(x_min - 3 * y_max, x_max - 3 * y_min + 1):
    #     """x-3y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), (np.linspace(x_min, x_max, 1000) - i) / 3,
    #             color='brown', alpha=0.9, zorder=4, linewidth=1.0)
    #
    # for i in range(3 * x_min + y_min, 3 * x_max + y_max + 1):
    #     """3x+y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), i - 3 * np.linspace(x_min, x_max, 1000),
    #             color='brown', alpha=0.9, zorder=4, linewidth=1.0)
    #
    # for i in range(3 * x_min - y_max, 3 * x_max - y_min + 1):
    #     """3x-y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), 3 * np.linspace(x_min, x_max, 1000) - i,
    #             color='brown', alpha=0.9, zorder=4, linewidth=1.0)

    """五阶共振"""
    for i in np.arange(x_min - 0.2, x_max + 0.2, 0.2):
        """5x=N"""
        ax.axvline(x=float(i), color='green', alpha=0.8, zorder=5, linewidth=1.0)

    # for i in np.arange(y_min - 0.2, y_max + 0.2, 0.2):
    #     """5y=N"""
    #     ax.axhline(y=float(i), color='green', alpha=0.8, zorder=5, linewidth=1.0)
    #
    for i in range(x_min + 4 * y_min, x_max + 4 * y_max + 1):
        """x+4y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (i - np.linspace(x_min, x_max, 1000)) / 4,
                color='green', alpha=0.8, zorder=5, linewidth=1.0)

    for i in range(x_min - 4 * y_max, x_max - 4 * y_min + 1):
        """x-4y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (np.linspace(x_min, x_max, 1000) - i) / 4,
                color='green', alpha=0.8, zorder=5, linewidth=1.0)

    for i in range(3 * x_min + 2 * y_min, 3 * x_max + 2 * y_max + 1):
        """3x+2y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (i - 3 * np.linspace(x_min, x_max, 1000)) / 2,
                color='green', alpha=0.8, zorder=5, linewidth=1.0)

    for i in range(3 * x_min - 2 * y_max, 3 * x_max - 2 * y_min + 1):
        """3x-2y=N"""
        ax.plot(np.linspace(x_min, x_max, 1000), (3 * np.linspace(x_min, x_max, 1000) - i) / 2,
                color='green', alpha=0.8, zorder=5, linewidth=1.0)
    # ----------------------------------------------------------

    # for i in range(2 * x_min + 3 * y_min, 2 * x_max + 3 * y_max + 1):
    #     """2x+3y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), (i - 2 * np.linspace(x_min, x_max, 1000)) / 3,
    #             color='green', alpha=0.8, zorder=5, linewidth=1.0)
    #
    # for i in range(2 * x_min - 3 * y_max, 2 * x_max - 3 * y_min + 1):
    #     """2x-3y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), (2 * np.linspace(x_min, x_max, 1000) - i) / 3,
    #             color='green', alpha=0.8, zorder=5, linewidth=1.0)

    # for i in range(4 * x_min + y_min, 4 * x_max + y_max + 1):
    #     """4x+y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), i - 4 * np.linspace(x_min, x_max, 1000),
    #             color='green', alpha=0.8, zorder=5, linewidth=1.0)
    #
    # for i in range(4 * x_min - y_max, 4 * x_max - y_min + 1):
    #     """4x-y=N"""
    #     ax.plot(np.linspace(x_min, x_max, 1000), 4 * np.linspace(x_min, x_max, 1000) - i,
    #             color='green', alpha=0.8, zorder=5, linewidth=1.0)