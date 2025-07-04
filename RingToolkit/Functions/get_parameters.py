import numpy as np
from math import tan, pi
from typing import List, Tuple
# ----------------------------------------------------------------------------------------------------------------------
def get_parameters(cell_twiss: List) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    tunes = np.array([cell_twiss[-1][1]["phi_x"] / (2 * pi), cell_twiss[-1][1]["phi_y"] / (2 * pi)])
    integrals = np.zeros(5)
    chromat_0 = np.zeros(2)
    chromat_1 = np.zeros(2)

    def h_function(alpha: float, beta: float, gamma: float, disp: float, d_disp: float) -> float:
        return gamma * disp ** 2 + 2.0 * alpha * disp * d_disp + beta * d_disp ** 2

    for i, (s, curr) in enumerate(cell_twiss):
        prev = cell_twiss[i - 1][1] if i > 0 else curr

        t1 = curr['t1']
        t2 = curr['t2']
        l = curr['l']
        k = curr['k']
        k2 = curr['k2']
        rho = curr['rho'] or 0.0
        h = 1 / rho if rho else 0.0

        dx_p = prev["Disp_X"]
        d_dx_p = prev["d_Disp_X"]
        ax_p, ay_p = prev["Alpha_X"], prev["Alpha_Y"]
        bx_p, by_p = prev["Beta_X"], prev["Beta_Y"]

        dx = curr['Disp_X']
        d_dx = curr['d_Disp_X']
        ax, ay = curr["Alpha_X"], curr["Alpha_Y"]
        bx, by = curr['Beta_X'], curr['Beta_Y']
        gx, gy = curr["Gamma_X"], curr["Gamma_Y"]
        hx = h_function(ax, bx, gx, dx, d_dx)

        integrals += [
            l * dx * h,
            l * h ** 2,
            l * abs(h) ** 3,
            l * dx * h * (h ** 2 + 2 * k) + dx_p * tan(-t1) * h ** 2 + dx * tan(-t2) * h ** 2,
            l * hx * h ** 3
        ]

        # edge_1_x = (h * bx_p * tan(-t1) - h * tan(-t1) ** 2 * (bx_p * d_dx_p - ax_p * dx_p + h * dx_p * bx_p * tan(-t1))) / (4 * pi)
        edge_1_y = (-h * bx_p * tan(-t1) + h * tan(-t1) ** 2 * (by_p * d_dx_p - ay_p * dx_p - h * dx_p * by_p * tan(-t1)) + by_p * h * d_dx_p) / (4 * pi)
        # edge_2_x = (h * bx * tan(-t2) + h * tan(-t2) ** 2 * (bx * d_dx - ax * dx - h * dx * bx * tan(-t2))) / (4 * pi)
        edge_2_y = (-h * bx * tan(-t2) - h * tan(-t2) ** 2 * (by * d_dx - ay * dx + h * dx * by * tan(-t2)) - by * h * d_dx) / (4 * pi)

        chromat_0 += [
            - ((k + h ** 2 - 2 * h * k * dx) * bx + h * (2 * d_dx * ax - dx * gx)) * l / (4 * pi),
            edge_1_y + edge_2_y + ((k - h * k * dx) * by + h * dx * gy) * l / (4 * pi)
        ]
        chromat_1 += [
             - ((k + h ** 2 - (k2 + 2 * h * k) * dx) * bx + h * (2 * d_dx * ax - dx * gx)) * l / (4 * pi),
            edge_1_y + edge_2_y + ((k - (k2 + h * k) * dx) * by + h * dx * gy) * l / (4 * pi)
        ]
    return tunes, integrals, chromat_0, chromat_1