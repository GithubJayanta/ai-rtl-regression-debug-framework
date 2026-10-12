import argparse
import json
import os
from pathlib import Path

from parse_logs import parse_log
from parse_waveform import parse_vcd

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="AI-assisted RTL failure triage.")
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

    summary_path = run_dir / "summary.json"
    if not summary_path.exists():
        raise SystemExit(f"Summary not found: {summary_path}")

    raw = json.loads(summary_path.read_text())
    summary = raw["results"] if isinstance(raw, dict) else raw

    rtl_path = ROOT / "rtl" / "fifo.v"
    rtl = rtl_path.read_text()

    fails = []

    for result in summary:
        if result.get("passed"):
            continue

        log_path = ROOT / result["log"]
        parsed = parse_log(str(log_path))

        waveform_evidence = None
        waveform_path = result.get("waveform")

        if waveform_path:
            full_waveform_path = ROOT / waveform_path
            if full_waveform_path.exists():
                try:
                    waveform_evidence = parse_vcd(
                        full_waveform_path,
                        failure_ns=parsed["fail_sim_time_ns"],
                    )
                except Exception as exc:
                    waveform_evidence = {
                        "error": f"Waveform parsing failed: {exc}"
                    }
            else:
                waveform_evidence = {
                    "error": f"Waveform file not found: {waveform_path}"
                }
        else:
            waveform_evidence = {
                "error": "No waveform path recorded for this run."
            }

        fails.append({
            "seed": result["seed"],
            "errors": parsed["errors"],
            "first_fail_cycle": parsed["first_fail_cycle"],
            "fail_sim_time_ns": parsed["fail_sim_time_ns"],
            "waveform_evidence": waveform_evidence,
        })

    report_path = run_dir / "triage_report.md"

    if not fails:
        report_path.write_text("All seeds passed. Nothing to triage.\n")
        print("All seeds passed. Nothing to triage.")
        print(f"Report: {report_path}")
        return 0

    prompt = f"""You are an experienced RTL design and verification engineer.

Analyze the failing regression runs using the RTL, assertion messages,
and waveform evidence supplied below.

Rules:
1. Group failures by likely root cause, ignoring per-seed differences
   such as cycle numbers and occupancy values.
2. Separate directly observed waveform facts from inferred explanations.
3. Identify relevant signals such as count, full, wr_en, do_wr,
   rd_en, do_rd, wp, and rp.
4. Explain the causal sequence that leads to each failure.
5. Recommend a concrete RTL fix or next debugging step.
6. Do not claim a signal value was observed if it is absent from
   the supplied waveform evidence.
7. Return ONLY valid JSON, without Markdown fences, in this schema:
{{
  "groups": [
    {{
      "signature": "",
      "seeds": [],
      "observed_evidence": [],
      "root_cause": "",
      "recommended_fix": "",
      "next_debug_step": ""
    }}
  ]
}}

RTL:
{rtl}

Failing runs and waveform evidence:
{json.dumps(fails, indent=2)}"""

    try:
        from google import genai

        client = genai.Client()
        response = client.models.generate_content(
            model=os.getenv("TRIAGE_MODEL", "gemini-2.5-flash"),
            contents=prompt,
        )
        report = response.text or ""
        missing = [
            failure["seed"]
            for failure in fails
            if str(failure["seed"]) not in report
        ]
        if missing:
            report += f"\n\nWARNING: seeds missing from triage: {missing}"
    except Exception as exc:
        report = (
            f"LLM unavailable ({exc}). Raw failures:\n"
            + json.dumps(fails, indent=2)
        )

    report_path.write_text(report + "\n")
    print(report)
    print(f"\nReport saved to: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

