import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRIAGE_DIR = ROOT / "triage"


def run_stage(name, command, expected_failure=False):
    print(f"\n{'=' * 60}")
    print(f"STAGE: {name}")
    print(f"{'=' * 60}", flush=True)

    result = subprocess.run(command, cwd=ROOT, check=False)

    if result.returncode != 0:
        if expected_failure:
            print(
                f"{name} returned {result.returncode}. "
                "Continuing because failures are expected in bug mode."
            )
        else:
            print(f"WARNING: {name} returned {result.returncode}.")

    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run the RTL regression triage pipeline.")
    parser.add_argument("seeds", nargs="?", type=int, default=8)
    parser.add_argument("--bug", action="store_true")
    parser.add_argument("--run-dir", default="runs")
    args = parser.parse_args()

    if args.seeds < 1:
        parser.error("Number of seeds must be at least 1.")

    run_dir = Path(args.run_dir)
    if run_dir.is_absolute():
        try:
            run_dir = run_dir.resolve().relative_to(ROOT.resolve())
        except ValueError:
            parser.error("--run-dir must be inside the project root.")
    else:
        run_dir = run_dir.resolve()
        try:
            run_dir = run_dir.relative_to(ROOT.resolve())
        except ValueError:
            parser.error("--run-dir must resolve inside the project root.")

    run_dir_arg = str(run_dir)
    python = sys.executable

    regression_command = [
        python, str(TRIAGE_DIR / "run_regression.py"),
        str(args.seeds), "--run-dir", run_dir_arg,
    ]
    if args.bug:
        regression_command.append("--bug")

    regression_code = run_stage(
        "Regression", regression_command, expected_failure=args.bug
    )

    # Check coverage_report.py supports --run-dir before enabling this stage.
    coverage_code = run_stage(
        "Functional coverage",
        [python, str(TRIAGE_DIR / "coverage_report.py"),
         "--run-dir", run_dir_arg],
    )

    classification_code = run_stage(
        "Failure classification",
        [python, str(TRIAGE_DIR / "classify_results.py"),
         "--run-dir", run_dir_arg],
    )

    if args.bug or regression_code != 0:
        llm_code = run_stage(
            "LLM-assisted triage",
            [python, str(TRIAGE_DIR / "triage_llm.py"),
             "--run-dir", run_dir_arg],
            expected_failure=args.bug,
        )
    else:
        llm_code = 0
        print("\nSkipping LLM triage: normal regression passed.")

    print(f"\n{'=' * 60}")
    print("PIPELINE SUMMARY")
    print(f"{'=' * 60}")
    print(f"Mode: {'BUG INJECTION' if args.bug else 'NORMAL'}")
    print(f"Seeds: {args.seeds}")
    print(f"Run directory: {run_dir_arg}")
    print(f"Regression exit code: {regression_code}")
    print(f"Coverage report exit code: {coverage_code}")
    print(f"Classification exit code: {classification_code}")
    print(f"LLM triage exit code: {llm_code}")

    analysis_ok = (
        coverage_code == 0
        and classification_code == 0
        and llm_code == 0
    )

    if analysis_ok and (args.bug or regression_code == 0):
        print("PIPELINE COMPLETED.")
        return 0

    print("PIPELINE COMPLETED WITH ERRORS. Check the stage output above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

