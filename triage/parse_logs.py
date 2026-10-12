import re

def parse_log(path):
    text = open(path, errors="ignore").read()
    errs = re.findall(r"AssertionError:\s*(.+)", text)
    # first-failing cycle comes straight from our assertion message
    cycles = [int(c) for c in re.findall(r"cycle[ =](\d+)", " ".join(errs))]
    # sim time (ns) from cocotb's summary table row
    m = re.search(r"\bFAIL\s+([\d.]+)", text)
    return {"errors": sorted(set(errs)),
            "first_fail_cycle": min(cycles) if cycles else None,
            "fail_sim_time_ns": float(m.group(1)) if m else None,
            "tail": "\n".join(text.splitlines()[-25:])}
