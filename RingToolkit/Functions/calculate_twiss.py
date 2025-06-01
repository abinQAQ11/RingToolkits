import math
import numpy as np
# ----------------------------------------------------------------------------------------------------------------------
def calculate_twiss(m_s: np.ndarray, plane: str = 'x'):
    """Helper method for Twiss parameter calculation per plane"""
    index = 0 if plane == 'x' else 2
    trace = (m_s[index, index] + m_s[index + 1, index + 1]) * 0.5

    if not (-1.0 < trace < 1.0):
        return 0.0, 0.0, 0.0, 0.0, -100

    phi = math.acos(trace)
    sin_phi = math.sin(phi)

    beta_key = (index, index + 1)
    # Check the sign of sin(phi) to ensure the beta is positive.
    sign_check = (sin_phi < 0.0 and m_s[beta_key] < 0.0) or (sin_phi > 0.0 and m_s[beta_key] > 0.0)
    sin_phi = -sin_phi if not sign_check else sin_phi

    beta = m_s[beta_key] / sin_phi
    alpha = (m_s[index, index] - m_s[index + 1, index + 1]) / (2 * sin_phi)
    gamma = -m_s[index + 1, index] / sin_phi

    return beta, alpha, gamma, sin_phi, phi