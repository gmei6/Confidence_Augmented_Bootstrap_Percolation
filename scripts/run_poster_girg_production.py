"""Run the C3b GIRG production sweeps (poster Comparison 2, 500 trials/cell).

Grids refined from the pilot (results/poster_girg_mu*_pilot_raw.json): transitions
sit at a_c ~ 10.5 / 6.6 / 4.5 for mu-bar 0 / 0.4 / 0.7, so each grid densifies
a in [1, 48] around its own transition. Runs on the progress-instrumented runner
(C3b-obs) so the log streams `progress: N/M` lines.

Must be a real script file, not stdin (macOS spawn re-imports __main__).

Usage:
    arch -arm64 python3 scripts/run_poster_girg_production.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from twocascade.runner import run_sweep

CONFIGS = [
    "configs/poster_girg_mu0.json",
    "configs/poster_girg_mu40.json",
    "configs/poster_girg_mu70.json",
]

if __name__ == "__main__":
    for cfg in CONFIGS:
        t = time.time()
        print(f"=== {cfg} ===", flush=True)
        run_sweep(cfg)
        print(f"    done in {time.time() - t:.0f}s", flush=True)
    print("ALL PRODUCTION ARMS DONE")
