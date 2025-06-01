import math
import cmath
import numpy as np
from typing import List, Dict, Tuple
# ----------------------------------------------------------------------------------------------------------------------
def get_driving_terms(cell_twiss: List, period: int) -> Tuple[List, List, Dict]:
    ring_twiss = cell_twiss * period
    s_total = 0.0
    mu_x = mu_y = 0.0

    d_terms_m = []
    d_terms = []
    h_coeffs = {key: 0j for key in ['h_21000', 'h_30000', 'h_10110', 'h_10020', 'h_10200',
                                    'h_20001', 'h_00201', 'h_10002', 'h_11001', 'h_00111']}
    for i, (s, curr) in enumerate(ring_twiss):
        l  = curr['l']
        # k = curr['k']
        k2 = curr['k2'] / 2
        bx = curr['Beta_X']
        by = curr['Beta_Y']
        dx = curr['Disp_X']
        mu_x += l / bx
        mu_y += l / by

        # Calculate coefficients
        # common_term = (k - 2 * k2 * dx) * l
        sqrt_bx = math.sqrt(bx)
        coeffs = {
                # 'h_11001': common_term * bx / 4,
                # 'h_00111': -common_term * by / 4,
                # 'h_20001': common_term * bx * cmath.exp(2j * mu_x) / 8,
                # 'h_00201': -common_term * by * cmath.exp(2j * mu_y) / 8,
                # 'h_10002': (k - k2 * dx) * l * dx * sqrt_bx * cmath.exp(1j * mu_x) / 2,

                'h_21000': -k2 * l * sqrt_bx * bx * cmath.exp(1j * mu_x) / 8,
                'h_30000': -k2 * l * sqrt_bx * bx * cmath.exp(3j * mu_x) / 24,
                'h_10110': k2 * l * sqrt_bx * by * cmath.exp(1j * mu_x) / 4,
                'h_10020': k2 * l * sqrt_bx * by * cmath.exp(1j * (mu_x - 2 * mu_y)) / 8,
                'h_10200': k2 * l * sqrt_bx * by * cmath.exp(1j * (mu_x + 2 * mu_y)) / 8,
                }
        # Accumulate coefficients
        for key in h_coeffs:
            h_coeffs[key] += coeffs.get(key, 0j)

        s_total += l
        if i < len(cell_twiss):
            d_terms.append((
                s_total,
                {
                'h_21000': (h_coeffs['h_21000'], np.array([1, 0])),
                'h_30000': (h_coeffs['h_30000'], np.array([3, 0])),
                'h_10110': (h_coeffs['h_10110'], np.array([1, 0])),
                'h_10020': (h_coeffs['h_10020'], np.array([1,-2])),
                'h_10200': (h_coeffs['h_10200'], np.array([1, 2])),
                'mu': np.array([[mu_x],[mu_y]]), 'l': l})
                        )
        d_terms_m.append((
            s_total,
            {**{k: np.abs(v) for k, v in h_coeffs.items()},
             'Beta_X': bx, 'Beta_Y': by, 'Disp_X': dx,
             'mu_x': mu_x, 'mu_y': mu_y}
        ))
    h = {k: np.abs(v) for k, v in h_coeffs.items()}
    return d_terms_m, d_terms, h