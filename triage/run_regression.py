import argparse
import shutil
import concurrent.futures
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests"
RUNS_DIR = ROOT / "runs"

MAX_WORKERS = 4
TIMEOUT_SECONDS = 120


def run_seed(seed, bug, runs_dir):
    run_dir = runs_dir / f"seed_{seed}"
    run_dir.mkdir(parents=True, exist_ok=True)

    results_file = run_dir / "results.xml"
    log_file = run_dir / "log.txt"
    coverage_file = run_dir / "coverage.json"
    waveform_file = run_dir / "waveform.vcd"
    build_dir = run_dir / f"build_bug{int(bug)}"   # separate build per mode
# Remove stale Verilator artifacts so tracing settings are applied consistently.
    shutil.rmtree(build_dir, ignore_errors=True)

    # Clear outputs from any previous run so stale files can't look current
    results_file.unlink(missing_ok=True)
    coverage_file.unlink(missing_ok=True)
    waveform_file.unlink(missing_ok=True)

    env = os.environ.copy()
    env["RANDOM_SEED"] = str(seed)
    env["COVERAGE_FILE"] = str(coverage_file)
    # Make sure cocotb can import test_fifo.py from the tests directory
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(TESTS_DIR) + (os.pathsep + existing if existing else "")

    cmd = [
        "make",
        "-C", str(TESTS_DIR),
        f"SIM_BUILD={build_dir}",
        f"COCOTB_RESULTS_FILE={results_file}",
        f"BUG={1 if bug else 0}",
        f'SIM_CMD_SUFFIX=--trace-file {waveform_file}',
    ]

    started = time.monotonic()
    exit_code = None
    error = None
    timed_out = False
    log_text = ""

    try:
        process = subprocess.run(
            cmd, env=env, capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS, check=False,
        )
        exit_code = process.returncode
        log_text = process.stdout + process.stderr

    except subprocess.TimeoutExpired as exc:
        timed_out = True
        error = f"Timed out after {TIMEOUT_SECONDS} seconds"
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        log_text = stdout + stderr + "\n" + error

    except OSError as exc:
        error = str(exc)
        log_text = f"Failed to launch simulator: {exc}"

    duration = round(time.monotonic() - started, 3)
    log_file.write_text(log_text, encoding="utf-8")

    test_count = 0
    failures = 0
    xml_error = None

    if results_file.exists():
        try:
            root = ET.parse(results_file).getroot()
            testcases = root.findall(".//testcase")
            test_count = len(testcases)
            failures = sum(
                1 for case in testcases
                if case.find("failure") is not None
                or case.find("error") is not None
                or case.find("skipped") is not None
            )
        except ET.ParseError as exc:
            xml_error = f"Invalid results XML: {exc}"

    passed = (
        exit_code == 0
        and not timed_out
        and test_count > 0
        and failures == 0
        and xml_error is None
        and error is None
    )

    return {
        "seed": seed,
        "bug_enabled": bug,
        "passed": passed,
        "exit_code": exit_code,
        "test_count": test_count,
        "failed_or_skipped_tests": failures,
        "duration_seconds": duration,
        "timed_out": timed_out,
        "error": error or xml_error,
        "log": str(log_file.relative_to(ROOT)),
        "results_xml": (str(results_file.relative_to(ROOT))
                        if results_file.exists() else None),
        "coverage": (str(coverage_file.relative_to(ROOT))
                     if coverage_file.exists() else None),
        "waveform": (str(waveform_file.relative_to(ROOT))
                     if waveform_file.exists() else None),
    }



def main():
    parser = argparse.ArgumentParser(description="Run parallel FIFO RTL regression.")
    parser.add_argument(
        "n", nargs="?", type=int, default=8,
        help="Number of seeds to run (default: 8)"
    )
    parser.add_argument(
        "--bug", action="store_true",
        help="Enable the injected RTL bug"
    )
    parser.add_argument(
        "--run-dir", default="runs",
        help="Output directory relative to the project root (default: runs)"
    )
    args = parser.parse_args()

    n = args.n
    bug = args.bug

    if n < 1:
        raise SystemExit("Number of seeds must be at least 1.")

    runs_dir = Path(args.run_dir)
    if not runs_dir.is_absolute():
        runs_dir = ROOT / runs_dir
    runs_dir = runs_dir.resolve()

    try:
        runs_dir.relative_to(ROOT)
    except ValueError:
        raise SystemExit("--run-dir must be inside the project root.")

    runs_dir.mkdir(parents=True, exist_ok=True)
    results = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        futures = {
            executor.submit(run_seed, seed, bug, runs_dir): seed
            for seed in range(1, n + 1)
        }

        for future in concurrent.futures.as_completed(futures):
            seed = futures[future]

            try:
                result = future.result()
            except Exception as exc:
                log_path = runs_dir / f"seed_{seed}" / "log.txt"
                result = {
                    "seed": seed,
                    "bug_enabled": bug,
                    "passed": False,
                    "timed_out": False,
                    "test_count": 0,
                    "error": f"Unexpected worker error: {exc}",
                    "log": str(log_path.relative_to(ROOT)),
                }

            result_path = runs_dir / f"seed_{seed}" / "result.json"
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(
                json.dumps(result, indent=2),
                encoding="utf-8",
            )
            results.append(result)

    results.sort(key=lambda r: r["seed"])
    passed_count = sum(bool(r["passed"]) for r in results)

    summary = {
        "total_runs": len(results),
        "passed": passed_count,
        "failed": len(results) - passed_count,
        "bug_enabled": bug,
        "max_workers": MAX_WORKERS,
        "results": results,
    }

    summary_file = runs_dir / "summary.json"
    summary_file.write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(f"Regression: {passed_count}/{len(results)} passed")
    print(f"Bug injection enabled: {bug}")
    print(f"Summary: {summary_file}")

    return 0 if passed_count == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
