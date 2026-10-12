import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate functional coverage from regression runs."
    )
    parser.add_argument("--run-dir", default="runs")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    run_dir = run_dir.resolve()

    try:
        run_dir.relative_to(ROOT.resolve())
    except ValueError:
        parser.error("--run-dir must be inside the project root.")

    files = sorted(run_dir.glob("seed_*/coverage.json"))
    if not files:
        raise SystemExit(f"No coverage files found in {run_dir}")

    tot = {}
    for file in files:
        try:
            coverage = json.loads(file.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            raise SystemExit(f"Cannot read {file}: {exc}")

        for key, value in coverage.items():
            if key == "max_occupancy":
                tot[key] = max(tot.get(key, 0), value)
            else:
                tot[key] = tot.get(key, 0) + value

    print(f"{len(files)} seeds with coverage")
    for key, value in tot.items():
        print(f"  {key}: {value}")

    for bin_name in (
        "full_cycles",
        "writes_blocked_full",
        "reads_blocked_empty",
        "simultaneous_requests",
    ):
        print(f"  {'HIT ' if tot.get(bin_name, 0) else 'MISS'} {bin_name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
