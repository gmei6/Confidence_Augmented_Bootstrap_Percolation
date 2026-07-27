"""Run the poster comparison sweep — Erdős–Rényi vs configuration model."""

import os
import sys
import time

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep, get_git_commit_hash

ALL_CONFIGS = [
    "poster_er_mu0",
    "poster_er_mu40",
    "poster_er_mu70",
    "poster_cm_mu0",
    "poster_cm_mu40",
    "poster_cm_mu70",
]


def main() -> None:
    os.chdir(base_dir)
    requested = sys.argv[1:] if len(sys.argv) > 1 else ALL_CONFIGS

    targets = []
    for req in requested:
        name = os.path.basename(req)
        if name.endswith(".json"):
            name = name[:-5]
        targets.append(name)

    print(f"repo root : {base_dir}", flush=True)
    print(f"git commit: {get_git_commit_hash()}", flush=True)

    t0 = time.time()
    for name in targets:
        cfg_name = f"{name}.json"
        cfg_path = os.path.join(base_dir, "configs", cfg_name)
        if not os.path.exists(cfg_path):
            raise FileNotFoundError(f"Config file not found at {cfg_path}")
        t1 = time.time()
        print(f"[{time.time() - t0:7.0f}s] running {cfg_name} ...", flush=True)
        run_sweep(cfg_path)
        print(
            f"[{time.time() - t0:7.0f}s] done {cfg_name} in {time.time() - t1:.0f}s",
            flush=True,
        )

    print(f"[{time.time() - t0:7.0f}s] ALL DONE", flush=True)


if __name__ == "__main__":
    main()
