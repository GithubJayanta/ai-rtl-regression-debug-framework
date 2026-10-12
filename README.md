# AI-Assisted RTL Regression and Debug Automation Framework

**Automated RTL regression · Failure classification · AI-assisted
root-cause analysis**

A reproducible verification workflow combining Verilog, Cocotb,
Verilator, Python, SLURM, and Gemini-powered triage.

------------------------------------------------------------------------

## Overview

This project automates regression testing and failure triage for a
Verilog FIFO. It supports randomized multi-seed simulation, deliberate
bug injection, result aggregation, failure classification, coverage
reporting, and AI-assisted debugging.

The goal is to make RTL verification results easier to reproduce,
inspect, and diagnose---while keeping the evidence from each simulation
run organized.

## Highlights

-   **Randomized regression:** Run the FIFO testbench across multiple
    seeds.
-   **Bug injection:** Enable a deliberate FIFO write-control bug with a
    compile-time option.
-   **Parallel cluster execution:** Launch clean and bug-injected
    regression jobs through SLURM.
-   **Automated reporting:** Collect per-seed results into
    machine-readable summaries.
-   **Failure classification:** Distinguish passing runs from the known
    injected-bug signature.
-   **AI-assisted triage:** Generate a diagnosis and suggested
    correction from failure evidence.
-   **Debug artifacts:** Keep logs, XML results, coverage data, and
    waveforms for investigation.

## Validation Results

The pipeline was validated on a SLURM cluster with **20 randomized seeds
per mode**.

  Metric               Clean RTL    Bug-injected RTL
  ------------------ ----------- -------------------
  Regression seeds            20                  20
  Passed runs                 20                   0
  Failed runs                  0                  20
  Classification       20 `PASS`   20 `BUG_DETECTED`
  SLURM job                 `47`                `48`
  Job exit status          `0:0`               `0:0`

**Interpretation:** the clean design passed all 20 runs. With the
deliberate overflow bug enabled, all 20 runs failed the test and were
classified as `BUG_DETECTED`. The simulator process itself exited
successfully in the bug-injected run; test failures are represented
separately in the regression results.

> These results demonstrate detection of the specific injected FIFO bug
> in this test setup. They do not establish general detection accuracy
> for arbitrary RTL bugs.

## Example: Injected FIFO Overflow Bug

The correct write-control logic blocks writes when the FIFO is full:

``` verilog
wire do_wr = wr_en && !full;
```

The bug-injected version removes the full check:

``` verilog
wire do_wr = wr_en;
```

This permits a write request while the FIFO is full. The regression
detected the resulting overflow behavior, and the generated triage
identified the missing `!full` condition as the root cause.

### Suggested correction

``` verilog
wire do_wr = wr_en && !full;
```

The exact behavior for simultaneous read/write requests should always be
checked against the intended FIFO specification.

## Workflow

``` text
Verilog FIFO + Cocotb testbench
              |
              v
    Verilator simulations
    across randomized seeds
              |
              v
       Per-seed artifacts
   results / logs / waveforms
              |
              v
       Result aggregation
        and coverage report
              |
              v
       Failure classification
              |
              v
     AI-assisted failure triage
       and suggested correction
```

## Technology Stack

  -----------------------------------------------------------------------
  Technology                          Role
  ----------------------------------- -----------------------------------
  Verilog HDL                         FIFO RTL design and conditional bug
                                      injection

  Cocotb                              Python-based RTL testbench

  Verilator                           RTL simulation

  Python                              Regression orchestration,
                                      collection, classification, and
                                      reporting

  SLURM                               Cluster job scheduling and parallel
                                      regression execution

  Gemini API                          AI-assisted failure analysis
  -----------------------------------------------------------------------

The validated development environment used Python 3.12, Verilator 5.020,
and Cocotb 1.9.2. The project also uses the `google.genai` SDK for
Gemini-based triage.

## Repository Layout

