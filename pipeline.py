#!/usr/bin/env python3
"""
pipeline.py
-----------
Orchestrates the entire DAPO workflow in fresh processes:

1) generator.py       -> Creates artifacts/experiment_results.csv
2) judge.py           -> Chooses best prompt & merges refinements, writes artifacts/best_prompt.json
3) executioner.py     -> Uses ultimate prompt to produce a final Requirements Analysis and logs it
4) jury.py            -> Re-checks entire dataset (including the 'ultimate' entry) for final commentary

Logs output and errors in real time for debugging.
"""

import subprocess
import time
import os
import sys
from datetime import datetime

# Optionally allow overriding Python interpreter
PYTHON_EXEC = sys.executable  # Uses the same Python as the script is running

def log_message(msg, error=False):
    """Logs a message with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_type = "❌ ERROR" if error else "ℹ️ INFO"
    print(f"[{timestamp}] {log_type}: {msg}")

def run_step(script, description):
    """Executes a pipeline step with improved logging and real-time streaming."""
    log_message(f"🚀 Running {script} -> {description}")

    start_time = time.time()
    try:
        with subprocess.Popen(
            [PYTHON_EXEC, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ) as proc:
            # Stream stdout
            for line in proc.stdout:
                print(f"[{script}]: {line.strip()}")

            proc.wait()  # Wait for script completion

            elapsed_time = time.time() - start_time
            if proc.returncode == 0:
                log_message(f"✅ {script} completed successfully in {elapsed_time:.2f} seconds.\n")
            else:
                log_message(f"⚠️ WARNING: {script} failed with exit code {proc.returncode}. Continuing pipeline...", error=True)
                log_message(f"🔍 Standard Error Output:\n{proc.stderr.read()}", error=True)

    except Exception as e:
        log_message(f"❌ Unexpected error while running {script}: {e}", error=True)
        sys.exit(1)

def main():
    log_message("🚀 Starting the full DAPO pipeline...\n")

    steps = [
        ("generator.py",       "Generate 36 prompt variations"),
        ("judge.py",           "Judge picks best prompt & merges refinements"),
        ("executioner.py",     "Execute ultimate prompt for final Requirements Analysis"),
        ("jury.py",            "Perform final analysis on all results")
    ]

    for i, (script, description) in enumerate(steps, start=1):
        log_message(f"{i}/{len(steps)}: {description}")
        run_step(script, description)

        # Optional sleep (adjust if API rate limits apply)
        if i < len(steps):
            time.sleep(1)  # Reduce wait time for efficiency

    # Attempt to display a snippet of the final analysis
    final_report_path = os.path.join("artifacts", "final_analysis_report.md")
    if os.path.isfile(final_report_path):
        with open(final_report_path, "r") as f:
            analysis_text = f.read()
        log_message(f"\n✅ Pipeline complete! Final analysis from '{final_report_path}':\n")
        # Print the first ~700 characters for a quick preview
        print(analysis_text[:700], "...\n")
    else:
        log_message(f"\n❌ {final_report_path} not found. Check jury.py output.", error=True)

if __name__ == "__main__":
    main()
