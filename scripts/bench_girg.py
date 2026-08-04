"""Benchmark: GIRG adjacency samplers.

Two modes.

DEFAULT (no flags) -- the original within-Python comparison, slow vs fast.

--cross-language -- the cpp-girg-plan's own benchmark (G5.1): Python oracle vs
C++ direct vs C++ BKL over an n-grid, which is the measurement the port exists
to justify and which G0-G5 asserted in prose without ever taking. Requires the
C++ binary; each C++ point is one `--girg-verify bench` invocation, which times
the sampler call ALONE (no file I/O, no point/weight generation) and prints
"variant n seconds edges".

  arch -arm64 python3 scripts/bench_girg.py --cross-language

The two languages sample independent graphs from the SAME model at the same
(tau, w_min, alpha_g, n) -- RNG-stream identity across languages is an explicit
non-goal (constitution §5.4), so the edge counts printed alongside each timing
are the honest check that both are sampling the same distribution, not a
correctness claim in themselves (that is what tests/test_cpp_girg_validation.py
is for).

DEFAULT-mode detail. Times single-graph sampling (fixed seed) for:
  - slow sampler at n=1000 and n=2000 (measured)
  - fast sampler at n=1000, n=2000, n=10000 (measured)
  - slow sampler at n=10000 (extrapolated quadratically from n=2000, not run —
    O(n^2) scalar loop at n=10000 would take on the order of hours)

Then projects sampling-only wall time for an 11-grid-point x 500-trial x
3-fear-arm sweep at n=10000 using the fast sampler.

Run with: arch -arm64 python3 scripts/bench_girg.py
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from twocascade.girg import (
    sample_torus_points,
    sample_powerlaw_weights,
    sample_girg_adjacency,
    sample_girg_adjacency_slow,
)

ALPHA_G = 1.2
TAU = 2.5
W_MIN = 1.0
SEED = 12345

REPO_ROOT = Path(__file__).resolve().parent.parent
CPP_BIN = REPO_ROOT / "cpp" / "build" / "twocascade_run"
# Chosen so the grid spans a 20x range in n (a 400x range in pair count), which
# is enough to separate quadratic from near-linear growth by inspection, while
# keeping the slowest single point (the Python oracle at n=40000) inside a
# couple of minutes on one core.
DEFAULT_N_GRID = (2000, 10000, 40000)
# The cross-language mode uses the PRODUCTION w_min (configs/poster_girg_*.json,
# calibrated for mean degree ~4.53 at n=10000), not this module's legacy
# W_MIN = 1.0. That legacy value produces mean degree ~80, a regime in which the
# BKL acceptance bound saturates constantly and the benchmark would flatter or
# penalise the samplers for reasons no production sweep will ever hit. The
# python-only mode keeps W_MIN unchanged so its already-reported table stays
# comparable.
XLANG_W_MIN = 0.186377


def make_inputs(n, seed):
    rng = np.random.default_rng(seed)
    pts = sample_torus_points(n, rng)
    w = sample_powerlaw_weights(n, TAU, W_MIN, rng)
    return pts, w


def time_one(sampler, n, seed):
    pts, w = make_inputs(n, seed)
    rng = np.random.default_rng(seed + 1)
    t0 = time.perf_counter()
    sampler(pts, w, ALPHA_G, rng)
    t1 = time.perf_counter()
    return t1 - t0


def time_python_oracle(n, seed, w_min):
    """Time the production Python sampler and report (seconds, edge count).

    Point/weight generation is outside the timed region, matching what the C++
    bench mode times, so the comparison is sampler-to-sampler.
    """
    rng = np.random.default_rng(seed)
    pts = sample_torus_points(n, rng)
    w = sample_powerlaw_weights(n, TAU, w_min, rng)
    rng = np.random.default_rng(seed + 1)
    t0 = time.perf_counter()
    adj = sample_girg_adjacency(pts, w, ALPHA_G, rng)
    t1 = time.perf_counter()
    return t1 - t0, sum(len(a) for a in adj) // 2


def time_cpp(variant, n, seed, w_min):
    """Time one C++ sampler via the binary's bench mode: (seconds, edge count)."""
    out = subprocess.run(
        [
            str(CPP_BIN), "--girg-verify", "bench",
            "--n", str(n), "--tau", str(TAU), "--w-min", str(w_min),
            "--alpha-g", str(ALPHA_G), "--girg-variant", variant,
            "--base-seed", str(seed),
        ],
        capture_output=True, text=True, check=True,
        env={"OMP_NUM_THREADS": "1", "PATH": "/usr/bin:/bin"},
    ).stdout.split()
    assert out[0] == variant and int(out[1]) == n, f"unexpected bench output: {out}"
    return float(out[2]), int(out[3])


LABELS = ("python-oracle", "cpp-direct", "cpp-bkl")


