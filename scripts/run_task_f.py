"""
Task F runner: counting-process sweeps recording per-trial cumulative failures S(t).

Mirrors twocascade.runner.run_sweep (Python engine path) but additionally records,
for every trial, the cumulative failure counts S(t) for t = 0..t_max via the
Python-only `track_nodes`/`tracked_failure_rounds` diagnostic side-channel (D-026),
cross-checked in-process against the engine's `history` output. The C++ engine does
not populate this side-channel, so engine="python" is mandatory for these configs.

Raw output convention (per cell):
  - "failed_fractions", "rounds_completed": as in runner.run_sweep.
  - "s_histories": list (one entry per trial) of [S(0), S(1), ..., S(min(T, t_max))]
    where S(0) = seed size a and T = rounds_completed. For t beyond the list end
    the cascade has terminated, so S(t) equals the last entry.
"""

import argparse
import datetime
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.model import calculate_beta, calculate_p_n, janson_a_c
from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)
from twocascade.runner import get_git_commit_hash

DEFAULT_CONFIGS = [
    "counting_process_n1000.json",
    "counting_process_n2000.json",
    "counting_process_n4000.json",
    "counting_process_n8000.json",
]


def run_single_trial_counting(args) -> tuple[float, int, list[int]]:
    """Run one realization and return (failed_fraction, rounds, S(t) history)."""
    (n, p, r, mu, kappa, a, target_high_degree, window_len, weights, t_max, child_seed) = args

    rng = np.random.default_rng(child_seed)

    adj = sample_gnp_adjacency(n, p, rng)
    fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng)
    nodes = make_nodes(fears)
    seeds = choose_seed(n, a, adj, rng, target_high_degree)

    res = run_cascade(
        adjacency=adj, nodes=nodes, r=r, seed_indices=seeds,
        rng=rng, record_history=True,
        window_len=window_len, weights=weights,
        track_nodes=set(range(n)),
    )

    # Rebuild S(t) from the D-026 side-channel and cross-check against history.
    failure_rounds = np.fromiter(res.tracked_failure_rounds.values(), dtype=np.int64)
    s_from_tracked = [int(np.sum(failure_rounds <= t)) for t in range(res.rounds_completed + 1)]
    if s_from_tracked != res.history:
        raise RuntimeError(
            f"tracked_failure_rounds disagrees with history: "
            f"tracked={s_from_tracked} history={res.history}"
        )

    return res.final_failed_fraction, res.rounds_completed, res.history[: t_max + 1]


