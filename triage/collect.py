import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(
        description="Collect and validate RTL regression results."
    )
    parser.add_argument(
        "--run-dir",
        default="runs",
        help="Regression output directory relative to project root",
    )
    parser.add_argument(
        "--expected",
        type=int,
        default=20,
        help="Expected number of seed results (default: 20)",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    run_dir = run_dir.resolve()

    try:
        run_dir.relative_to(ROOT)
    except ValueError:
        sys.exit("ERROR: --run-dir must be inside the project root.")

    if args.expected < 1:
        sys.exit("ERROR: --expected must be at least 1.")

    files = sorted(
        run_dir.glob("seed_*/result.json"),
        key=lambda p: int(p.parent.name.split("_")[1]),
    )

    results = []
    for path in files:
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
            if "seed" not in result or "passed" not in result:
                raise ValueError("Missing required seed/passed field")
            results.append(result)
        except (json.JSONDecodeError, ValueError) as exc:
            sys.exit(f"ERROR: Invalid result {path}: {exc}")

    seeds = [r["seed"] for r in results]
    if len(seeds) != len(set(seeds)):
        sys.exit("ERROR: Duplicate seed results found.")

    if len(results) != args.expected:
        sys.exit(
            f"INCOMPLETE: found {len(results)}/{args.expected} results "
            f"in {run_dir}. Check missing jobs before classifying."
        )

    bug_modes = {r.get("bug_enabled") for r in results}
    if len(bug_modes) != 1 or None in bug_modes:
        sys.exit("ERROR: Missing or mixed bug_enabled values.")

    bug_enabled = bug_modes.pop()
    summary = {
        "bug_enabled": bug_enabled,
        "total_runs": len(results),
        "passed": sum(bool(r["passed"]) for r in results),
        "failed": sum(not bool(r["passed"]) for r in results),
        "results": results,
    }

    summary_path = run_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(f"Results collected: {len(results)}/{args.expected}")
    print(f"Bug injection enabled: {bug_enabled}")
    print(f"Passed: {summary['passed']}/{len(results)}")
    print(f"Failed: {summary['failed']}/{len(results)}")
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()

