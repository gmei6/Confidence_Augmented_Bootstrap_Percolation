"""Calibrate GIRG's w_min so its realised mean degree matches the configuration
model's realised mean degree (task C2, companion to calibrate_matched_degree.py).

GIRG (`src/twocascade/girg.py`) has no direct mean-degree knob. Mean degree is an
EMERGENT CONSEQUENCE of (tau, w_min, alpha_g, n): given n, tau, alpha_g, the only
lever left is w_min, the power-law weight floor fed to `sample_powerlaw_weights`.
This script bisects w_min until GIRG's realised mean degree lands on the
configuration model's realised mean degree, read from
`results/processed/matched_degree_calibration.json` ->
`configuration_model.realised_mean_degree` (the post-erasure figure that graph
actually carries, not the drawn degree sequence -- see calibrate_matched_degree.py
for why that distinction matters there too).

Heavy-tail caveat: at tau=2.5 the power-law weight distribution has a heavy second
moment (tau < 3), so replicate-to-replicate variance in the realised mean degree is
real, not sampling noise to be argued away. That is exactly why
`measure_girg_degree` never reports a single graph's degree: it averages over a
FIXED set of `replicates` independent graphs (deterministic given base_seed) and
reports the standard error of that mean. The bisection tolerance should be judged
against this se, not against zero.

Tolerance default: measured in practice (n=10000, 20 replicates, base_seed
20260802) the GIRG-side se is ~0.08 -- roughly 3x the configuration-model
target's se (~0.026), because GIRG's heavy-tailed weights feed the degree of
every node rather than being partially clipped the way the configuration
model's d_min/erasure pipeline clips its tail. `--tol 0.02` therefore sits WELL
below the measurement noise floor: bisection to that tolerance pins the
replicate-set mean, and the solved w_min inherits the noise of that mean.
Validate any solved w_min on an independent base_seed before treating the match
as real (done for the committed calibration: independent 20-replicate check at
base_seed=31415 gave <k> = 4.638 +/- 0.125, z = +0.84 vs target). Tighter
tolerances would demand more replicates to be meaningful, not more bisection
iterations.

Seeding discipline mirrors runner.py:121-130 / calibrate_matched_degree.py: each
replicate gets its own SeedSequence child of `base_seed`, which is then split into
two independent streams -- `rng_graph` for the torus points and power-law weights
(drawn in that order, matching runner.py:150-152's girg branch) and `rng_pair` for
the GIRG edge draws. Because the seed derivation depends only on (base_seed,
replicates) and not on w_min, `measure_girg_degree` is a deterministic function of
w_min alone at fixed (n, tau, alpha_g, replicates, base_seed): re-evaluating it at
the same w_min during bisection reuses the exact same `replicates` graphs' point
and weight draws (edge draws differ, since GIRG connection probabilities depend on
w_min), so the objective the solver bisects on has no seed drift across iterations.

Usage:
    arch -arm64 python3 scripts/calibrate_girg_degree.py
    arch -arm64 python3 scripts/calibrate_girg_degree.py --n 2000 --replicates 6
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from twocascade.girg import (
    sample_torus_points,
    sample_powerlaw_weights,
    sample_girg_adjacency,
)


def git_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def measure_girg_degree(n, tau, w_min, alpha_g, replicates, base_seed):
    """Mean GIRG degree, averaged over `replicates` independent graphs.

    Each replicate spawns its own SeedSequence child of `base_seed`, then splits
    into `rng_graph` (torus points, then power-law weights -- same order as
    runner.py's girg branch) and `rng_pair` (GIRG edge draws), matching the
    runner's rng_graph / rng_pair separation (runner.py:121-130). Uses the fast
    block-vectorized `sample_girg_adjacency`, never the O(n^2) reference loop.

    Deterministic given (n, tau, w_min, alpha_g, replicates, base_seed): the same
    inputs always reproduce the same graphs and the same result.

    Returns (realised_mean, realised_se) where realised_mean is the mean over
    replicates of each graph's own mean(len(adj[i]) for i in range(n)), and
    realised_se is the standard error of that mean (std with ddof=1, over
    sqrt(replicates)). tau=2.5 gives a heavy-tailed weight distribution, so this
    se is a real, load-bearing quantity -- not a formality.
    """
    means = []
    for child in np.random.SeedSequence(base_seed).spawn(replicates):
        rng_graph, rng_pair = (np.random.default_rng(s) for s in child.spawn(2))
        points = sample_torus_points(n, rng_graph)
        weights = sample_powerlaw_weights(n, tau, w_min, rng_graph)
        adj = sample_girg_adjacency(points, weights, alpha_g, rng_pair)
        means.append(float(np.mean([len(a) for a in adj])))

    arr = np.array(means)
    realised_mean = float(arr.mean())
    realised_se = float(arr.std(ddof=1) / np.sqrt(len(arr)))
    return realised_mean, realised_se


def solve_w_min(target, n, tau, alpha_g, replicates, base_seed, tol, w_lo, w_hi, max_iter):
    """Bisect w_min so measure_girg_degree(..., w_min, ...) lands within tol of target.

    Mean GIRG degree is monotone increasing in w_min (larger weight floor -> larger
    connection probabilities everywhere), so ordinary bisection applies. Every
    candidate w_min is measured with the SAME (n, tau, alpha_g, replicates,
    base_seed) -- so, per measure_girg_degree's docstring, the same replicate
    point/weight draws recur at every iteration and only the edges (which depend
    on w_min) differ. The objective is therefore a deterministic function of
    w_min alone; there is no seed drift across bisection iterations.

    Before bisecting, verifies the bracket [w_lo, w_hi] actually straddles target
    by measuring both endpoints. If it doesn't, returns converged=False with the
    endpoint measurements attached as diagnostics rather than extrapolating
    outside a range the sampler was never evaluated on.

    Returns a dict with keys: w_min, achieved_mean_degree, achieved_se,
    iterations, converged, target, w_lo, w_hi, mean_at_w_lo, se_at_w_lo,
    mean_at_w_hi, se_at_w_hi, trace (list of per-evaluation dicts, each with
    iteration, w_min, achieved_mean_degree, achieved_se).
    """
    trace = []

    mean_lo, se_lo = measure_girg_degree(n, tau, w_lo, alpha_g, replicates, base_seed)
    trace.append({"iteration": 0, "w_min": w_lo, "achieved_mean_degree": mean_lo,
                   "achieved_se": se_lo, "note": "bracket_lo"})
    mean_hi, se_hi = measure_girg_degree(n, tau, w_hi, alpha_g, replicates, base_seed)
    trace.append({"iteration": 0, "w_min": w_hi, "achieved_mean_degree": mean_hi,
                   "achieved_se": se_hi, "note": "bracket_hi"})

    result = {
        "target": target,
        "w_lo": w_lo, "w_hi": w_hi,
        "mean_at_w_lo": mean_lo, "se_at_w_lo": se_lo,
        "mean_at_w_hi": mean_hi, "se_at_w_hi": se_hi,
        "trace": trace,
    }

    if not (mean_lo <= target <= mean_hi):
        result.update({
            "w_min": None,
            "achieved_mean_degree": None,
            "achieved_se": None,
            "iterations": 0,
            "converged": False,
            "diagnostics": (
                f"target {target} not bracketed: mean(w_lo={w_lo}) = {mean_lo:.4f}, "
                f"mean(w_hi={w_hi}) = {mean_hi:.4f}. Widen [w_lo, w_hi]."
            ),
        })
        return result

    lo, hi = w_lo, w_hi
    mid = w_lo
    mean_mid, se_mid = mean_lo, se_lo
    converged = False
    it = 0
    for it in range(1, max_iter + 1):
        mid = 0.5 * (lo + hi)
        mean_mid, se_mid = measure_girg_degree(n, tau, mid, alpha_g, replicates, base_seed)
        trace.append({"iteration": it, "w_min": mid, "achieved_mean_degree": mean_mid,
                       "achieved_se": se_mid})
        if abs(mean_mid - target) <= tol:
            converged = True
            break
        if mean_mid < target:
            lo = mid
        else:
            hi = mid

    result.update({
        "w_min": mid,
        "achieved_mean_degree": mean_mid,
        "achieved_se": se_mid,
        "iterations": it,
        "converged": converged,
        "trace": trace,
    })
    return result


def main():
    ap = argparse.ArgumentParser(
        description="Calibrate GIRG's w_min to match the configuration model's "
                     "realised mean degree (task C2)."
    )
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--tau", type=float, default=2.5)
    ap.add_argument("--alpha-g", type=float, default=1.2)
    ap.add_argument("--replicates", type=int, default=20)
    ap.add_argument("--base-seed", type=int, default=20260802)
    ap.add_argument("--tol", type=float, default=0.02,
                     help="Bisection tolerance on achieved mean degree. Default 0.02 "
                          "sits well below the ~0.08 measurement se at n=10000 with "
                          "20 replicates (see docstring): it pins the replicate-set "
                          "mean; validate on an independent base_seed.")
    ap.add_argument("--w-lo", type=float, default=0.1)
    ap.add_argument("--w-hi", type=float, default=3.0)
    ap.add_argument("--max-iter", type=int, default=30)
    ap.add_argument(
        "--calibration-in",
        default="results/processed/matched_degree_calibration.json",
        help="repo-relative path to the configuration-model calibration JSON "
             "(source of the target mean degree)",
    )
    ap.add_argument(
        "--out",
        default="results/processed/girg_degree_calibration.json",
        help="repo-relative output path",
    )
    args = ap.parse_args()

    cal_path = os.path.join(REPO_ROOT, args.calibration_in)
    if not os.path.exists(cal_path):
        raise FileNotFoundError(
            f"Calibration input not found: {args.calibration_in}\n"
            f"Run scripts/calibrate_matched_degree.py first to produce it."
        )
    with open(cal_path) as f:
        cal = json.load(f)
    cm = cal["configuration_model"]
    target = cm["realised_mean_degree"]
    target_se = cm["realised_se"]

    print(f"GIRG w_min calibration  tau={args.tau} alpha_g={args.alpha_g} n={args.n} "
          f"({args.replicates} replicates, base_seed={args.base_seed})")
    print(f"  target <k> (configuration model, realised) = {target:.5f} +/- {target_se:.5f}")
    print(f"  source: {args.calibration_in}")
    print()

    result = solve_w_min(
        target, args.n, args.tau, args.alpha_g, args.replicates, args.base_seed,
        args.tol, args.w_lo, args.w_hi, args.max_iter,
    )

    if not result["converged"]:
        print("  DID NOT CONVERGE")
        if result.get("w_min") is None:
            print(f"  {result['diagnostics']}")
        else:
            print(f"  best w_min = {result['w_min']:.6f}  "
                  f"achieved <k> = {result['achieved_mean_degree']:.4f} "
                  f"+/- {result['achieved_se']:.4f}  "
                  f"(residual {result['achieved_mean_degree'] - target:+.4f}, "
                  f"iterations={result['iterations']})")
    else:
        residual = result["achieved_mean_degree"] - target
        print(f"  solved w_min          = {result['w_min']:.6f}")
        print(f"  achieved <k>          = {result['achieved_mean_degree']:.4f} "
              f"+/- {result['achieved_se']:.4f}")
        print(f"  residual (achieved-target) = {residual:+.4f}")
        print(f"  iterations            = {result['iterations']}")

    payload = {
        "metadata": {
            "script": "scripts/calibrate_girg_degree.py",
            "git_commit": git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "base_seed": args.base_seed,
            "replicates": args.replicates,
            "tol": args.tol,
        },
        "girg": {
            "n": args.n,
            "tau": args.tau,
            "alpha_g": args.alpha_g,
            "w_min": result["w_min"],
            "achieved_mean_degree": result["achieved_mean_degree"],
            "achieved_se": result["achieved_se"],
            "iterations": result["iterations"],
            "converged": result["converged"],
            "w_lo": args.w_lo, "w_hi": args.w_hi,
            "mean_at_w_lo": result["mean_at_w_lo"],
            "mean_at_w_hi": result["mean_at_w_hi"],
            "trace": result["trace"],
        },
        "target": {
            "source": args.calibration_in,
            "cm_realised_mean_degree": target,
            "cm_realised_se": target_se,
        },
    }

    out_path = os.path.join(REPO_ROOT, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