``` text
ai-regression-triage/
├── rtl/
│   └── fifo.v
├── tests/
│   ├── test_fifo.py
│   └── Makefile
├── triage/
│   ├── run_regression.py
│   ├── collect.py
│   ├── classify_results.py
│   ├── coverage_report.py
│   ├── triage_llm.py
│   └── run_pipeline.py
├── slurm/
│   └── validate_pipeline.sbatch
├── results/                 # Curated reports (recommended)
├── docs/                    # Diagrams/screenshots (recommended)
├── requirements.txt
├── .gitignore
└── README.md
```

Confirm filenames against the actual repository before relying on this
illustrative tree.

## Run Locally

### Prerequisites

-   Linux or WSL2
-   Python 3.12 (validated environment)
-   Verilator (version 5.020 was validated)
-   Cocotb (version 1.9.2 was validated)
-   Python dependencies listed in `requirements.txt`
-   A Gemini API key only if AI triage is enabled

Install your project dependencies using the repository's dependency
file:

``` bash
python -m pip install -r requirements.txt
```

Ensure `verilator` is installed and available on `PATH`.

### Clean regression

``` bash
python triage/run_pipeline.py 20 --run-dir runs/local_clean
```

### Bug-injected regression

``` bash
python triage/run_pipeline.py 20 --bug --run-dir runs/local_bug
```

The pipeline writes run summaries, classification reports, and per-seed
debug artifacts under the selected run directory.

## Run on SLURM

Submit the clean regression:

``` bash
sbatch --export=ALL slurm/validate_pipeline.sbatch 20 clean
```

Submit the bug-injected regression:

``` bash
sbatch --export=ALL slurm/validate_pipeline.sbatch 20 bug
```

Check job status:

``` bash
squeue -u "$USER"
```

The batch script assumes the Python virtual environment is available at
`$HOME/.venv` and that Verilator and the required dependencies are
available on the compute node. Adjust the script for your cluster if
needed.

## Results and Debug Artifacts

Typical per-seed outputs include:

-   `result.json` --- structured pass/fail outcome
-   `results.xml` --- test results in XML format
-   `log.txt` --- simulator and test log
-   `coverage.json` --- per-seed coverage data
-   `waveform.vcd` --- waveform for debugging

Aggregated outputs include:

-   `summary.json` --- total, passed, and failed runs
-   `classification_report.json` --- classification counts
-   `triage_report.md` --- AI-assisted diagnosis (check the current
    output format; the validated report was JSON-formatted despite the
    `.md` extension)

A coverage script is available to aggregate and print coverage
information. A persistent aggregate `coverage_report.json` was not
confirmed in the validated artifact set.

For a recruiter-friendly repository, commit concise summaries and one
useful waveform or screenshot rather than every generated log and VCD
file.

## Gemini API Configuration

Set the API key in your shell environment when AI triage is required:

``` bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Never commit API keys, `.env` files containing secrets, credentials, or
tokens. If an API request fails, verify that the environment variable is
set without printing its value.

## Current Scope and Limitations

-   The validated design is a FIFO and the demonstrated fault is a
    specific write-when-full overflow bug.
-   Results depend on the assertions, stimulus, and scenarios
    implemented in the testbench.
-   AI-generated root-cause analysis is advisory and should be checked
    against the RTL, testbench, and design specification.
-   The validated SLURM runs used 20 seeds per mode; runtime and
    behavior may vary across machines and configurations.

## Potential Next Steps

-   Persist aggregate coverage in a machine-readable report.
-   Reuse a compiled simulator binary to reduce per-seed build overhead,
    where supported by the simulation flow.
-   Add more RTL blocks and fault-injection scenarios.
-   Add CI automation for repeatable regression runs.
-   Validate AI triage output against structured fields and retain the
    raw model response for auditability.

## Author

**Jayanta Chakraborty**

*RTL verification · Digital design · Regression automation · AI-assisted
debugging*
