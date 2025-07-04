
def export_to_elegant(lattice, suf: str="_1"):
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

    final = []
    transfer = []
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

    with open(f"{lattice.name}{suf}.lat", 'w', encoding='utf-8') as f:
        f.write(f"!energy={lattice.energy * 1e-9:.5f};\n\n")
        f.write("!----- table of elements ---------------------------------------------\n\n")
        for element_type in types:
            for item in elements_by_type[element_type]:
                l = item.length * 100
                if element_type == 'drift':
                    f.write(f"{item.family_name}\t: DRIFT, l = {item.length:.8f}\n")
                elif element_type == 'quadrupole':
                    n_kicks = (l - (l % 4)) if (l % 4) < 2 else (l + (4 - (l % 4)))
                    f.write(
                        f"{item.family_name}\t: KQUAD, n_kicks = {int(n_kicks)}, l = {item.length:.8f}, k1 = {item.k:.8f}\n")
                elif element_type == 'bending':
                    n_kicks = (l - (l % 4)) if (l % 4) < 2 else (l + (4 - (l % 4)))
                    f.write(
                        f"{item.family_name}\t: CSBEND, n_kicks = {int(n_kicks)}, l = {item.length:.8f}, angle = {item.bending_angle:.8f}, k1 = {item.k:.8f},&\n"
                        f"\t  e1 = {item.entrance_angle:.8f}, e2 = {item.exit_angle:.8f}, integration_order = 4\n"
                    )
                elif element_type == 'sextupole':
                    n_kicks = (l - (l % 4)) if (l % 4) < 2 else (l + (4 - (l % 4)))
                    f.write(
                        f"{item.family_name}\t: KSEXT, n_kicks = {int(n_kicks)}, l = {item.length:.8f}, k2 = {item.k:.8f}\n")
                elif element_type == 'octupole':
                    f.write(f"{item.family_name}\t: {item.type}, k3 = {item.k:.8f}\n")
            f.write("\n")
        f.write("!----- table of segments ---------------------------------------------\n\n")

        for i, item in enumerate(final):
            f.write(f"p{i+1}\t: line=({', '.join(item)})\n")
        f.write(f"PE\t: line=({', '.join(p_part + n_part)})\n")
        f.write(f"RING: line=({lattice.periodicity}*pe)\n")