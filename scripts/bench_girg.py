#!/usr/bin/env python3
"""Measure what the indexed GIRG sampler bought over the O(n^2) reference.

Writes results/processed/girg_speedup.json. Takes no required arguments.

Three sections, and the split between the first two is the whole point:

  points        both implementations, at sizes where timing the O(n^2)
                reference is still affordable. Every entry has a `speedup`.
  indexed_only  the indexed sampler alone, at sizes where the reference would
                dominate the runtime and tell us nothing we do not already know.
                These entries deliberately have NO `speedup` key, because there
                is no reference timing to divide by, and inventing one would be
                the only dishonest thing this script could do.
  points_sparse the same paired comparison in the SPARSE regime (mean degree
                ~10) that the poster's Comparison 2 sweep actually runs in.

Attempt 1 of this task put the indexed-only sizes into `points` and the
acceptance check, which requires a `speedup` on every entry there, died on a
KeyError. Splitting them is not cosmetic: `points` means "a comparison" and
`indexed_only` means "a measurement", and one number per entry is the
difference.

The sparse section exists because a single speedup figure is misleading. The
saving comes from skipping pairs that will not connect, so it grows as the graph
gets sparser: at n=4000 the same code is ~6x faster in the dense default and
~32x faster at the mean degree the sweep uses. Quoting either number alone
overstates or understates the result depending on which way you lean.
"""

import json
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "src"))

import numpy as np  # noqa: E402

from twocascade.girg import (  # noqa: E402
    sample_girg_adjacency,
    sample_girg_adjacency_reference,
    sample_powerlaw_weights,
    sample_torus_points,
)

ALPHA_G = 1.0
TAU = 2.5

# The brief's parameters, and the ones the `points` section reports.
W_MIN_DENSE = 1.0
# Chosen to land the mean degree near the calibrated <k> the sweep uses. Mean
# degree scales roughly with w^2, so this is sqrt(4.5/75) of the dense w_min.
W_MIN_SPARSE = 0.245

PAIRED_SIZES = (500, 1000, 2000, 4000)
INDEXED_ONLY_SIZES = (8000, 16000)
REPEATS = 3


def _edge_count(adj):
    return sum(len(a) for a in adj) // 2


def _instance(n, w_min, seed):
    rng = np.random.default_rng(seed)
    points = sample_torus_points(n, rng)
    weights = sample_powerlaw_weights(n, TAU, w_min, rng)
    return points, weights


def _time_one(fn, points, weights, seed):
    """One timed sample. perf_counter, not time(): this is elapsed work."""
    rng = np.random.default_rng(seed)
    start = time.perf_counter()
    adj = fn(points, weights, ALPHA_G, rng)
    return time.perf_counter() - start, _edge_count(adj)


def _measure(fn, n, w_min, seed_base):
    """Median of REPEATS runs on distinct seeds.

    A single run of a randomised sampler is not a measurement — both the runtime
    and the edge count vary between seeds. The median rather than the mean for
    the timing, because one scheduling hiccup should not move the number.
    """
    times, edges = [], []
    for k in range(REPEATS):
        points, weights = _instance(n, w_min, seed_base + k)
        t, e = _time_one(fn, points, weights, seed_base + 500 + k)
        times.append(t)
        edges.append(e)
    return statistics.median(times), statistics.mean(edges)


def _paired(sizes, w_min, seed_base):
    rows = []
    for n in sizes:
        ref_s, ref_e = _measure(sample_girg_adjacency_reference, n, w_min, seed_base)
        idx_s, idx_e = _measure(sample_girg_adjacency, n, w_min, seed_base)
        rows.append({
            "n": n,
            "reference_s": ref_s,
            "indexed_s": idx_s,
            "speedup": ref_s / idx_s,
            "reference_edges": ref_e,
            "indexed_edges": idx_e,
            "mean_degree": 2.0 * ref_e / n,
        })
        print("n=%-6d ref=%8.3fs  indexed=%8.3fs  speedup=%6.2fx  <k>=%.2f"
              % (n, ref_s, idx_s, ref_s / idx_s, 2.0 * ref_e / n), flush=True)
    return rows


def _git_head():
    try:
        return subprocess.check_output(
            ["git", "-C", _ROOT, "rev-parse", "HEAD"], text=True).strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def main():
    print("paired, dense (w_min=%.3f) — the brief's parameters" % W_MIN_DENSE, flush=True)
    points = _paired(PAIRED_SIZES, W_MIN_DENSE, seed_base=1000)

    print("indexed only — the reference is not run at these sizes", flush=True)
    indexed_only = []
    for n in INDEXED_ONLY_SIZES:
        idx_s, idx_e = _measure(sample_girg_adjacency, n, W_MIN_DENSE, 2000)
        indexed_only.append({
            "n": n,
            "indexed_s": idx_s,
            "indexed_edges": idx_e,
            "mean_degree": 2.0 * idx_e / n,
        })
        print("n=%-6d indexed=%8.3fs  <k>=%.2f" % (n, idx_s, 2.0 * idx_e / n), flush=True)

    print("paired, sparse (w_min=%.3f) — the regime Comparison 2 runs in" % W_MIN_SPARSE,
          flush=True)
    points_sparse = _paired(PAIRED_SIZES, W_MIN_SPARSE, seed_base=3000)

    out = {
        "commit": _git_head(),
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "alpha_g": ALPHA_G,
        "tau": TAU,
        "w_min": W_MIN_DENSE,
        "repeats": REPEATS,
        "statistic": "median of %d runs on distinct seeds; edge counts are means" % REPEATS,
        "points": points,
        "indexed_only": indexed_only,
        "w_min_sparse": W_MIN_SPARSE,
        "points_sparse": points_sparse,
    }

    dest_dir = os.path.join(_ROOT, "results", "processed")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "girg_speedup.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print("wrote %s" % dest)


if __name__ == "__main__":
    main()
