import re
# ----------------------------------------------------------------------------------------------------------------------
def sbs_extract(file_path: str):
    f3_rms = []
    pair_step = []
    pair_counts = {}
    cx = []
    cy = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            f3_match = re.search(r"f3_rms=([0-9.]+(?:[eE][-+]?[0-9]+)?)", line)
            if f3_match:
                f3_rms.append(float(f3_match.group(1)))

            cx_match = re.search(r"cx1=(-?\d+\.?\d*)", line)
            if cx_match:
                cx.append(float(cx_match.group(1)))

            cy_match = re.search(r"cy1=(-?\d+\.?\d*)", line)
            if cy_match:
                cy.append(float(cy_match.group(1)))

            num_match = re.search(r"num=(\d+)", line)
            if num_match:
                pair_step.append(float(num_match.group(1)))
                num = num_match.group(1)
                pair_counts[num] = pair_counts.get(num, 0) + 1

    return f3_rms, pair_step, pair_counts, cx, cy