def cross_language_main(n_grid, w_min=XLANG_W_MIN):
    if not CPP_BIN.exists():
        sys.exit(f"C++ binary not found at {CPP_BIN}; build cpp/ in Release mode first.")

    by_key = {}
    for n in n_grid:
        for label in LABELS:
            print(f"  timing {label} at n={n} ...", flush=True)
            if label == "python-oracle":
                seconds, edges = time_python_oracle(n, SEED, w_min)
            else:
                seconds, edges = time_cpp(label.split("-", 1)[1], n, SEED, w_min)
            by_key[(label, n)] = (seconds, edges)
            print(f"    {seconds:.4f} s, {edges} edges", flush=True)

    print()
    print(f"tau={TAU} w_min={w_min} alpha_g={ALPHA_G} base_seed={SEED}, "
          f"1 graph per cell, single-threaded")
    print()
    print("| sampler | n | sec/graph | edges | vs cpp-bkl |")
    print("|---|---|---|---|---|")
    for n in n_grid:
        bkl_s = by_key[("cpp-bkl", n)][0]
        for label in LABELS:
            s, e = by_key[(label, n)]
            ratio = "1.0x (ref)" if label == "cpp-bkl" else f"{s / bkl_s:.1f}x"
            print(f"| {label} | {n} | {s:.4f} | {e} | {ratio} |")

    if len(n_grid) < 2:
        return
    steps = list(zip(n_grid, n_grid[1:]))
    print()
    header = " | ".join(f"{lo}->{hi} ({hi/lo:g}x n)" for lo, hi in steps)
    print(f"| sampler | {header} |")
    print("|---" * (len(steps) + 1) + "|")
    for label in LABELS:
        parts = []
        for lo, hi in steps:
            quad = (hi / lo) ** 2
            got = by_key[(label, hi)][0] / by_key[(label, lo)][0]
            parts.append(f"{got:.1f}x (quadratic: {quad:.0f}x)")
        print(f"| {label} | " + " | ".join(parts) + " |")


def main():
    results = {}

    print("Timing slow sampler...")
    for n in (1000, 2000):
        results[("slow", n)] = time_one(sample_girg_adjacency_slow, n, SEED)
        print(f"  slow n={n}: {results[('slow', n)]:.4f} s")

    print("Timing fast sampler...")
    for n in (1000, 2000, 10000):
        results[("fast", n)] = time_one(sample_girg_adjacency, n, SEED)
        print(f"  fast n={n}: {results[('fast', n)]:.4f} s")

    # Quadratic extrapolation of the slow sampler to n=10000 from the n=2000
    # measurement (O(n^2) pairwise loop): t(10000) ~= t(2000) * (10000/2000)^2
    slow_2000 = results[("slow", 2000)]
    slow_10000_extrap = slow_2000 * (10000 / 2000) ** 2

    print()
    print("=" * 60)
    print(f"{'sampler':8s} {'n':>7s} {'sec/graph':>12s}  {'note'}")
    print("-" * 60)
    for n in (1000, 2000):
        print(f"{'slow':8s} {n:7d} {results[('slow', n)]:12.4f}  measured")
    print(f"{'slow':8s} {10000:7d} {slow_10000_extrap:12.4f}  extrapolated (quadratic from n=2000)")
    for n in (1000, 2000, 10000):
        print(f"{'fast':8s} {n:7d} {results[('fast', n)]:12.4f}  measured")
    print("=" * 60)

    speedup_2000 = slow_2000 / results[("fast", 2000)]
    print(f"\nSpeedup at n=2000: {speedup_2000:.1f}x (slow {slow_2000:.4f}s / fast {results[('fast', 2000)]:.4f}s)")

    speedup_10000_extrap = slow_10000_extrap / results[("fast", 10000)]
    print(f"Projected speedup at n=10000: {speedup_10000_extrap:.1f}x "
          f"(slow extrap {slow_10000_extrap:.4f}s / fast measured {results[('fast', 10000)]:.4f}s)")

    # Projected total sampling time for the target sweep.
    n_grid_points = 11
    n_trials = 500
    n_fear_arms = 3
    total_graphs = n_grid_points * n_trials * n_fear_arms
    fast_10000 = results[("fast", 10000)]
    total_seconds_fast = total_graphs * fast_10000
    total_hours_fast = total_seconds_fast / 3600.0

    total_seconds_slow_extrap = total_graphs * slow_10000_extrap
    total_hours_slow_extrap = total_seconds_slow_extrap / 3600.0

    print()
    print(f"Projected sampling-only cost for {n_grid_points} grid points x {n_trials} trials "
          f"x {n_fear_arms} fear arms = {total_graphs} graphs at n=10000:")
    print(f"  fast sampler:          {total_hours_fast:.3f} hours ({total_seconds_fast:.1f} s)")
    print(f"  slow sampler (extrap): {total_hours_slow_extrap:.1f} hours ({total_seconds_slow_extrap:.1f} s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cross-language", action="store_true",
                    help="Python oracle vs C++ direct vs C++ BKL over an n-grid")
    ap.add_argument("--n-grid", type=int, nargs="+", default=list(DEFAULT_N_GRID),
                    help="n values for --cross-language (default: 2000 10000 40000)")
    cli = ap.parse_args()
    if cli.cross_language:
        cross_language_main(cli.n_grid)
    else:
        main()
