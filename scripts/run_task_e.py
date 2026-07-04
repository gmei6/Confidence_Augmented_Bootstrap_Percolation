import os
import sys
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash
from twocascade.model import calculate_beta, calculate_p_n, janson_a_c
from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade
)
from twocascade.analysis import load_raw_results, analyze_fear_field_concentration
from twocascade.plotting import plot_fear_field_concentration

def run_single_trial_with_history(args):
    """Worker task to run a single simulation realization with history tracking."""
    (n, p, r, mu, kappa, a, target_high_degree, window_len, weights, child_seed) = args
    
    rng = np.random.default_rng(child_seed)
    
    adj = sample_gnp_adjacency(n, p, rng)
    fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng)
    
    nodes = make_nodes(fears)
    seeds = choose_seed(n, a, adj, rng, target_high_degree)
    
    res = run_cascade(
        adjacency=adj, nodes=nodes, r=r, seed_indices=seeds,
        rng=rng, record_history=True,
        window_len=window_len, weights=weights
    )
    
    return res.final_failed_fraction, res.rounds_completed, res.history

def run_sweep_with_history(config_path: str):
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
    beta = calculate_beta(scaling["target_mean_degree"], scaling["n_ref"], alpha)
    p = calculate_p_n(beta, n, alpha)

    ac0 = janson_a_c(n, p, r)
    
    mean_fear_grid = sweep["mean_fear_grid"]
    seed_multiples = sweep["seed_multiples"]
    trials_per_cell = sweep["trials_per_cell"]
    base_seed = sweep["base_seed"]
    
    ss = np.random.SeedSequence(base_seed)
    
    out_data = {
      "metadata": {
        "n": n, "p": p, "r": r, "concentration": kappa, "theta": theta,
        "window_len": window_len, "weights": weights, "trials_per_cell": trials_per_cell,
        "base_seed": base_seed, "git_commit": get_git_commit_hash(),
        "timestamp": datetime.datetime.now().isoformat(),
        "engine": "python_with_history"
      },
      "sweep_parameters": {
        "mean_fear_grid": mean_fear_grid,
        "seed_multiples": sweep["seed_multiples"],
        "seed_size_grid": [max(r, round(m * ac0)) for m in seed_multiples]
      },
      "results": []
    }
    
    tasks = []
    cell_info = []
    
    for i, mu in enumerate(mean_fear_grid):
        for j, mult in enumerate(seed_multiples):
            a = max(r, round(mult * ac0))
            cell_info.append((i, j, mu, mult, a))
            
    num_cells = len(cell_info)
    child_seeds = ss.spawn(num_cells * trials_per_cell)
    seed_idx = 0
    for i, j, mu, mult, a in cell_info:
        for trial in range(trials_per_cell):
            child_seed = child_seeds[seed_idx]
            seed_idx += 1
            tasks.append((
                n, p, r, mu, kappa, a, target_high_degree,
                window_len, weights, child_seed
            ))
            
    print(f"Starting sweep simulation (Python with history) with {len(tasks)} tasks...")
    n_workers = os.cpu_count() or 4
    chunksize = max(1, len(tasks) // (n_workers * 4))
    
    with Pool(processes=n_workers) as pool:
        results_flat = pool.map(run_single_trial_with_history, tasks, chunksize=chunksize)
        
    result_idx = 0
    for i, j, mu, mult, a in cell_info:
        failed_fractions = []
        rounds_completed = []
        histories = []
        
        for _ in range(trials_per_cell):
            ff, rc, hist = results_flat[result_idx]
            failed_fractions.append(ff)
            rounds_completed.append(rc)
            histories.append(hist)
            result_idx += 1
            
        out_data["results"].append({
            "mean_fear": mu,
            "mean_fear_idx": i,
            "seed_multiple": mult,
            "seed_multiple_idx": j,
            "seed_size": a,
            "failed_fractions": failed_fractions,
            "rounds_completed": rounds_completed,
            "histories": histories
        })
        
    raw_filepath = cfg["output"]["raw_filepath"]
    raw_filepath_full = os.path.join(base_dir, raw_filepath)
    os.makedirs(os.path.dirname(raw_filepath_full), exist_ok=True)
    
    with open(raw_filepath_full, "w") as f:
        json.dump(out_data, f, indent=2)
        
    print(f"Sweep simulation complete. Raw results saved to {raw_filepath_full}")


def main():
    configs = [
        "fear_concentration_n1000.json",
        "fear_concentration_n2000.json",
        "fear_concentration_n4000.json",
        "fear_concentration_n8000.json",
    ]

    for config_name in configs:
        config_path = os.path.join(base_dir, "configs", config_name)
        if not os.path.exists(config_path):
            print(f"Error: Config file not found at {config_path}")
            continue
            
        print(f"Running sweep for {config_name} with history...")
        run_sweep_with_history(config_path)
        
    print("\n=== Step 2: Analyzing Results ===")
    n_values = [1000, 2000, 4000, 8000]
    raw_by_n = {}
    
    for n in n_values:
        raw_path = os.path.join(base_dir, "results", "raw", f"fear_concentration_n{n}.json")
        if not os.path.exists(raw_path):
            print(f"Error: Raw file {raw_path} not found.")
            return
        raw_by_n[n] = load_raw_results(raw_path)

    concentration = analyze_fear_field_concentration(raw_by_n)
    
    figures_dir = os.path.join(base_dir, "results", "figures")
    plot_fear_field_concentration(concentration, figures_dir)
    print("Done!")

if __name__ == "__main__":
    main()
