import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(
        description="Classify RTL regression outcomes."
    )
    parser.add_argument(
        "--run-dir",
        default="runs",
        help="Regression output directory relative to project root",
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

    summary_path = run_dir / "summary.json"
    report_path = run_dir / "classification_report.json"

    if not summary_path.is_file():
        sys.exit(f"ERROR: Summary not found: {summary_path}")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    results = summary.get("results", [])
    bug_enabled = summary.get("bug_enabled", False)

    classified = []

    for result in results:
        log_value = result.get("log")
        log_path = ROOT / log_value if log_value else None
        log = (
            log_path.read_text(errors="replace")
            if log_path and log_path.is_file()
            else ""
        )

        if result.get("timed_out"):
            classification = "INFRASTRUCTURE_TIMEOUT"

        elif result.get("error"):
            classification = "INFRASTRUCTURE_ERROR"

        elif result.get("test_count", 0) == 0:
            classification = "NO_TEST_EXECUTED"

        elif result.get("passed"):
            classification = "PASS"

        elif "AssertionError" in log:
            expected_bug_signature = (
                "full mismatch" in log
                and "occupancy=" in log
                and ("wr=1" in log or "rd=1" in log)
            )

            if bug_enabled and expected_bug_signature:
                classification = "BUG_DETECTED"
            else:
                classification = "FUNCTIONAL_FAILURE"

        else:
            classification = "UNCLASSIFIED_FAILURE"

        classified.append({
            "seed": result.get("seed"),
            "classification": classification,
            "bug_enabled": bug_enabled,
            "log": log_value,
        })

    counts = {}
    for item in classified:
        key = item["classification"]
        counts[key] = counts.get(key, 0) + 1

    report = {
        "bug_enabled": bug_enabled,
        "total_runs": len(classified),
        "classification_counts": counts,
        "results": classified,
    }

    report_path.write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    print(json.dumps({
        "bug_enabled": bug_enabled,
        "total_runs": len(classified),
        "classification_counts": counts,
        "report": str(report_path),
    }, indent=2))


if __name__ == "__main__":
    main()

