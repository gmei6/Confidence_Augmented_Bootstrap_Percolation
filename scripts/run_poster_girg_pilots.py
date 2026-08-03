"""Run the C3b GIRG pilot sweeps (poster Comparison 2 bracket run).

Three arms at mu-bar in {0, 0.4, 0.7}, log-spaced seed grid 2..256, 100
trials/cell, n=10000 -- a bracket run to locate GIRG's a_c before the 500-trial
production grids. Configs are byte-level copies of the CM arms except the graph
block (girg, tau=2.5, calibrated w_min=0.186377, alpha_g=1.2), so geometry is
the only difference between the families.

Must be a real script file, not stdin: run_sweep uses multiprocessing.Pool and
macOS spawn re-imports __main__, which fails for '<stdin>' (measured 2026-08-02
-- 512KB of FileNotFoundError tracebacks, zero trials completed).

Usage:
    arch -arm64 python3 scripts/run_poster_girg_pilots.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from twocascade.runner import run_sweep

CONFIGS = [
    "configs/poster_girg_mu0_pilot.json",
    "configs/poster_girg_mu40_pilot.json",
    "configs/poster_girg_mu70_pilot.json",
]

if __name__ == "__main__":
    for cfg in CONFIGS:
        t = time.time()
        print(f"=== {cfg} ===", flush=True)
        run_sweep(cfg)
        print(f"    done in {time.time() - t:.0f}s", flush=True)
    print("ALL PILOT ARMS DONE")
