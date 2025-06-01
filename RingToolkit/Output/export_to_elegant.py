
def export_to_elegant(lattice, suf: str="_1"):
    types = ['drift', 'quadrupole', 'bending', 'sextupole', 'octupole']
    elements_by_type = {key: [] for key in types}
    for item in lattice.components:
        elements_by_type[item.type].append(item)

    for type_key in elements_by_type:
        elements_by_type[type_key].sort(key=lambda x: len(x.family_name))

    result = []
    sublist = []
    dipole_count = 0
    if not lattice.half_cell:
        mags = lattice.cell
    else:
        mags = lattice.half_cell

    for item in mags:
        if item.type == "bending":
            dipole_count += 1
            if sublist and dipole_count % 2 == 1:
                sublist.append(item.family_name)
                result.append(sublist)
                sublist = []
            elif sublist and dipole_count % 2 == 0:
                result.append(sublist)
                sublist = [item.family_name]
        else:
            sublist.append(item.family_name)

    if sublist:
        result.append(sublist)

    p_part = [f"p{i + 1}" for i in range(len(result))]
    if not lattice.half_cell:
        n_part = []
    else:
        n_part = [f"-P{i + 1}" for i in range(len(result) - 1, -1, -1)]

    with open(f"{lattice.name}{suf}.lat", 'w', encoding='utf-8') as f:
        f.write(f"!energy={lattice.energy * 1e-9:.5f};\n\n")
        f.write("!----- table of elements ---------------------------------------------\n\n")
        for element_type in types:
            for item in elements_by_type[element_type]:
                if element_type == 'drift':
                    f.write(f"{item.family_name}\t: drift, l = {item.length:.8f}\n")
                elif element_type == 'quadrupole':
                    l = item.length * 100
                    n_kicks = (l - (l % 4)) if (l % 4) < 2 else (l + (4 - (l % 4)))
                    f.write(
                        f"{item.family_name}\t: kquad, n_kicks = {int(n_kicks)}, l = {item.length:.8f}, k1 = {item.k:.8f}\n")
                elif element_type == 'bending':
                    l = item.length * 100
                    n_kicks = (l - (l % 4)) if (l % 4) < 2 else (l + (4 - (l % 4)))
                    f.write(
                        f"{item.family_name}\t: csbend, n_kicks = {int(n_kicks)}, l = {item.length:.8f}, angle = {item.bending_angle:.8f}, k1 = {item.k:.8f},&\n"
                        f"\t  e1 = {item.entrance_angle:.8f}, e2 = {item.exit_angle:.8f}, integration_order = 4\n"
                    )
                elif element_type == 'sextupole':
                    l = item.length * 100
                    n_kicks = (l - (l % 4)) if (l % 4) < 2 else (l + (4 - (l % 4)))
                    f.write(
                        f"{item.family_name}\t: ksext, n_kicks = {int(n_kicks)}, l = {item.length:.8f}, k2 = {item.k:.8f}\n")
                elif element_type == 'octupole':
                    f.write(f"{item.family_name}\t: {item.type}, k3 = {item.k:.8f}\n")
            f.write("\n")
        f.write("!----- table of segments ---------------------------------------------\n\n")

        for i, item in enumerate(result):
            f.write(f"p{i+1}\t: line=({', '.join(item)})\n")
        f.write(f"pe\t: line=({', '.join(p_part + n_part)})\n")
        f.write(f"ring: line=({lattice.periodicity}*pe)\n")
    pass