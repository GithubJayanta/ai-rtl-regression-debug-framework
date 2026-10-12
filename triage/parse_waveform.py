import re
import sys
from pathlib import Path


SIGNALS_OF_INTEREST = {
    "count", "full", "empty", "wr_en", "rd_en",
    "do_wr", "do_rd", "wp", "rp", "clk", "rst",
}


def parse_failure_time_ns(log_path):
    text = Path(log_path).read_text(errors="ignore")

    # Cocotb's test summary usually contains a row such as FAIL 281.00
    match = re.search(r"\bFAIL\s+([\d.]+)", text)
    if match:
        return float(match.group(1))

    # Fall back to the timestamp on the assertion line, if present.
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*ns.*AssertionError:", text
    )
    return float(match.group(1)) if match else None


def parse_vcd(waveform_path, failure_ns=None, window_ns=50):
    text = Path(waveform_path).read_text(errors="ignore")
    lines = text.splitlines()

    timescale_ns = None
    scope = []
    signal_ids = {}
    selected_ids = {}
    definitions_done = False

    for line in lines:
        line = line.strip()

    for line in lines:
        line = line.strip()

        if line.startswith("$timescale"):
            inline = re.search(
                r"\$timescale\s+(\d+)\s*(s|ms|us|ns|ps|fs)\s+\$end",
                line,
            )
            if inline:
                amount, unit = inline.groups()
                factors = {
                    "s": 1e9, "ms": 1e6, "us": 1e3,
                    "ns": 1.0, "ps": 1e-3, "fs": 1e-6,
                }
                timescale_ns = int(amount) * factors[unit]
            continue

        if line.startswith("$scope"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] != "$end":
                scope.append(parts[2])
            continue

        if line.startswith("$upscope"):
            if scope:
                scope.pop()
            continue

        if line.startswith("$var"):
            parts = line.split()
            if len(parts) >= 5:
                width = int(parts[2])
                identifier = parts[3]
                signal_name = parts[4]
                full_name = ".".join(scope + [signal_name])
                signal_ids[identifier] = {
                    "name": full_name,
                    "width": width,
                }
                if (
                    full_name.startswith("fifo.")
                    and signal_name in SIGNALS_OF_INTEREST
                ):
                    selected_ids[identifier] = full_name
            continue

        if line.startswith("$enddefinitions"):
            definitions_done = True
            break
    if timescale_ns is None:
        raise ValueError("Could not read VCD timescale.")

    # Fall back to matching leaf names if the hierarchy differs.
    if not selected_ids:
        for identifier, info in signal_ids.items():
            leaf = info["name"].split(".")[-1]
            if leaf in SIGNALS_OF_INTEREST:
                selected_ids[identifier] = info["name"]

    if not definitions_done:
        raise ValueError("VCD signal definitions are incomplete.")

    if not selected_ids:
        raise ValueError("No relevant FIFO signals found in the VCD.")

    current_time = 0
    values = {}
    transitions = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("#"):
            try:
                current_time = int(line[1:])
            except ValueError:
                continue
            continue

        identifier = None
        value = None

        if line[0] in "bB":
            parts = line[1:].split()
            if len(parts) == 2:
                value, identifier = parts
                value = value.lower()
        elif line[0] in "01xXzZ":
            value = line[0].lower()
            identifier = line[1:]

        if identifier not in selected_ids or value is None:
            continue

        values[identifier] = value
        transitions.append(
            (current_time, selected_ids[identifier], value)
        )

    failure_units = (
        int(round(failure_ns / timescale_ns))
        if failure_ns is not None else None
    )
    window_units = int(round(window_ns / timescale_ns))

    if failure_units is not None:
        transitions = [
            item for item in transitions
            if failure_units - window_units
            <= item[0]
            <= failure_units + window_units
        ]

    # Convert timestamps into ns and cap output size.
        transitions = transitions[-150:]

    return {
        "timescale_ns_per_unit": timescale_ns,
        "failure_time_ns": failure_ns,
        "signals": sorted(set(selected_ids.values())),
        "transitions": [
            {
                "time_ns": round(time * timescale_ns, 6),
                "signal": name,
                "value": value,
            }
            for time, name, value in transitions
        ],
    }


def main():
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python triage/parse_waveform.py "
            "<waveform.vcd> [log.txt]"
        )

    waveform = Path(sys.argv[1])
    log_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    failure_ns = (
        parse_failure_time_ns(log_path)
        if log_path and log_path.exists()
        else None
    )

    result = parse_vcd(waveform, failure_ns)
    print(f"VCD timescale: {result['timescale_ns_per_unit']} ns/unit")
    print(f"Failure time: {result['failure_time_ns']} ns")
    print("Selected signals:", ", ".join(result["signals"]))
    print("\nTransitions near failure:")

    for item in result["transitions"]:
        print(
            f"{item['time_ns']:12.6f} ns  "
            f"{item['signal']:<20} = {item['value']}"
        )


if __name__ == "__main__":
    main()
