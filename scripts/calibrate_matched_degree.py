"""Calibrate the matched mean degree for the D-038 poster comparison (task T1).

The two comparison families set their mean degree by completely different means:

  * Erdos-Renyi           <k> is a KNOB. beta = target_mean_degree / n_ref^(1-alpha),
                          p = beta * n^(-alpha), so <k> = (n-1)p lands on the target
                          at n = n_ref (model.py:52-64).
  * configuration model   <k> is an EMERGENT CONSEQUENCE of (tau, d_min), and erasure
                          of self-loops and multi-edges then shaves it further. There
                          is no knob.

So "same n, same average degree" is not two numbers set equal. This script measures the
configuration model's realised post-erasure mean degree over several graph replicates,
then solves the Erdos-Renyi target_mean_degree that reproduces it at the same n.

Two traps this exists to avoid:

  1. The configuration-model configs carry `scaling.target_mean_degree: 4.0`, which is
     NOT that family's mean degree -- on that path the runner computes `p` and then
     ignores it, and the value survives only to normalise janson_a_c for seed_multiples.
     Reading 4.0 as "the config model runs at <k> = 4" is a quiet, plausible-looking error.
  2. Erasure is not negligible: at tau=2.5 it costs about 0.09 of a degree. Matching the
     DRAWN mean rather than the REALISED mean biases the comparison by roughly 2%.

Also note the match holds at ONE n. Erdos-Renyi's mean degree is deliberately n-dependent
(the Janson regime, alpha=0.6, D-004) while the configuration model's is flat in n, so a
single beta matches the families at n = n_ref and nowhere else. The poster comparison is
pinned to a single n for exactly this reason.

Usage:
    arch -arm64 python3 scripts/calibrate_matched_degree.py
    arch -arm64 python3 scripts/calibrate_matched_degree.py --n 20000 --tau 2.3
"""

import argparse
import json
import os
import subprocess
import sys
import datetime

import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from twocascade.graphs import sample_powerlaw_degrees, sample_configuration_model
from twocascade.model import calculate_beta, calculate_p_n


def git_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def measure_config_model_degree(n, tau, d_min, replicates, base_seed):
    """Mean degree of the erased configuration model, over independent graphs.

    Returns (drawn_mean, drawn_se, realised_mean, realised_se). The realised value is
    the one to match: it is the graph the cascade actually traverses.
    """
    drawn, realised = [], []
    for child in np.random.SeedSequence(base_seed).spawn(replicates):
        # Separate streams for the degree sequence and the stub pairing, matching the
        # runner's RNG discipline (runner.py:121-130).
        rng_graph, rng_pair = (np.random.default_rng(s) for s in child.spawn(2))
        degrees = sample_powerlaw_degrees(n, tau, d_min, rng_graph)
        adjacency = sample_configuration_model(degrees, rng_pair)
        drawn.append(float(np.mean(degrees)))
        realised.append(float(np.mean([len(a) for a in adjacency])))

    def mean_se(xs):
        arr = np.array(xs)
        return float(arr.mean()), float(arr.std(ddof=1) / np.sqrt(len(arr)))

    return (*mean_se(drawn), *mean_se(realised))


def solve_er_target(mean_degree, n, n_ref, alpha):
    """target_mean_degree such that Erdos-Renyi (n-1)p equals mean_degree at this n."""
    target = mean_degree * n / (n - 1)
    p = calculate_p_n(calculate_beta(target, n_ref, alpha), n, alpha)
    return target, p, (n - 1) * p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--tau", type=float, default=2.5)
    ap.add_argument("--d-min", type=int, default=2)
    ap.add_argument("--replicates", type=int, default=20)
    ap.add_argument("--base-seed", type=int, default=20260727)
    ap.add_argument("--alpha", type=float, default=0.6)
    ap.add_argument("--n-ref", type=int, default=10000)
    ap.add_argument(
        "--out",
        default="results/processed/matched_degree_calibration.json",
        help="repo-relative output path",
    )
    args = ap.parse_args()

    drawn, drawn_se, realised, realised_se = measure_config_model_degree(
        args.n, args.tau, args.d_min, args.replicates, args.base_seed
    )
    target, p, er_realised = solve_er_target(realised, args.n, args.n_ref, args.alpha)

    print(f"configuration model  tau={args.tau} d_min={args.d_min} n={args.n} "
          f"({args.replicates} replicates, base_seed={args.base_seed})")
    print(f"  drawn     <k> = {drawn:.4f} +/- {drawn_se:.4f}")
    print(f"  REALISED  <k> = {realised:.4f} +/- {realised_se:.4f}   <-- the match target")
    print(f"  erasure loss  = {drawn - realised:.4f}")
    print()
    print(f"Erdos-Renyi matched at n={args.n}, alpha={args.alpha}, n_ref={args.n_ref}")
    print(f"  target_mean_degree = {target:.4f}")
    print(f"  p                  = {p:.10f}")
    print(f"  (n-1)p             = {er_realised:.4f}  "
          f"(residual {er_realised - realised:+.2e})")

    payload = {
        "metadata": {
            "script": "scripts/calibrate_matched_degree.py",
            "git_commit": git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "base_seed": args.base_seed,
            "replicates": args.replicates,
        },
        "configuration_model": {
            "n": args.n, "tau": args.tau, "d_min": args.d_min,
            "drawn_mean_degree": drawn, "drawn_se": drawn_se,
            "realised_mean_degree": realised, "realised_se": realised_se,
            "erasure_loss": drawn - realised,
        },
        "erdos_renyi_matched": {
            "n": args.n, "alpha": args.alpha, "n_ref": args.n_ref,
            "target_mean_degree": target, "p": p,
            "realised_mean_degree": er_realised,
        },
    }

    out_path = os.path.join(REPO_ROOT, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
