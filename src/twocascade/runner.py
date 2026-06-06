"""
Simulation runner to orchestrate grid sweeps and record raw results.
"""

import json
import datetime
import os
import subprocess
from typing import Dict, Any, List, Optional
import numpy as np
from multiprocessing import Pool

from twocascade.model import calculate_beta, calculate_p_n, janson_a_c
from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade
)

def get_git_commit_hash() -> str:
    """Get the current Git commit hash for metadata tracking."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return "dirty-or-unknown"

def serialize_graph_to_json(adjacency: List[List[int]], filepath: str) -> None:
    """Save graph adjacency list as JSON for C++ cross-validation."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(adjacency, f)

def run_single_trial(args) -> tuple[float, int]:
    """Worker task to run a single simulation realization."""
    (n, p, r, mu, kappa, a, target_high_degree, window_len, weights, child_seed) = args
    
    rng = np.random.default_rng(child_seed)
    
    adj = sample_gnp_adjacency(n, p, rng)
    fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng)
    
    nodes = make_nodes(fears)
    seeds = choose_seed(n, a, adj, rng, target_high_degree)
    
    res = run_cascade(
        adjacency=adj, nodes=nodes, r=r, seed_indices=seeds,
        rng=rng, record_history=False,
        window_len=window_len, weights=weights
    )
    
    return res.final_failed_fraction, res.rounds_completed

def run_sweep(config_path: str, num_processes: Optional[int] = None) -> None:
    """Run a grid sweep based on a config file and save raw outcomes to JSON."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    with open(config_path, "r") as f:
        cfg = json.load(f)
        
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
    
    alpha = scaling["alpha"]
    if not (1.0 / r < alpha < 1.0):
        raise ValueError(f"Janson scaling exponent alpha must satisfy 1/r < alpha < 1, got {alpha} (for r={r})")
        
    beta = calculate_beta(scaling["target_mean_degree"], scaling["n_ref"], alpha)
    p = calculate_p_n(beta, n, alpha)
    if 0.0 < p < 1e-15:
        raise ValueError(f"Calculated edge probability p={p} is too small (< 1e-15), which could cause underflow division by zero in graph generation")
        
    ac0 = janson_a_c(n, p, r)
    
    mean_fear_grid = sweep["mean_fear_grid"]
    seed_multiples = sweep["seed_multiples"]
    trials_per_cell = sweep["trials_per_cell"]
    base_seed = sweep["base_seed"]
    
    # Seeding setup
    ss = np.random.SeedSequence(base_seed)
    num_cells = len(mean_fear_grid) * len(seed_multiples)
    child_seeds = ss.spawn(num_cells * trials_per_cell)
    
    out_data = {
      "metadata": {
        "n": n, "p": p, "r": r, "concentration": kappa, "theta": theta,
        "window_len": window_len, "weights": weights, "trials_per_cell": trials_per_cell,
        "base_seed": base_seed, "git_commit": get_git_commit_hash(),
        "timestamp": datetime.datetime.now().isoformat()
      },
      "sweep_parameters": {
        "mean_fear_grid": mean_fear_grid,
        "seed_multiples": seed_multiples,
        "seed_size_grid": [max(r, round(m * ac0)) for m in seed_multiples]
      },
      "results": []
    }
    
    tasks = []
    cell_info = []
    seed_idx = 0
    
    for i, mu in enumerate(mean_fear_grid):
        for j, mult in enumerate(seed_multiples):
            a = max(r, round(mult * ac0))
            cell_info.append((i, j, mu, mult, a))
            
            for trial in range(trials_per_cell):
                child_seed = child_seeds[seed_idx]
                seed_idx += 1
                
                tasks.append((
                    n, p, r, mu, kappa, a, target_high_degree,
                    window_len, weights, child_seed
                ))
                
    print(f"Starting sweep simulation with {len(tasks)} tasks...")
    # Dynamically calculate chunksize to ensure work is balanced across all cores
    n_workers = num_processes if num_processes else os.cpu_count() or 4
    chunksize = max(1, len(tasks) // (n_workers * 4))
    
    with Pool(processes=num_processes) as pool:
        results_flat = pool.map(run_single_trial, tasks, chunksize=chunksize)
        
    result_idx = 0
    for i, j, mu, mult, a in cell_info:
        failed_fractions = []
        rounds_completed = []
        
        for _ in range(trials_per_cell):
            ff, rc = results_flat[result_idx]
            failed_fractions.append(ff)
            rounds_completed.append(rc)
            result_idx += 1
            
        out_data["results"].append({
            "mean_fear": mu,
            "mean_fear_idx": i,
            "seed_multiple": mult,
            "seed_multiple_idx": j,
            "seed_size": a,
            "failed_fractions": failed_fractions,
            "rounds_completed": rounds_completed
        })
        
    raw_filepath = cfg["output"]["raw_filepath"]
    os.makedirs(os.path.dirname(raw_filepath), exist_ok=True)
    
    with open(raw_filepath, "w") as f:
        json.dump(out_data, f, indent=2)
        
    print(f"Sweep simulation complete. Raw results saved to {raw_filepath}")
