#!/usr/bin/env python3
"""Dump a deterministic mu=0 reference run for Python<->C++ cross-validation (Prong A, SKILL §5.4).

At mean_fear=0 the fear channel is off, so the cascade is deterministic given the
graph + seed set + r. This script generates one G(n,p) graph from the reference
oracle, runs the mu=0 cascade, and writes three artifacts the C++ engine must
reproduce:

  <out>/graph.txt   : first line "n m", then m lines "u v" (undirected edges, u<v)
  <out>/seed.txt    : one line of space-separated initial failed-node indices
  <out>/failed.txt  : one line of space-separated final failed-node indices (sorted)

The C++ engine loads graph.txt + seed.txt, runs at the same r with no fear, and its
final failed set must equal failed.txt exactly. Usage:

  python dump_reference_run.py --n 1000 --p 0.01 --r 2 --seed-size 30 --base-seed 0 \
      --out results/raw/xval
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, required=True, help="number of nodes")
    ap.add_argument("--p", type=float, required=True, help="edge probability")
    ap.add_argument("--r", type=int, required=True, help="solvency threshold (>=2)")
    ap.add_argument("--seed-size", type=int, required=True, help="initial shock size a")
    ap.add_argument("--base-seed", type=int, default=0, help="RNG base seed (reproducible)")
    ap.add_argument("--out", type=Path, default=Path("results/raw/xval"), help="output dir")
    args = ap.parse_args()

    rng = np.random.default_rng(args.base_seed)

    adjacency = sample_gnp_adjacency(n=args.n, p=args.p, rng=rng)
    # mean_fear=0 -> all fears 0 -> fear channel off -> deterministic cascade.
    fears = sample_individual_fears(n=args.n, mean_fear=0.0, concentration=50.0, rng=rng)
    nodes = make_nodes(individual_fears=fears)
    seed_indices = choose_seed(
        n=args.n, seed_size=args.seed_size, adjacency=adjacency, rng=rng,
        target_high_degree=False,
    )
    run_cascade(
        adjacency=adjacency, nodes=nodes, r=args.r, seed_indices=seed_indices,
        rng=rng, record_history=False,
    )
    failed = sorted(node.index for node in nodes if node.failed)

    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    edges = sorted((min(u, v), max(u, v)) for u, nbrs in enumerate(adjacency) for v in nbrs if u < v)
    with (out / "graph.txt").open("w") as fh:
        fh.write(f"{args.n} {len(edges)}\n")
        for u, v in edges:
            fh.write(f"{u} {v}\n")
    (out / "seed.txt").write_text(" ".join(map(str, sorted(seed_indices))) + "\n")
    (out / "failed.txt").write_text(" ".join(map(str, failed)) + "\n")

    print(f"n={args.n} p={args.p} r={args.r} seed_size={args.seed_size} base_seed={args.base_seed}")
    print(f"edges={len(edges)} final_failed={len(failed)} -> {out}/")


if __name__ == "__main__":
    main()
