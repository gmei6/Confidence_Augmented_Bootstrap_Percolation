#!/usr/bin/env python3
"""Dump a deterministic mu=0 GIRG-shaped reference run (Prong A, cpp-girg-plan G5).

Same idea as .claude/skills/cross-validation/scripts/dump_reference_run.py, but
the graph is a GIRG sample (from the C1 oracle `sample_girg_adjacency`) instead
of G(n,p). At mean_fear=0 the fear channel is off, so the cascade is
deterministic given the graph + seed set + r -- this is what lets the C++
engine's existing (graph-content-agnostic) `--dump-failed-set` path be reused
completely unchanged: it reads a plain edge list, and a GIRG-shaped edge list
loads through it exactly like a G(n,p) one (implementation_plan.md's "Current
state" note on `load_graph_from_file`).

Writes four artifacts:
  <out>/graph.txt   : first line "n m", then m lines "u v" (undirected edges, u<v)
  <out>/seed.txt    : one line of space-separated initial failed-node indices
  <out>/failed.txt  : one line of space-separated final failed-node indices (sorted)
  <out>/meta.txt    : the parameters used + the git commit, for provenance

Usage:
  python scripts/dump_girg_cascade_reference.py --n 2000 --tau 2.5 --w-min 0.245 \
      --alpha-g 1.2 --r 2 --seed-size 20 --base-seed 0 --out results/raw/xval/girg_cascade
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import numpy as np

from twocascade.girg import sample_torus_points, sample_powerlaw_weights, sample_girg_adjacency
from twocascade.reference import sample_individual_fears, make_nodes, choose_seed, run_cascade

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
    ap.add_argument("--n", type=int, required=True, help="number of nodes")
    ap.add_argument("--tau", type=float, default=2.5, help="power-law exponent")
    ap.add_argument("--w-min", type=float, default=0.186377, help="minimum weight")
    ap.add_argument("--alpha-g", type=float, default=1.2, help="GIRG kernel exponent")
    ap.add_argument("--r", type=int, required=True, help="solvency threshold (>=2)")
    ap.add_argument("--seed-size", type=int, required=True, help="initial shock size a")
    ap.add_argument("--base-seed", type=int, default=0, help="RNG base seed (reproducible)")
    ap.add_argument("--out", type=Path, default=Path("results/raw/xval/girg_cascade"), help="output dir")
    args = ap.parse_args()

    rng = np.random.default_rng(args.base_seed)

    points = sample_torus_points(args.n, rng)
    weights = sample_powerlaw_weights(args.n, args.tau, args.w_min, rng)
    adjacency = sample_girg_adjacency(points, weights, args.alpha_g, rng)

    # mean_fear=0 -> all fears 0 -> fear channel off -> deterministic cascade.
    # Uses the same global sample_individual_fears as the mu=0 gnp fixture: at
    # mu=0 the degree-dependent (gamma) fear model and the global model are
    # both the all-zero point mass, so which one is "used" is moot here -- the
    # point of Prong A is the cascade LOGIC on a GIRG-shaped graph, not the
    # (out of scope at mu=0) fear model.
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

    # Provenance: this script previously wrote no meta file at all, so a
    # graph.txt/failed.txt fixture on disk carried no record of the parameters
    # or the sampler/cascade revision that produced it. `failed.txt` is a
    # cross-language ORACLE -- an unstamped one is not auditable.
    (out / "meta.txt").write_text(
        f"n={args.n} tau={args.tau} w_min={args.w_min} alpha_g={args.alpha_g} "
        f"r={args.r} seed_size={args.seed_size} base_seed={args.base_seed} "
        f"mean_fear=0.0 concentration=50.0 edges={len(edges)} final_failed={len(failed)} "
        f"git_commit={git_commit_hash()}\n"
    )

    print(f"n={args.n} tau={args.tau} w_min={args.w_min} alpha_g={args.alpha_g} r={args.r} "
          f"seed_size={args.seed_size} base_seed={args.base_seed}")
    print(f"edges={len(edges)} final_failed={len(failed)} -> {out}/")


if __name__ == "__main__":
    main()
