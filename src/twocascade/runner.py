"""
Simulation runner to orchestrate grid sweeps and record raw results.
"""

import json
import datetime
import os
import subprocess
import time
from pathlib import Path
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
from twocascade.geometry import (
    sample_torus_points,
    build_rgg_adjacency,
    build_soft_rgg_adjacency,
    build_fear_adjacency,
    run_cascade_local_fear
)
from twocascade.graphs import (
    sample_powerlaw_degrees,
    sample_configuration_model,
    sample_degree_dependent_fears
)
from twocascade.girg import (
    sample_powerlaw_weights,
    sample_girg_adjacency
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CPP_BIN = REPO_ROOT / "cpp" / "build" / "twocascade_run"

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

def run_single_cell_cpp(args) -> List[tuple[float, int]]:
    """Worker task to run a single cell's trials using C++ engine."""
    (n, p, r, mu, kappa, a, trials_per_cell, window_len, weights, cell_seed, cpp_bin_str) = args
    
    # Generate 64-bit seed from SeedSequence
    seed_val = int(cell_seed.generate_state(1, dtype=np.uint64)[0])
    
    cmd = [
        cpp_bin_str,
        "--n", str(n),
        "--p", str(p),
        "--r", str(r),
        "--mu", str(mu),
        "--kappa", str(kappa),
        "--seed-size", str(a),
        "--trials", str(trials_per_cell),
        "--base-seed", str(seed_val),
        "--window-len", str(window_len),
    ]
    if weights is not None and len(weights) > 0:
        cmd.extend(["--weights", ",".join(map(str, weights))])
        
    env = {**os.environ, "OMP_NUM_THREADS": "1"}
    
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            check=True,
            timeout=600  # safety timeout
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"C++ engine timed out after 600s: cmd={' '.join(cmd)}") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"C++ engine failed with exit code {e.returncode}.\n"
            f"Command: {' '.join(cmd)}\n"
            f"Stderr: {e.stderr}"
        ) from e
        
    outcomes = []
    for line in res.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            raise RuntimeError(f"C++ engine returned malformed output line: '{line}'")
        outcomes.append((float(parts[0]), int(parts[1])))
        
    if len(outcomes) != trials_per_cell:
        raise RuntimeError(
            f"C++ engine returned {len(outcomes)} trials, expected {trials_per_cell}.\n"
            f"Command: {' '.join(cmd)}\n"
            f"Stdout: {res.stdout}"
        )
        
    return outcomes

def run_single_trial(args) -> tuple[float, int]:
    """Worker task to run a single simulation realization."""
    (n, p, r, mu, kappa, a, target_high_degree, window_len, weights, graph_cfg, fear_cfg, seed_layout, child_seed) = args
    
    # Strict RNG discipline: separate streams for degrees/geometry, pairing, fears, cascades
    if isinstance(child_seed, np.random.SeedSequence):
        ss = child_seed
    else:
        ss = np.random.SeedSequence(child_seed)
    child_seeds = ss.spawn(4)
    rng_graph = np.random.default_rng(child_seeds[0])
    rng_pair = np.random.default_rng(child_seeds[1])
    rng_fear = np.random.default_rng(child_seeds[2])
    rng_casc = np.random.default_rng(child_seeds[3])
    
    graph_type = graph_cfg.get("type", "gnp")
    points = None
    
    if graph_type == "configuration_model":
        tau = graph_cfg["tau"]
        d_min = graph_cfg["d_min"]
        degrees = sample_powerlaw_degrees(n, tau, d_min, rng_graph)
        adj = sample_configuration_model(degrees, rng_pair)
        
        gamma = fear_cfg.get("gamma", 0.0)
        fears, stats = sample_degree_dependent_fears(degrees, mu, gamma, kappa, rng_fear)
    else:
        if graph_type == "gnp":
            adj = sample_gnp_adjacency(n, p, rng_pair)
        elif graph_type == "girg":
            # GIRG has no hard connection radius: P(i~j) falls off with distance
            # and rises with the weight product, so it does not use r_n at all.
            points = sample_torus_points(n, rng_graph)
            weights_girg = sample_powerlaw_weights(
                n, graph_cfg["tau"], graph_cfg.get("w_min", 1.0), rng_graph)
            adj = sample_girg_adjacency(
                points, weights_girg, graph_cfg.get("alpha_g", 1.2), rng_pair)
        else:
            points = sample_torus_points(n, rng_graph)
            c = graph_cfg.get("mean_degree_c", 2.0)
            r_n = np.sqrt(c * np.log(n) / (np.pi * n))
            if graph_type == "rgg":
                adj = build_rgg_adjacency(points, r_n)
            elif graph_type == "soft_rgg":
                alpha_g = graph_cfg.get("alpha_g", 3.0)
                adj = build_soft_rgg_adjacency(points, r_n, alpha_g, rng_pair)
            else:
                raise ValueError(f"Unknown graph type: {graph_type}")

        if graph_type == "girg":
            gamma = fear_cfg.get("gamma", 0.0)
            fears, fear_stats = sample_degree_dependent_fears(
                weights_girg, mu, gamma, kappa, rng_fear)
        else:
            fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng_fear)

    nodes = make_nodes(fears)
    
    if seed_layout == "disc":
        if points is None:
            raise ValueError("disc seeding requires a geometric graph")
        center = sample_torus_points(1, rng_casc)[0]
        diff = np.abs(points - center)
        diff = np.minimum(diff, 1.0 - diff)
        dists = np.sum(diff**2, axis=1)
        seeds = np.argsort(dists)[:a].tolist()
    else:
        seeds = choose_seed(n, a, adj, rng_casc, target_high_degree)
        
    fear_type = fear_cfg.get("type", "global")
    if fear_type == "global":
        res = run_cascade(
            adjacency=adj, nodes=nodes, r=r, seed_indices=seeds,
            rng=rng_casc, record_history=False,
            window_len=window_len, weights=weights
        )
    elif fear_type == "local":
        if points is None:
            raise ValueError("local fear requires a geometric graph")
        ell_over_rn = fear_cfg.get("ell_over_rn", 1.0)
        if ell_over_rn == float('inf') or ell_over_rn == "inf":
            ell = 2.0
        else:
            ell = r_n * float(ell_over_rn)
        fear_adj = build_fear_adjacency(points, ell)
        res = run_cascade_local_fear(
            adjacency=adj, fear_adjacency=fear_adj, nodes=nodes, r=r, seed_indices=seeds,
            rng=rng_casc, record_history=False,
            window_len=window_len, weights=weights
        )
    else:
        raise ValueError(f"Unknown fear field type: {fear_type}")
    
    return res.final_failed_fraction, res.rounds_completed

