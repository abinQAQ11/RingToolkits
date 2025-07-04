import math
import cmath
import numpy as np
from typing import List, Dict, Tuple
# ----------------------------------------------------------------------------------------------------------------------
def get_driving_terms(twiss: List, period: int):
    keys = ['h_21000', 'h_30000', 'h_10110', 'h_10020', 'h_10200']
    h_coeffs = {key: 0j for key in keys}
    Phi_x = twiss[-1][1]["phi_x"]
    Phi_y = twiss[-1][1]["phi_y"]
    d_terms = []
    d_terms_m = []
    position = 0.0
    num_sext = 0

    for i in range(period):
        for j, (s, curr) in enumerate(twiss):
            l = curr['l']
            b3 = curr['k2'] / 2
            bx = curr['Beta_X']
            by = curr['Beta_Y']
            phi_x = curr['phi_x'] + i * Phi_x
            phi_y = curr['phi_y'] + i * Phi_y
            sqrt_bx = math.sqrt(bx)
            if curr["type"] == "sextupole":
                num_sext += 1

            coeffs = {
                'h_21000': -b3 * l * sqrt_bx * bx * cmath.exp(1j * phi_x) / 8,
                'h_30000': -b3 * l * sqrt_bx * bx * cmath.exp(1j * 3 * phi_x) / 24,
                'h_10110':  b3 * l * sqrt_bx * by * cmath.exp(1j * phi_x) / 4,
                'h_10020':  b3 * l * sqrt_bx * by * cmath.exp(1j * (phi_x - 2 * phi_y)) / 8,
                'h_10200':  b3 * l * sqrt_bx * by * cmath.exp(1j * (phi_x + 2 * phi_y)) / 8,
            }
            for key in h_coeffs:
                h_coeffs[key] += coeffs.get(key, 0j)

            if i == 0:
                d_terms.append((
                    s,
                    {
                        'h_21000': (h_coeffs['h_21000'], np.array([1, 0])),
                        'h_30000': (h_coeffs['h_30000'], np.array([3, 0])),
                        'h_10110': (h_coeffs['h_10110'], np.array([1, 0])),
                        'h_10020': (h_coeffs['h_10020'], np.array([1,-2])),
                        'h_10200': (h_coeffs['h_10200'], np.array([1, 2])),
                        'phase': np.array([[phi_x], [phi_y]]), 'l': l,
                        'num_sext': num_sext
                    }
                ))
            position += l
            d_terms_m.append((position,{**{k: np.abs(v) for k, v in h_coeffs.items()}}))

    h = {k: np.abs(v) for k, v in h_coeffs.items()}
    return d_terms_m, d_terms, h
# ----------------------------------------------------------------------------------------------------------------------
def get_rdts(d_terms: List) -> Tuple[Dict, Dict, float]:
    keys = ['h_21000', 'h_30000', 'h_10110', 'h_10020', 'h_10200']
    new_keys = ['f_21000_rms', 'f_30000_rms', 'f_10110_rms', 'f_10020_rms', 'f_10200_rms']
    rdts = {key: [] for key in keys}
    f_rms = {key: 0.0 for key in keys}

    last_term = d_terms[-1][1]
    total_sexts = last_term["num_sext"]
    phase_vector = last_term["phase"]

    for i, (s, term) in enumerate(d_terms):
        for key in keys:
            coeff, m = term[key]
            fac_0 = np.dot(m, phase_vector).item()
            fac_1 = 1 - cmath.exp(1j * fac_0)
            C_0 = last_term[key][0] / fac_1
            C_t = coeff - C_0

            f_rms[key] += (np.abs(C_t) ** 2) / total_sexts
            rdts[key].append((s,
                {'C_0': np.abs(C_0), 'C_t': np.abs(-C_t)})
            )
    f3_rms = math.sqrt(sum(f_rms.values()))
    f_rms = {new_key: math.sqrt(value) for new_key, value in zip(new_keys, f_rms.values())}
    return rdts, f_rms, f3_rms