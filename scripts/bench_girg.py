#!/usr/bin/env python3
import sys
import os
import time
import json
import subprocess
import datetime
from pathlib import Path

# Insert the src directory into sys.path to allow importing twocascade
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

import numpy as np
from twocascade.girg import (
    sample_torus_points, 
    sample_powerlaw_weights, 
    sample_girg_adjacency_reference, 
    sample_girg_adjacency
)

def count_edges(adj):
    """Returns the number of undirected edges."""
    return sum(len(neighbors) for neighbors in adj) / 2.0

def main():
    alpha_g = 1.0
    tau = 2.5
    w_min = 1.0
    
    n_both = [500, 1000, 2000, 4000]
    n_indexed_only = [8000, 16000]
    
    seeds = [42, 43, 44]
    points_results = []
    
    start_time = time.perf_counter()
    
    for n in sorted(n_both + n_indexed_only):
        ref_times = []
        idx_times = []
        ref_edges = []
        idx_edges = []
        
        run_ref = n in n_both
        
        # Guard against n=4000 taking too long for the reference if we are close to timeout.
        # But realistically, 4000 shouldn't be too bad in Python. Let's monitor total time.
        if run_ref and n == 4000 and (time.perf_counter() - start_time) > 200:
            print(f"Skipping reference benchmark for n=4000 due to time constraints.")
            run_ref = False
            
        for seed in seeds:
            rng = np.random.default_rng(seed)
            pts = sample_torus_points(n, rng)
            w = sample_powerlaw_weights(n, tau, w_min, rng)
            
            if run_ref:
                rng_ref = np.random.default_rng(seed + 100)
                t0 = time.perf_counter()
                adj_ref = sample_girg_adjacency_reference(pts, w, alpha_g, rng_ref)
                t1 = time.perf_counter()
                ref_times.append(t1 - t0)
                ref_edges.append(count_edges(adj_ref))
                
            rng_idx = np.random.default_rng(seed + 100)
            t0 = time.perf_counter()
            adj_idx = sample_girg_adjacency(pts, w, alpha_g, rng_idx)
            t1 = time.perf_counter()
            idx_times.append(t1 - t0)
            idx_edges.append(count_edges(adj_idx))
            
        med_idx_s = np.median(idx_times)
        mean_idx_e = np.mean(idx_edges)
        
        pt = {
            "n": n,
            "indexed_s": med_idx_s,
            "indexed_edges": mean_idx_e
        }
        
        if run_ref:
            med_ref_s = np.median(ref_times)
            mean_ref_e = np.mean(ref_edges)
            speedup = med_ref_s / med_idx_s if med_idx_s > 0 else float('inf')
            pt["reference_s"] = med_ref_s
            pt["reference_edges"] = mean_ref_e
            pt["speedup"] = speedup
            
        points_results.append(pt)
        print(f"n={n}, indexed_s={med_idx_s:.4f}, indexed_edges={mean_idx_e:.1f}", flush=True)
        if run_ref:
            print(f"       reference_s={med_ref_s:.4f}, reference_edges={mean_ref_e:.1f}, speedup={speedup:.2f}", flush=True)
        
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=project_root).decode('utf-8').strip()
    except Exception:
        commit = "unknown"
        
    # Generate ISO-8601 UTC string
    now = datetime.datetime.now(datetime.timezone.utc)
    generated = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    out = {
        "commit": commit,
        "generated": generated,
        "alpha_g": alpha_g,
        "tau": tau,
        "w_min": w_min,
        "points": points_results
    }
    
    out_path = project_root / "results" / "processed" / "girg_speedup.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    main()
