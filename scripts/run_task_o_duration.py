"""
Task O follow-up (Q5, C-Q5(ii)): duration dichotomy n-sweep.

T_theta(n) for the global fear field vs the ell = r_n local field on hard RGGs
(D_bar = 2 log n), disc-seeded, at n in {4000, 8000, 16000, 32000}.

C-Q5(ii) predicts: global-field T_theta(n) grows strictly slower than the
ballistic bound (T_theta / sqrt(n / log n) -> 0: secondary nucleation
short-circuits the front), while the local field at fixed ell/r_n stays
ballistic, Theta(sqrt(n / log n)). The mu = 0 cell is the shared control
(field type is provably irrelevant at mu = 0), run once per n.

Durations only - no per-round locality statistics and no position logging -
so the raw JSON stays small at n = 32000 (the D-014 JSON-bloat rule).

Owns its raw output (results integrity rule): stamps config, seeds, and git
commit into results/q5_duration_raw.json.
"""

import os
import sys
import json
import datetime
from multiprocessing import Pool

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash
from twocascade.reference import make_nodes, sample_individual_fears
from twocascade.geometry import (
    sample_torus_points,
    build_rgg_adjacency,
    build_fear_adjacency,
    run_cascade_local_fear,
)

CONFIG = {
    "n_grid": [4000, 8000, 16000, 32000],
    "r": 2,
    "concentration": 50,
    "theta": 0.5,
    "window_len": 5,
    "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
    "mean_degree_c": 2.0,
    "seed_layout": "disc",
    "seed_size": 30,
    "cells": [
        {"field": "control", "ell_over_rn": None, "mean_fear": 0.0},
        {"field": "global", "ell_over_rn": None, "mean_fear": 0.2},
        {"field": "global", "ell_over_rn": None, "mean_fear": 0.4},
        {"field": "local_1", "ell_over_rn": 1.0, "mean_fear": 0.2},
        {"field": "local_1", "ell_over_rn": 1.0, "mean_fear": 0.4},
    ],
    "trials_per_cell": 30,
    "base_seed": 2027,
}

OUTPUT_PATH = "results/q5_duration_raw.json"


def run_trial(args):
    (n, cell, child_seed, cfg) = args
    s_graph, s_fear, s_casc = child_seed.spawn(3)
    rng_graph = np.random.default_rng(s_graph)
    rng_fear = np.random.default_rng(s_fear)
    rng_casc = np.random.default_rng(s_casc)

    r_n = float(np.sqrt(cfg["mean_degree_c"] * np.log(n) / (np.pi * n)))
    points = sample_torus_points(n, rng_graph)
    adj = build_rgg_adjacency(points, r_n)
    fear_adj = (None if cell["ell_over_rn"] is None
                else build_fear_adjacency(points, cell["ell_over_rn"] * r_n))

    fears = sample_individual_fears(n, mean_fear=cell["mean_fear"],
                                    concentration=cfg["concentration"], rng=rng_fear)

    center = sample_torus_points(1, rng_casc)[0]
    diff = np.abs(points - center)
    diff = np.minimum(diff, 1.0 - diff)
    seeds = np.argsort(np.sum(diff ** 2, axis=1))[:cfg["seed_size"]].tolist()

    nodes = make_nodes(list(fears))
    res = run_cascade_local_fear(
        adjacency=adj, fear_adjacency=fear_adj, nodes=nodes, r=cfg["r"],
        seed_indices=seeds, rng=rng_casc, record_history=True,
        window_len=cfg["window_len"], weights=cfg["weights"])

    # T_theta from the cumulative history (history[0] is the seed count).
    theta_count = cfg["theta"] * n
    t_theta = next((t for t, c in enumerate(res.history) if c >= theta_count), None)

    return {
        "n": n,
        "field": cell["field"],
        "mean_fear": cell["mean_fear"],
        "final_failed_fraction": res.final_failed_fraction,
        "rounds_completed": res.rounds_completed,
        "t_theta": t_theta,
        "systemic": res.final_failed_fraction >= cfg["theta"],
    }


def main():
    cfg = CONFIG
    grid = [(n, cell) for n in cfg["n_grid"] for cell in cfg["cells"]]
    ss = np.random.SeedSequence(cfg["base_seed"])
    child_seeds = ss.spawn(len(grid) * cfg["trials_per_cell"])

    tasks = []
    idx = 0
    for n, cell in grid:
        for _ in range(cfg["trials_per_cell"]):
            tasks.append((n, cell, child_seeds[idx], cfg))
            idx += 1

    print(f"Q5 duration sweep: {len(grid)} cells x {cfg['trials_per_cell']} trials "
          f"= {len(tasks)} trials")
    n_workers = os.cpu_count() or 4
    chunksize = max(1, len(tasks) // (n_workers * 4))
    with Pool() as pool:
        results = pool.map(run_trial, tasks, chunksize=chunksize)

    out = {
        "metadata": {
            "task": "O follow-up (Q5 C-Q5(ii) duration dichotomy n-sweep)",
            **{k: v for k, v in cfg.items()},
            "git_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "engine": "python (run_cascade_local_fear)",
        },
        "results": results,
    }
    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
