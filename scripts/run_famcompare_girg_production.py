"""Run the Fear Amplifies cross-family comparison GIRG production sweeps.

Three arms at n in {4000, 10000, 20000}, each holding a bounded seed a=r=2
fixed and sweeping mean_fear_grid = [0, 0.1, 0.2, 0.3, 0.4] -- mirroring the
existing q4_ignition_tau25_mumap_n{n}.json configuration-model series exactly
(same seed methodology, same mu grid, same trials_per_cell=500, same
base_seed=42), so the only difference between the CM and GIRG arms is
geometry. Per-n w_min values come from scripts/calibrate_girg_degree.py,
matching each n's configuration-model realised mean degree
(results/processed/matched_degree_calibration_n{n}.json).

GIRG sampling is O(n^2); the n=20000 arm alone is multi-hour. Must be a real
script file, not stdin (macOS spawn re-imports __main__ for multiprocessing).

Usage:
    nohup arch -arm64 python3 scripts/run_famcompare_girg_production.py \
        > /tmp/fear_amplifies_logs/girg_production.log 2>&1 &
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from twocascade.runner import run_sweep, get_git_commit_hash

CONFIGS = [
    "configs/famcompare_girg_n4000.json",
    "configs/famcompare_girg_n10000.json",
    "configs/famcompare_girg_n20000.json",
]

if __name__ == "__main__":
    print(f"git commit: {get_git_commit_hash()}", flush=True)
    t0 = time.time()
    for cfg in CONFIGS:
        t = time.time()
        print(f"=== {cfg} ===", flush=True)
        run_sweep(cfg)
        print(f"    done in {time.time() - t:.0f}s (total {time.time() - t0:.0f}s)", flush=True)
    print("ALL FAMCOMPARE GIRG PRODUCTION ARMS DONE", flush=True)
