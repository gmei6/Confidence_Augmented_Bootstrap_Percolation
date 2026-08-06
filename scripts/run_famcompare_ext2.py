"""Run the famcompare mu_bar in {0.8, 0.9, 1.0} extension sweep (Gary, 2026-08-06).

Pushes the "effect of fear" probability figure (scripts/plot_famcompare_probability.py)
past mu_bar=0.7 into the regime where R_fear approaches its own subcriticality
threshold (okf/lessons.md, "Subcriticality of Fear"). Fresh base_seed per config
(20260806/07/08), distinct from the base/ext files' base_seed=42, so these new
cells don't share an RNG substream with the existing mu_bar=0.0/0.5-0.7 cells
(see analyze_famcompare.py's RNG-STREAM NOTE for the collision this avoids).
"""
import os
import sys
import time

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep, get_git_commit_hash

CONFIGS = [
    "famcompare_er_bounded_n10000_ext2",
    "famcompare_cm_matched_n10000_ext2",
    "famcompare_girg_n10000_ext2",
]


def main() -> None:
    os.chdir(base_dir)
    print(f"repo root : {base_dir}", flush=True)
    print(f"git commit: {get_git_commit_hash()}", flush=True)

    t0 = time.time()
    for name in CONFIGS:
        cfg_path = os.path.join(base_dir, "configs", f"{name}.json")
        if not os.path.exists(cfg_path):
            raise FileNotFoundError(f"Config file not found at {cfg_path}")
        t1 = time.time()
        print(f"[{time.time() - t0:7.0f}s] running {name}.json ...", flush=True)
        run_sweep(cfg_path)
        print(
            f"[{time.time() - t0:7.0f}s] done {name}.json in {time.time() - t1:.0f}s",
            flush=True,
        )
    print(f"[{time.time() - t0:7.0f}s] ALL DONE", flush=True)


if __name__ == "__main__":
    main()
