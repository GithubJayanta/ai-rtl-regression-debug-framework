#!/bin/bash
#SBATCH --job-name=fifo_regr
#SBATCH --array=1-20
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --output=runs/slurm_%A_%a.out

cd "$SLURM_SUBMIT_DIR"
source "${VENV:-$HOME/.venv}/bin/activate"
which verilator
python triage/run_one.py "$SLURM_ARRAY_TASK_ID" --bug
