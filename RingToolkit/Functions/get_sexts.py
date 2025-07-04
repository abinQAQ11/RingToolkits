import math
import numpy as np
from collections import defaultdict
# ----------------------------------------------------------------------------------------------------------------------
def get_sexts(lattice, sext_1, sext_2, cx1: float = 1.0, cy1: float = 1.0):
    chromatic_contributions = defaultdict(lambda: np.zeros(2))
    for segment in lattice.twiss:
        elem = segment[1]
        if elem['type'] == 'sextupole':
            k2 = 1.0 if elem['k2'] == 0.0 else elem['k2']
            contribution_x = k2 * elem['Disp_X'] * elem['Beta_X'] * elem['l']
            contribution_y = k2 * elem['Disp_X'] * elem['Beta_Y'] * elem['l']
            chromatic_contributions[elem['name']] += [contribution_x, contribution_y]

    sextupoles = [
        mag.family_name
        for mag in lattice.components
        if mag.type == "sextupole"
    ]
    main_sext = [sext_1, sext_2]
    others = [s for s in sextupoles if s not in main_sext]

    # 计算目标参数
    sum_main = np.array([chromatic_contributions[s] for s in main_sext])
    sum_other = np.array(sum(chromatic_contributions[s] for s in others))
    target_factor = 4 * math.pi / lattice.periodicity
    target_x = (cx1 - lattice.chromat_x0) * target_factor - sum_other[0]
    target_y = -(cy1 - lattice.chromat_y0) * target_factor - sum_other[1]

    # 解线性方程组
    matrix_a = sum_main[:, [0, 1]].T
    if np.linalg.cond(matrix_a) > 1e12:
        return 0.0, 0.0
    try:
        solution = np.linalg.solve(matrix_a, [target_x, target_y])
    except np.linalg.LinAlgError:
        return 0.0, 0.0

    return solution[0], solution[1]