def run_sweep(config_path: str, num_processes: Optional[int] = None, engine: Optional[str] = None) -> None:
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
    
    graph_cfg = cfg.get("graph", pinned.get("graph", {"type": "gnp"}))
    fear_cfg = cfg.get("fear_field", pinned.get("fear", {"type": "global"}))
    seed_layout = cfg.get("seed_layout", "uniform")
    
    # Engine resolution precedence: parameter override -> root-level config key -> auto-detect
    engine_requested = engine or cfg.get("engine")
    if engine_requested is not None:
        if engine_requested == "cpp":
            if not CPP_BIN.exists():
                raise FileNotFoundError(f"C++ engine binary not found at {CPP_BIN}. Please build the C++ engine first.")
            resolved_engine = "cpp"
        elif engine_requested == "python":
            resolved_engine = "python"
        else:
            raise ValueError(f"Unknown engine '{engine_requested}'. Must be 'cpp' or 'python'.")
    else:
        if graph_cfg.get("type", "gnp") != "gnp" or fear_cfg.get("type", "global") != "global":
            resolved_engine = "python"
        else:
            resolved_engine = "cpp" if CPP_BIN.exists() else "python"

    print(f"==================================================")
    print(f"USING SIMULATION ENGINE: {resolved_engine.upper()}")
    print(f"==================================================")

    alpha = scaling["alpha"]
    if not (1.0 / r < alpha < 1.0):
        raise ValueError(f"Janson scaling exponent alpha must satisfy 1/r < alpha < 1, got {alpha} (for r={r})")
        
    beta = calculate_beta(scaling["target_mean_degree"], scaling["n_ref"], alpha)
    p = calculate_p_n(beta, n, alpha)
    if 0.0 < p < 1e-15:
        raise ValueError(f"Calculated edge probability p={p} is too small (< 1e-15), which could cause underflow division by zero in graph generation")
        
    if resolved_engine == "cpp" and target_high_degree:
        raise ValueError("C++ engine does not support target_high_degree=True seeding. Please use engine='python' or set target_high_degree=False.")

    ac0 = janson_a_c(n, p, r)
    
    mean_fear_grid = sweep["mean_fear_grid"]
    trials_per_cell = sweep["trials_per_cell"]
    base_seed = sweep["base_seed"]

    # Seed sizes may be given either as multiples of the Janson critical seed
    # (the historical path, floored at r) or as absolute counts. The absolute
    # path exists because the multiple path cannot express a < r at all, and a
    # single-node seed (a=1) is a legitimate experiment.
    seed_multiples_cfg = sweep.get("seed_multiples")
    seed_sizes_cfg = sweep.get("seed_sizes")
    if (seed_multiples_cfg is None) == (seed_sizes_cfg is None):
        raise ValueError(
            "config must set exactly one of sweep.seed_multiples or sweep.seed_sizes")
    if seed_sizes_cfg is not None:
        seed_size_grid = [int(a) for a in seed_sizes_cfg]
        if any(a < 1 for a in seed_size_grid):
            raise ValueError(f"seed_sizes must all be >= 1, got {seed_size_grid}")
        if any(a > n for a in seed_size_grid):
            raise ValueError(f"seed_sizes must all be <= n={n}, got {seed_size_grid}")
        # Keep the recorded multiple meaningful so downstream analysis that reads
        # seed_multiple still sees "fraction of the Janson critical seed".
        seed_multiples = [a / ac0 for a in seed_size_grid]
    else:
        seed_multiples = list(seed_multiples_cfg)
        seed_size_grid = [max(r, round(m * ac0)) for m in seed_multiples]
    
    # Seeding setup
    ss = np.random.SeedSequence(base_seed)
    
    out_data = {
      "metadata": {
        "n": n, "p": p, "r": r, "concentration": kappa, "theta": theta,
        "window_len": window_len, "weights": weights, "trials_per_cell": trials_per_cell,
        "base_seed": base_seed, "git_commit": get_git_commit_hash(),
        "timestamp": datetime.datetime.now().isoformat(),
        "engine": resolved_engine
      },
      "sweep_parameters": {
        "mean_fear_grid": mean_fear_grid,
        "seed_multiples": seed_multiples,
        "seed_size_grid": seed_size_grid,
        "seed_size_source": "seed_sizes" if seed_sizes_cfg is not None else "seed_multiples"
      },
      "results": []
    }
    
    tasks = []
    cell_info = []
    
    for i, mu in enumerate(mean_fear_grid):
        for j, (mult, a) in enumerate(zip(seed_multiples, seed_size_grid)):
            cell_info.append((i, j, mu, mult, a))
            
    num_cells = len(cell_info)

    if resolved_engine == "cpp":
        cell_seeds = ss.spawn(num_cells)
        for idx, (i, j, mu, mult, a) in enumerate(cell_info):
            tasks.append((
                n, p, r, mu, kappa, a, trials_per_cell,
                window_len, weights, cell_seeds[idx], str(CPP_BIN)
            ))
            
        print(f"Starting sweep simulation (C++) with {len(tasks)} cell tasks...")
        n_workers = num_processes if num_processes else os.cpu_count() or 4
        chunksize = max(1, len(tasks) // (n_workers * 4))
        
        with Pool(processes=num_processes) as pool:
            results_flat = pool.map(run_single_cell_cpp, tasks, chunksize=chunksize)
            
        for idx, (i, j, mu, mult, a) in enumerate(cell_info):
            cell_results = results_flat[idx]
            failed_fractions = [ff for ff, rc in cell_results]
            rounds_completed = [rc for ff, rc in cell_results]
            
            out_data["results"].append({
                "mean_fear": mu,
                "mean_fear_idx": i,
                "seed_multiple": mult,
                "seed_multiple_idx": j,
                "seed_size": a,
                "failed_fractions": failed_fractions,
                "rounds_completed": rounds_completed
            })
            
    else:
        child_seeds = ss.spawn(num_cells * trials_per_cell)
        seed_idx = 0
        for i, j, mu, mult, a in cell_info:
            for trial in range(trials_per_cell):
                child_seed = child_seeds[seed_idx]
                seed_idx += 1
                tasks.append((
                    n, p, r, mu, kappa, a, target_high_degree,
                    window_len, weights, graph_cfg, fear_cfg, seed_layout, child_seed
                ))
                
        print(f"Starting sweep simulation (Python) with {len(tasks)} tasks...")
        n_workers = num_processes if num_processes else os.cpu_count() or 4
        chunksize = max(1, len(tasks) // (n_workers * 4))
        
        total_tasks = len(tasks)
        progress_interval = max(1, total_tasks // 20)
        results_flat = []
        start_time = time.monotonic()
        with Pool(processes=num_processes) as pool:
            for done, result in enumerate(
                pool.imap(run_single_trial, tasks, chunksize=chunksize), start=1
            ):
                results_flat.append(result)
                if done % progress_interval == 0 or done == total_tasks:
                    elapsed = time.monotonic() - start_time
                    pct = int(done / total_tasks * 100)
                    remaining = elapsed / done * (total_tasks - done)
                    print(
                        f"progress: {done}/{total_tasks} tasks ({pct}%), "
                        f"elapsed {elapsed:.0f}s, est. remaining {remaining:.0f}s",
                        flush=True,
                    )

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
