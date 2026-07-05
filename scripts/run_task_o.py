"""
Task O (Q5) localized-fear sweep: coverage entropy and the nucleation law.

Hard RGG on the unit torus at mean degree D_bar = 2 log n, disc-seeded
(localized droplet - the locality question's seeding, per the Q5 scoping doc),
sweeping mean fear x fear-field type:

  - global field (fear_adjacency=None; == ell >= torus diameter)
  - local field at ell/r_n in {1, 4}
    (ell/r_n = 16 is omitted at n=4000: 16*r_n = 0.58 > half-torus, so it is
    indistinguishable from the global field at this size)

Per trial, per round, records the C-Q5 locality statistics: new-failure count,
cumulative failed fraction g_t, remote failures, remote nucleation count,
coverage entropy H(t), and front radius; plus T_theta (first round with
cumulative fraction >= theta). Round statistics stop once the cumulative
fraction exceeds STATS_CUTOFF (cost control; every C-Q5 clause reads the
pre-theta trajectory) - the cascade itself always runs to completion.

Owns its raw output (results integrity rule): stamps config, seeds, and git
commit into results/q5_localized_fear_raw.json.
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
    remote_failures,
    remote_nucleation,
    coverage_entropy,
    front_radius,
)

CONFIG = {
    "n": 4000,
    "r": 2,
    "concentration": 50,
    "theta": 0.5,
    "window_len": 5,
    "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
    "mean_degree_c": 2.0,          # D_bar = c * log n; hard RGG radius from this
    "seed_layout": "disc",
    "seed_size": 30,
    "mean_fear_grid": [0.0, 0.2, 0.4, 0.6],
    "fields": [
        {"name": "global", "ell_over_rn": None},
        {"name": "local_1", "ell_over_rn": 1.0},
        {"name": "local_4", "ell_over_rn": 4.0},
    ],
    "trials_per_cell": 40,
    "base_seed": 2026,
    "stats_cutoff": 0.75,
}

OUTPUT_PATH = "results/q5_localized_fear_raw.json"


def run_trial(args):
    (mu, field, child_seed, cfg) = args
    n, r = cfg["n"], cfg["r"]
    ss = child_seed
    s_graph, s_fear, s_casc = ss.spawn(3)
    rng_graph = np.random.default_rng(s_graph)
    rng_fear = np.random.default_rng(s_fear)
    rng_casc = np.random.default_rng(s_casc)

    r_n = float(np.sqrt(cfg["mean_degree_c"] * np.log(n) / (np.pi * n)))
    points = sample_torus_points(n, rng_graph)
    adj = build_rgg_adjacency(points, r_n)
    fear_adj = (None if field["ell_over_rn"] is None
                else build_fear_adjacency(points, field["ell_over_rn"] * r_n))

    fears = sample_individual_fears(n, mean_fear=mu, concentration=cfg["concentration"],
                                    rng=rng_fear)

    # Disc seed: the seed_size nodes nearest a random center (torus metric).
    center = sample_torus_points(1, rng_casc)[0]
    diff = np.abs(points - center)
    diff = np.minimum(diff, 1.0 - diff)
    seeds = np.argsort(np.sum(diff ** 2, axis=1))[:cfg["seed_size"]].tolist()

    nodes = make_nodes(list(fears))
    round_log = []
    res = run_cascade_local_fear(
        adjacency=adj, fear_adjacency=fear_adj, nodes=nodes, r=r,
        seed_indices=seeds, rng=rng_casc, record_history=True,
        window_len=cfg["window_len"], weights=cfg["weights"],
        round_log=round_log)

    # Post-processing: per-round locality statistics on the pre-cutoff trajectory.
    theta, cutoff = cfg["theta"], cfg["stats_cutoff"]
    previously_failed = set(seeds)
    cum = len(seeds)
    rounds = []
    t_theta = None
    stats_truncated = False
    for t, new_set in enumerate(round_log, start=1):
        cum += len(new_set)
        g_t = cum / n
        if t_theta is None and g_t >= theta:
            t_theta = t
        if (cum - len(new_set)) / n <= cutoff:
            new_list = sorted(new_set)
            rounds.append({
                "t": t,
                "new": len(new_set),
                "g_t": g_t,
                "remote": remote_failures(new_list, previously_failed, points, r_n),
                "n_nuc": remote_nucleation(new_list, previously_failed, points, r_n, r),
                "H": coverage_entropy(new_list, points),
                "front_radius": front_radius(new_list, points, seeds),
            })
        else:
            stats_truncated = True
        previously_failed |= new_set

    return {
        "mean_fear": mu,
        "field": field["name"],
        "final_failed_fraction": res.final_failed_fraction,
        "rounds_completed": res.rounds_completed,
        "t_theta": t_theta,
        "systemic": res.final_failed_fraction >= theta,
        "stats_truncated": stats_truncated,
        "rounds": rounds,
    }


def main():
    cfg = CONFIG
    cells = [(mu, field) for mu in cfg["mean_fear_grid"] for field in cfg["fields"]]
    ss = np.random.SeedSequence(cfg["base_seed"])
    child_seeds = ss.spawn(len(cells) * cfg["trials_per_cell"])

    tasks = []
    idx = 0
    for mu, field in cells:
        for _ in range(cfg["trials_per_cell"]):
            tasks.append((mu, field, child_seeds[idx], cfg))
            idx += 1

    print(f"Task O sweep: {len(cells)} cells x {cfg['trials_per_cell']} trials "
          f"= {len(tasks)} trials")
    n_workers = os.cpu_count() or 4
    chunksize = max(1, len(tasks) // (n_workers * 4))
    with Pool() as pool:
        results = pool.map(run_trial, tasks, chunksize=chunksize)

    out = {
        "metadata": {
            "task": "O (Q5 localized fear: coverage entropy + nucleation law)",
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
