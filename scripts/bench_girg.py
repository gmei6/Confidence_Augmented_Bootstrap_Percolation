"""Benchmark: slow vs fast GIRG adjacency sampler.

Times single-graph sampling (fixed seed) for:
  - slow sampler at n=1000 and n=2000 (measured)
  - fast sampler at n=1000, n=2000, n=10000 (measured)
  - slow sampler at n=10000 (extrapolated quadratically from n=2000, not run —
    O(n^2) scalar loop at n=10000 would take on the order of hours)

Then projects sampling-only wall time for an 11-grid-point x 500-trial x
3-fear-arm sweep at n=10000 using the fast sampler.

Run with: arch -arm64 python3 scripts/bench_girg.py
"""
import time
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
    main()
