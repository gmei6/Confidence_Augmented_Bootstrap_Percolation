"""Run the Q4 P(systemic) cascade-boundary sweep tau_c(mu, n) at seed size a=8.

Drives the sanctioned runner (twocascade.runner.run_sweep) over the 28 committed
configs configs/q4_psys_boundary_n{n}_tau{tag}.json.

Design (fixed in the configs, restated here for the record):
  configuration model, d_min=2, r=2, kappa=50, theta=0.5, window_len=5,
  weights=[0.2]*5, gamma=0, target_high_degree=False,
  scaling {target_mean_degree 4.0, n_ref 10000, alpha 0.6}, engine "python".
  tau  in {2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5}
  mu   in {0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9}
  n    in {2000, 4000, 8000, 16000}
  500 trials/cell, base_seed=42  ->  196 cells, 98,000 runs.

The runner owns all output: it writes results/q4_psys_boundary_*_raw.json and
stamps each file with the seed, parameter tuple, and git commit hash. Nothing is
hand-written into results/. Run this from the repository root (the script also
chdir's there) so the git stamp resolves to the real HEAD and the config's
repo-relative raw_filepath lands in results/.

Usage:
    python scripts/run_q4_psys_boundary.py            # all 28 configs
    python scripts/run_q4_psys_boundary.py 2000 4000  # only these n
"""

import os
import sys
import time

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep, get_git_commit_hash

N_LIST = [2000, 4000, 8000, 16000]
TAU_TAGS = ["2p3", "2p5", "2p7", "2p9", "3p1", "3p3", "3p5"]


def main() -> None:
    os.chdir(base_dir)
    only_n = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else N_LIST

    print(f"repo root : {base_dir}", flush=True)
    print(f"git commit: {get_git_commit_hash()}", flush=True)

    t0 = time.time()
    for n in only_n:
        for tag in TAU_TAGS:
            name = f"q4_psys_boundary_n{n}_tau{tag}.json"
            cfg_path = os.path.join(base_dir, "configs", name)
            if not os.path.exists(cfg_path):
                raise FileNotFoundError(f"Config file not found at {cfg_path}")
            t1 = time.time()
            print(f"[{time.time() - t0:7.0f}s] running {name} ...", flush=True)
            run_sweep(cfg_path)
            print(f"[{time.time() - t0:7.0f}s] done {name} in {time.time() - t1:.0f}s",
                  flush=True)

    print(f"[{time.time() - t0:7.0f}s] ALL DONE", flush=True)


if __name__ == "__main__":
    main()
