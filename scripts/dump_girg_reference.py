#!/usr/bin/env python3
"""Dump shared GIRG points/weights for Python<->C++ cross-validation (cpp-girg-plan G1/G5).

Both the exact-probability check and the sampled-graph/level-set checks need
the C++ side and the Python side to evaluate on IDENTICAL geometry and
weights -- RNG streams differ across languages (numpy Generator vs
std::mt19937_64, constitution §5.4's explicit non-goal), so any comparison
that samples points/weights independently in each language would be
comparing apples to oranges before the sampler under test is even reached.

This script draws points/weights ONCE, from the Python oracle's own point/
weight samplers (twocascade.girg.sample_torus_points /
sample_powerlaw_weights -- these are not themselves under validation here,
only the adjacency samplers built on top of them are), and writes them in a
plain-text format the C++ binary's `--girg-verify` mode reads directly:

  <out>/points.txt   : n lines "x y"
  <out>/weights.txt  : n lines "w"
  <out>/meta.txt      : the parameters used, for provenance

Usage:
  python scripts/dump_girg_reference.py --n 200 --tau 2.5 --w-min 0.245 \
      --alpha-g 1.2 --base-seed 0 --out results/raw/xval/girg
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import numpy as np

from twocascade.girg import sample_torus_points, sample_powerlaw_weights

REPO_ROOT = Path(__file__).resolve().parent.parent


def git_commit_hash() -> str:
    """Same helper shape as scripts/calibrate_matched_degree.py and
    runner.get_git_commit_hash: never raises, degrades to 'unknown'."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, required=True, help="number of points")
    ap.add_argument("--tau", type=float, default=2.5, help="power-law exponent")
    ap.add_argument("--w-min", type=float, default=0.186377, help="minimum weight")
    ap.add_argument("--alpha-g", type=float, default=1.2, help="GIRG kernel exponent")
    ap.add_argument("--base-seed", type=int, default=0, help="RNG base seed (reproducible)")
    ap.add_argument("--out", type=Path, default=Path("results/raw/xval/girg"), help="output dir")
    args = ap.parse_args()

    rng = np.random.default_rng(args.base_seed)
    points = sample_torus_points(args.n, rng)
    weights = sample_powerlaw_weights(args.n, args.tau, args.w_min, rng)

    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    # %.17g round-trips a double exactly; both languages must see the same bits.
    np.savetxt(out / "points.txt", points, fmt="%.17g")
    np.savetxt(out / "weights.txt", weights.reshape(-1, 1), fmt="%.17g")

    # git_commit is part of the provenance contract, not decoration: without it
    # a points.txt/weights.txt pair cannot be tied back to the sampler revision
    # that produced it, and these fixtures outlive the test run that made them.
    (out / "meta.txt").write_text(
        f"n={args.n} tau={args.tau} w_min={args.w_min} alpha_g={args.alpha_g} "
        f"base_seed={args.base_seed} git_commit={git_commit_hash()}\n"
    )

    print(
        f"n={args.n} tau={args.tau} w_min={args.w_min} alpha_g={args.alpha_g} "
        f"base_seed={args.base_seed} -> {out}/"
    )


if __name__ == "__main__":
    main()
