import sys
import os
import time
import json
import subprocess
import datetime
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(os.getcwd()) / "src"))

import numpy as np
from twocascade.girg import (
    sample_torus_points, 
    sample_powerlaw_weights, 
    sample_girg_adjacency_reference, 
    sample_girg_adjacency
)

def count_edges(adj):
    return sum(len(neighbors) for neighbors in adj) / 2.0

def main():
    alpha_g = 1.0
    tau = 2.5
    w_min = 1.0
    
    n_both = [500, 1000, 2000, 4000]
    n_indexed_only = [8000, 16000]
    
    points = []
    seeds = [42, 43, 44]
    
    for n in sorted(n_both + n_indexed_only):
        ref_times = []
        idx_times = []
        ref_edges = []
        idx_edges = []
        
        run_ref = n in n_both
        
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
        else:
            pt["reference_s"] = None
            pt["reference_edges"] = None
            pt["speedup"] = None
            
        points.append(pt)
        print(f"n={n}, idx_s={med_idx_s:.4f}, ref_s={pt.get('reference_s')}, speedup={pt.get('speedup')}")
        
    print("Done benchmark")
    
if __name__ == "__main__":
    main()
