"""
S-047 overnight batch driver. Runs the queued unattended compute sequentially,
cheapest first, skipping any step whose output already exists, and continuing
past failures (each step's error is reported in the final summary instead of
aborting the batch).

Launch (note the arm64 requirement on this machine - see okf/lessons.md):

    nohup arch -arm64 python3 scripts/run_overnight_s047.py > overnight_s047.log 2>&1 &

Steps:
  1. Q5 duration dichotomy n-sweep (C-Q5(ii))          -> results/q5_duration_raw.json
  2. Q4 bounded-seed ignition gates (C-Q4(iii))        -> results/q4_ignition_*_raw.json
  3. Task E history regen + Task H clock-bias analysis -> results/raw/fear_concentration_*,
                                                          results/figures/clock_collapse_bias.png
  4. Q4 Phase 2 tilt grid at n=10000 + tau=3.5 gate    -> results/q4_phase2_*_raw.json
  5. Q3 finite-size nu at n=10000 (C++ engine)         -> results/raw/finite_size_r2_n10000.json
"""

import json
import os
import subprocess
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


def script_step(script_rel):
    """Run a standalone scripts/*.py as a subprocess with this interpreter."""
    print(f"  RUN  {script_rel}")
    subprocess.run([sys.executable, os.path.join(base_dir, script_rel)], check=True)


STEPS = [
    ("q5-duration (C-Q5(ii))", lambda: script_step("scripts/run_task_o_duration.py")),
    ("q4-ignition tau=2.5/3.5 x n (C-Q4(iii))", lambda: [
        sweep_step(f"configs/q4_ignition_{t}_n{n}.json")
        for t in ("tau25", "tau35") for n in (4000, 10000, 20000)]),
    ("task-e history regen + task-h clock bias", lambda: (
        script_step("scripts/run_task_e.py"),
        script_step("scripts/run_task_h.py"))),
    ("q4-phase2 tilt grid n=10000 + tau=3.5 gate", lambda: [
        sweep_step(f"configs/{c}.json") for c in (
            "q4_phase2_n10000_gammaneg1", "q4_phase2_n10000_gamma0",
            "q4_phase2_n10000_gammapos1", "q4_phase2_n10000_tau35_gamma0")]),
    ("q3 finite-size nu n=10000 (cpp)", lambda: sweep_step("configs/finite_size_r2_n10000.json")),
]


def main():
    # The duration sweep at n=32000 and the n=10000 tilt grid are the long
    # poles; everything is sequential so one failure cannot corrupt another.
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

    print("\n=== OVERNIGHT SUMMARY ===")
    failed = 0
    for name, status, dt in summary:
        print(f"  [{status.split(':')[0]:>6s}] {name} ({dt/60:.1f} min)"
              + ("" if status == "OK" else f" - {status}"))
        failed += status != "OK"
    print(f"{len(summary) - failed}/{len(summary)} steps succeeded")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