def run_counting_sweep(config_path: str, trials_override: int | None = None,
                       output_suffix: str = "", num_processes: int | None = None) -> None:
    """Run one config's sweep and save raw outcomes (with S(t) histories) to JSON."""
    with open(config_path, "r") as f:
        cfg = json.load(f)

    if cfg.get("engine") != "python":
        raise ValueError(
            f"Config {config_path} must set engine='python': the track_nodes "
            f"diagnostic side-channel is Python-only (D-026)."
        )

    pinned = cfg["pinned_params"]
    scaling = cfg["scaling"]
    sweep = cfg["sweep"]

    n = pinned["n"]
    r = pinned["r"]
    kappa = pinned["concentration"]
    theta = pinned["theta"]
    window_len = pinned["window_len"]
    weights = pinned["weights"]
    target_high_degree = pinned["target_high_degree"]
    t_max = cfg.get("counting_process", {}).get("t_max", 10)

    alpha = scaling["alpha"]
    if not (1.0 / r < alpha < 1.0):
        raise ValueError(f"Janson scaling exponent alpha must satisfy 1/r < alpha < 1, got {alpha} (for r={r})")

    beta = calculate_beta(scaling["target_mean_degree"], scaling["n_ref"], alpha)
    p = calculate_p_n(beta, n, alpha)
    ac0 = janson_a_c(n, p, r)

    mean_fear_grid = sweep["mean_fear_grid"]
    seed_multiples = sweep["seed_multiples"]
    trials_per_cell = trials_override if trials_override is not None else sweep["trials_per_cell"]
    base_seed = sweep["base_seed"]

    ss = np.random.SeedSequence(base_seed)

    out_data = {
        "metadata": {
            "n": n, "p": p, "r": r, "concentration": kappa, "theta": theta,
            "window_len": window_len, "weights": weights, "trials_per_cell": trials_per_cell,
            "base_seed": base_seed, "git_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "engine": "python",
            "t_max": t_max,
            "s_t_convention": (
                "s_histories[k][t] = cumulative failures S(t) after round t "
                "(index 0 = seed size a); for t past the list end, S(t) equals the last entry"
            ),
        },
        "sweep_parameters": {
            "mean_fear_grid": mean_fear_grid,
            "seed_multiples": seed_multiples,
            "seed_size_grid": [max(r, round(m * ac0)) for m in seed_multiples],
        },
        "results": [],
    }

    cell_info = []
    for i, mu in enumerate(mean_fear_grid):
        for j, mult in enumerate(seed_multiples):
            a = max(r, round(mult * ac0))
            cell_info.append((i, j, mu, mult, a))

    child_seeds = ss.spawn(len(cell_info) * trials_per_cell)
    tasks = []
    seed_idx = 0
    for i, j, mu, mult, a in cell_info:
        for _ in range(trials_per_cell):
            tasks.append((
                n, p, r, mu, kappa, a, target_high_degree,
                window_len, weights, t_max, child_seeds[seed_idx],
            ))
            seed_idx += 1

    print(f"[{os.path.basename(config_path)}] n={n}: {len(tasks)} trials across {len(cell_info)} cells...")
    n_workers = num_processes if num_processes else os.cpu_count() or 4
    chunksize = max(1, len(tasks) // (n_workers * 4))

    with Pool(processes=num_processes) as pool:
        results_flat = pool.map(run_single_trial_counting, tasks, chunksize=chunksize)

    result_idx = 0
    for i, j, mu, mult, a in cell_info:
        failed_fractions = []
        rounds_completed = []
        s_histories = []
        for _ in range(trials_per_cell):
            ff, rc, s_hist = results_flat[result_idx]
            failed_fractions.append(ff)
            rounds_completed.append(rc)
            s_histories.append(s_hist)
            result_idx += 1

        out_data["results"].append({
            "mean_fear": mu,
            "mean_fear_idx": i,
            "seed_multiple": mult,
            "seed_multiple_idx": j,
            "seed_size": a,
            "failed_fractions": failed_fractions,
            "rounds_completed": rounds_completed,
            "s_histories": s_histories,
        })

    raw_filepath = cfg["output"]["raw_filepath"]
    if output_suffix:
        root, ext = os.path.splitext(raw_filepath)
        raw_filepath = f"{root}{output_suffix}{ext}"
    raw_filepath = os.path.join(base_dir, raw_filepath)
    os.makedirs(os.path.dirname(raw_filepath), exist_ok=True)

    with open(raw_filepath, "w") as f:
        json.dump(out_data, f)

    print(f"[{os.path.basename(config_path)}] saved raw results to {raw_filepath}")


def main():
    parser = argparse.ArgumentParser(description="Task F counting-process sweeps (Python engine).")
    parser.add_argument("--configs", nargs="*", default=DEFAULT_CONFIGS,
                        help="Config filenames under configs/ (default: all four counting_process configs).")
    parser.add_argument("--trials", type=int, default=None,
                        help="Override trials_per_cell (smoke passes only).")
    parser.add_argument("--suffix", default="",
                        help="Suffix appended to the raw output filename (e.g. _smoke).")
    parser.add_argument("--processes", type=int, default=None)
    args = parser.parse_args()

    for config_name in args.configs:
        config_path = os.path.join(base_dir, "configs", config_name)
        run_counting_sweep(config_path, trials_override=args.trials,
                           output_suffix=args.suffix, num_processes=args.processes)


if __name__ == "__main__":
    main()
