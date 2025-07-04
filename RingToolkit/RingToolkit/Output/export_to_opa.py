import math
# ----------------------------------------------------------------------------------------------------------------------
def export_to_opa(lattice, suf: str='_1'):
    ax = lattice.ax
    ay = lattice.ay
    types = ['drift', 'quadrupole', 'bending', 'sextupole', 'octupole']
    elements_by_type = {key: [] for key in types}
    for item in lattice.components:
        elements_by_type[item.type].append(item)

    for type_key in elements_by_type:
        elements_by_type[type_key].sort(key=lambda x: len(x.family_name))

    mags = lattice.half_cell if lattice.half_cell else lattice.cell

    result, current_group = [], []
    in_bend = False

    for item in mags:
        is_bend = item.type == "bending"
        if is_bend != in_bend and current_group:
            result.append(current_group)
            current_group = []
            in_bend = is_bend
        current_group.append(item.family_name)

    if current_group:
        result.append(current_group)

    final, transfer = [], []
    for i, group in enumerate(result):
        if i % 2 == 1:
            if len(final) % 2 == 1:
                transfer.extend(group)
                final.append(transfer)
                transfer = []
            else:
                if transfer:
                    final.append(transfer)
                transfer = group
        else:
            transfer.extend(group)

    if transfer:
        final.append(transfer)

    p_part = [f"P{i+1}" for i in range(len(final))]
    n_part = [] if not lattice.half_cell else [f"-P{i+1}" for i in range(len(final)-1, -1, -1)]

    with open(f'{lattice.name}{suf}.opa', 'w', encoding='utf-8') as f:
        f.write(f"energy={lattice.energy * 1e-9:.5f};\n\n")
        for element_type in types:
            for item in elements_by_type[element_type]:
                if element_type == 'drift':
                    f.write(f"{item.family_name}: {item.type}, L = {item.length:.8f}, ax = {ax}, ay = {ay};\n")
                elif element_type == 'quadrupole':
                    f.write(f"{item.family_name}: {item.type}, L = {item.length:.8f}, K = {item.k}, ax = {ax}, ay = {ay};\n")
                elif element_type == 'bending':
                    f.write(
                        f"{item.family_name}: {item.type}, L = {item.length:.8f}, t = {math.degrees(item.bending_angle):.8f}, k = {item.k},\n"
                        f"t1 = {math.degrees(item.entrance_angle):.8f}, t2 = {math.degrees(item.exit_angle):.8f}, gap = {item.gap},\n"
                        f"k1in = {item.k1in}, k2ex = {item.k2ex}, k2in = {item.k2in},\n"
                        f"k2ex = {item.k2ex}, ax = {ax}, ay = {ay};\n"
                    )
                elif element_type == 'sextupole':
                    f.write(f"{item.family_name}: {item.type}, L = {item.length:.8f}, K = {item.k / 2}, ax = {ax}, ay = {ay};\n")
                elif element_type == 'octupole':
                    f.write(f"{item.family_name}: {item.type}, k = {item.k}, ax = {ax}, ay = {ay};\n")
            f.write("\n")

        for i, item in enumerate(final):
            f.write(f"P{i+1}:{','.join(item)};\n")
        f.write("\n")
        f.write(f"PE:{','.join(p_part + n_part)};\n\n")
        f.write(f"ring:{lattice.periodicity}*PE;")