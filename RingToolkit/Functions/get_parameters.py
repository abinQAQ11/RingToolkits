import math
import numpy as np
from typing import List, Tuple
# ----------------------------------------------------------------------------------------------------------------------
def get_parameters(cell_twiss: List) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    integrals = np.zeros(5)
    chromat_0 = np.zeros(2)
    chromat_1 = np.zeros(2)
    tunes = np.zeros(2)

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
        r_inv = 1/rho if rho else 0.0

        dx_prev = prev['Disp_X']
        dx_curr = curr['Disp_X']
        bx, by = curr['Beta_X'], curr['Beta_Y']
        ax, gx = curr['Alpha_X'], curr['Gamma_X']
        hx = h_function(ax, bx, gx, dx_curr, curr['d_Disp_X'])

        # Update phase advances
        tunes += l / np.array([bx, by]) / (2.0 * math.pi)

        # Calculate integrals
        integrals += [
                    l * dx_curr * r_inv,
                    l * r_inv ** 2,
                    l * abs(r_inv) ** 3,
                    l * dx_curr * r_inv * (r_inv ** 2 + 2 * k)
                        - dx_prev * np.tan(t1) * r_inv ** 2 - dx_curr * np.tan(t2) * r_inv ** 2,
                    l * hx * r_inv ** 3
        ]
        chromat_0 += [
                    -l * bx * (r_inv**2 + k) / (4 * math.pi),
                     l * by * (k - r_inv**2.5) / (4 * math.pi)
        ]
        chromat_1 += [
                    -l * bx * (r_inv**2 + k - k2 * dx_curr) / (4 * math.pi),
                     l * by * (k - r_inv**2.5 - k2 * dx_curr) / (4 * math.pi)
        ]
    return tunes, integrals, chromat_0, chromat_1