import math
import cmath
import numpy as np
from typing import List, Dict, Tuple
# ----------------------------------------------------------------------------------------------------------------------
def get_rdts(d_term: List) -> Tuple[Dict, Dict, float]:
    keys = ['h_21000', 'h_30000', 'h_10110', 'h_10020', 'h_10200']
    new_keys = ['f_21000_rms', 'f_30000_rms', 'f_10110_rms', 'f_10020_rms', 'f_10200_rms']
    rdts = {key: [] for key in keys}
    f_rms = {key: 0.0 for key in keys}

    total_terms = len(d_term)
    last_term = d_term[-1]
    mu_vector = last_term[1]['mu']
    s = 0.0
    for i, term in enumerate(d_term):
        s += term[1]['l']
        for key in keys:
            coeff, m = term[1][key]
            fac_0 = np.dot(m, mu_vector).item()
            fac_1 = 1 - cmath.exp(1j * fac_0)
            c_0 = last_term[1][key][0] / fac_1
            c_t = coeff - c_0

            f_rms[key] += (np.abs(c_t) ** 2) / total_terms
            rdts[key].append((
                s,
                {'C_0': np.abs(c_0), 'C_t': np.abs(c_t)}
            ))
    f3_rms = math.sqrt(sum(f_rms.values()))
    f_rms = {new_key: math.sqrt(value) for new_key, value in zip(new_keys, f_rms.values())}
    return rdts, f_rms, f3_rms