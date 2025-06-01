import numpy as np
from typing import List
from .calculate_twiss import calculate_twiss
# ----------------------------------------------------------------------------------------------------------------------
def get_twiss(cell, cell_m66) -> List:
    """Calculate Twiss parameters through the lattice"""
    s = 0.0
    twiss = []
    m = np.eye(6)
    for elem in cell:
        if elem.type == "octupole":
            continue

        for item in elem.slices:
            l = item['l']
            s += l
            m = np.dot(item['matrix'], m)
            inv_m = np.linalg.inv(m)
            m_s = np.linalg.multi_dot([m, cell_m66, inv_m])

            # Calculate parameters for both planes
            beta_x, alpha_x, gamma_x, sin_phi_x, phi_x = calculate_twiss(m_s, plane='x')
            beta_y, alpha_y, gamma_y, sin_phi_y, phi_y = calculate_twiss(m_s, plane='y')

            if -100 in (phi_x, phi_y):
                return []

            # Calculate dispersion
            disp = (m_s[0][5] * (1.0 - m_s[1][1]) + m_s[0][1] * m_s[1][5]) / (2.0 - m_s[0][0] - m_s[1][1])
            d_disp = (m_s[1][5] * (1.0 - m_s[0][0]) + m_s[1][0] * m_s[0][5]) / (2.0 - m_s[0][0] - m_s[1][1])

            k = item.get('k', 0.0)
            # List of twiss parameters within one period.
            twiss.append((
                s,
                {
                    'Beta_X': beta_x, 'Alpha_X': alpha_x, 'Gamma_X': gamma_x,
                    'Beta_Y': beta_y, 'Alpha_Y': alpha_y, 'Gamma_Y': gamma_y,
                    'Disp_X': disp, 'd_Disp_X': d_disp,
                    'name': item['name'],
                    'type': item['type'],
                    'rho': item.get('rho'),
                    'k2' : item.get('k2', 0.0),
                    't1' : item.get('t1', 0.0),
                    't2' : item.get('t2', 0.0),
                    'l': l,
                    'k': k,
                }
            ))
    return twiss