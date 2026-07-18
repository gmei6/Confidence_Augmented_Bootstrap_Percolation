"""
S-051 overnight batch driver. Runs the two config-only, no-src-changes tasks
queued in docs/queue/ (Task S, Task T) sequentially, skipping any step whose
output already exists, and continuing past failures (each step's error is
reported in the final summary instead of aborting the batch).

Deliberately excludes Task Q (epsilon-cap sampler fix) and Task R (cross-round
remote-ignition tracker): both require new/changed code (src/twocascade/graphs.py
for Q; a new analysis script for R) and are flagged in their task files as
needing human review before anything runs, per AGENTS.md "Propose, don't write".

Launch (note the arm64 requirement on this machine - see okf/lessons.md):

    nohup arch -arm64 python3 scripts/run_overnight_s051.py > overnight_s051.log 2>&1 &

Steps:
  1. Task S: Q4(iii) ignition gate, wider n-grid at n=40000            -> results/q4_ignition_tau25_n40000_raw.json
  2. Task S: Q4(iii) ignition gate, wider n-grid at n=80000            -> results/q4_ignition_tau25_n80000_raw.json
  3. Task T: Q3 finite-size nu, extended n=20000 (C++ engine)          -> results/raw/finite_size_r2_n20000.json
"""

import json
import os
import sys
import time

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep


def sweep_step(config_rel):
    """Run one run_sweep config unless its output already exists."""
    cfg_path = os.path.join(base_dir, config_rel)
    with open(cfg_path) as f:
        out_rel = json.load(f)["output"]["raw_filepath"]
    if os.path.exists(os.path.join(base_dir, out_rel)):
        print(f"  SKIP {config_rel}: {out_rel} exists")
        return
    print(f"  RUN  {config_rel}")
    run_sweep(cfg_path)


STEPS = [
    ("task-S q4-ignition tau=2.5 n=40000", lambda: sweep_step("configs/q4_ignition_tau25_n40000.json")),
    ("task-S q4-ignition tau=2.5 n=80000", lambda: sweep_step("configs/q4_ignition_tau25_n80000.json")),
    ("task-T q3 finite-size nu n=20000 (cpp)", lambda: sweep_step("configs/finite_size_r2_n20000.json")),
]


def main():
    summary = []
    for name, step in STEPS:
        print(f"\n=== STEP: {name} ===")
        t0 = time.time()
        try:
            step()
            summary.append((name, "OK", time.time() - t0))
        except Exception as e:
            summary.append((name, f"FAILED: {e}", time.time() - t0))
            print(f"  STEP FAILED (continuing): {e}")

    print("\n=== S-051 BATCH SUMMARY ===")
    failed = 0
    for name, status, dt in summary:
        print(f"  [{status.split(':')[0]:>6s}] {name} ({dt/60:.1f} min)"
              + ("" if status == "OK" else f" - {status}"))
        failed += status != "OK"
    print(f"{len(summary) - failed}/{len(summary)} steps succeeded")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
