import math
import numpy as np
from typing import List, Tuple
# ----------------------------------------------------------------------------------------------------------------------
def calculate_twiss(m_s: np.ndarray, plane: str = 'x') -> Tuple:
    """Calculate Twiss parameters for a given plane from the transfer matrix.
    Args:
        m_s: Symplectic transfer matrix -> M(s+L|s).
        plane: 'x' or 'y' for horizontal or vertical plane.
    Returns:
        Tuple of (beta, alpha, gamma, phi) for the specified plane.
        Returns (0, 0, 0, -100) if trace condition not met.
    """

    index = 0 if plane == 'x' else 2
    trace = (m_s[index, index] + m_s[index + 1, index + 1]) / 2

    if not (abs(trace) < 1.0):
        return 0.0, 0.0, 0.0, -100

    phi = math.acos(trace)
    sin_phi = math.sin(phi)
    beta_key = (index, index + 1)

    # Check the sign of sin(phi) to ensure the beta is positive.
    sign_check = (sin_phi < 0.0 and m_s[beta_key] < 0.0) or (sin_phi > 0.0 and m_s[beta_key] > 0.0)
    sin_phi = -sin_phi if not sign_check else sin_phi

    beta = m_s[beta_key] / sin_phi
    alpha = (m_s[index, index] - m_s[index + 1, index + 1]) / (2 * sin_phi)
    gamma = -m_s[index + 1, index] / sin_phi

    return beta, alpha, gamma, phi
# ----------------------------------------------------------------------------------------------------------------------
def calculate_dispersion(matrix) -> Tuple:
    """Calculate dispersion and its derivative from the transfer matrix."""

    eta = (matrix[0][5] * (1.0 - matrix[1][1]) + matrix[0][1] * matrix[1][5]) / (2.0 - matrix[0][0] - matrix[1][1])
    d_eta = (matrix[1][5] * (1.0 - matrix[0][0]) + matrix[1][0] * matrix[0][5]) / (2.0 - matrix[0][0] - matrix[1][1])
    return eta, d_eta
# ----------------------------------------------------------------------------------------------------------------------
def get_twiss(cell, cell_m66) -> List:
    """Calculate Twiss parameters through the lattice.
    Args:
        cell: List of lattice elements with their properties.
        cell_m66: 6x6 transfer matrix for the full cell.
    Returns:
        List of tuples containing (s_position, twiss_parameters_dict) for each element.
        """

    # Initialize periodic solution
    bx0, ax0, gx0, Phi_x = calculate_twiss(cell_m66, plane="x")
    by0, ay0, gy0, Phi_y = calculate_twiss(cell_m66, plane="y")

    if -100 in (Phi_x, Phi_y):
        return []

    eta0, d_eta0 = calculate_dispersion(cell_m66)

    twiss = [(
        0.0,
        {
            'Beta_X': bx0, 'Alpha_X': ax0, 'Gamma_X': gx0, 'Disp_X': eta0,
            'Beta_Y': by0, 'Alpha_Y': ay0, 'Gamma_Y': gy0, 'd_Disp_X': d_eta0,
            'phi_x': 0.0, 'phi_y': 0.0, 'name': "START", 'type': "None",
            'rho': 0.0, 'l': 0.0, 'k2': 0.0, 'k': 0.0, 't1': 0.0, 't2': 0.0,
        }
    )]

    s = 0.0
    m = np.eye(6)
    prev_phi_x = prev_phi_y = 0.0
    times_num_x = times_num_y = 0
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
            beta_x, alpha_x, gamma_x, _ = calculate_twiss(m_s, plane='x')
            beta_y, alpha_y, gamma_y, _ = calculate_twiss(m_s, plane='y')
            disp, d_disp = calculate_dispersion(m_s)

            phi_x = math.atan(m[0, 1]/ (m[0, 0] * bx0 - m[0, 1] * ax0))
            phi_y = math.atan(m[2, 3]/ (m[2, 2] * by0 - m[2, 3] * ay0))

            if prev_phi_x > 0 >= phi_x:
                times_num_x += 1
            prev_phi_x = phi_x
            phi_x += math.pi * times_num_x

            if prev_phi_y > 0 >= phi_y:
                times_num_y += 1
            prev_phi_y = phi_y
            phi_y += math.pi * times_num_y

            # List of twiss parameters within one period.
            twiss.append((
                s,
                {
                    'Beta_X': beta_x, 'Alpha_X': alpha_x, 'Gamma_X': gamma_x, 'Disp_X': disp,
                    'Beta_Y': beta_y, 'Alpha_Y': alpha_y, 'Gamma_Y': gamma_y, 'd_Disp_X': d_disp,
                    'name': item['name'], 'type': item['type'],
                    'phi_x': phi_x, 'phi_y': phi_y,
                    't1' : item.get('t1', 0.0),
                    't2' : item.get('t2', 0.0),
                    'k2': item.get('k2', 0.0),
                    'k': item.get('k', 0.0),
                    'rho': item.get('rho'),
                    'l': l,
                }
            ))
    return twiss