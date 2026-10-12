#!/bin/bash
#SBATCH --job-name=rtl-ai-validate
#SBATCH --partition=debug
#SBATCH --output=slurm/logs/%x-%j.out
#SBATCH --error=slurm/logs/%x-%j.err
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=1G

set -Eeuo pipefail

PROJECT_ROOT="${SLURM_SUBMIT_DIR}"
SEEDS="${1:-20}"
MODE="${2:-clean}"

cd "$PROJECT_ROOT"
source "$HOME/.venv/bin/activate"

echo "===== SLURM JOB INFORMATION ====="
echo "Job ID: ${SLURM_JOB_ID}"
echo "Host: $(hostname)"
echo "Mode: $MODE"
echo "Seeds: $SEEDS"
echo "Start: $(date -Is)"

python --version
verilator --version

case "$MODE" in
  clean)
    python triage/run_pipeline.py "$SEEDS" \
      --run-dir "runs/slurm_clean_${SLURM_JOB_ID}"
    ;;
  bug)
    python triage/run_pipeline.py "$SEEDS" \
      --bug \
      --run-dir "runs/slurm_bug_${SLURM_JOB_ID}"
    ;;
  *)
    echo "ERROR: Mode must be clean or bug"
    exit 2
    ;;
esac

echo "===== SLURM JOB FINISHED ====="
echo "End: $(date -Is)"
