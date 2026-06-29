import os
import sys
import json
import datetime
import math
import subprocess
from pathlib import Path
import numpy as np
import scipy.stats as stats

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep
from twocascade.analysis import analyze_sweep, load_raw_results

def create_configs():
    configs_dir = os.path.join(base_dir, "configs")
    os.makedirs(configs_dir, exist_ok=True)
    
    mean_fear_grid = [
        0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
        0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9
    ]
    seed_multiples = [
        0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0,
        1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4
    ]
    
    configs = {}
    for n in [1000, 2000]:
        for targeted in [False, True]:
            arm_str = "targeted" if targeted else "random"
            config_name = f"seed_{arm_str}_r2_n{n}.json"
            cfg = {
                "engine": "python",
                "pinned_params": {
                    "n": n,
                    "r": 2,
                    "concentration": 50.0,
                    "theta": 0.5,
                    "window_len": 1,
                    "weights": None,
                    "target_high_degree": targeted
                },
                "scaling": {
                    "n_ref": 1000,
                    "target_mean_degree": 8.0,
                    "alpha": 0.7
                },
                "sweep": {
                    "mean_fear_grid": mean_fear_grid,
                    "seed_multiples": seed_multiples,
                    "trials_per_cell": 300,
                    "base_seed": 20260629
                },
                "output": {
                    "raw_filepath": f"results/raw/seed_{arm_str}_r2_n{n}.json"
                }
            }
            path = os.path.join(configs_dir, config_name)
            with open(path, "w") as f:
                json.dump(cfg, f, indent=2)
            configs[f"n{n}_{arm_str}"] = path
    return configs

def run_simulations(configs):
    for key, path in configs.items():
        with open(path, "r") as f:
            cfg = json.load(f)
        raw_output_path = os.path.join(base_dir, cfg["output"]["raw_filepath"])
        if not os.path.exists(raw_output_path):
            print(f"Running sweep simulation for {key}...")
            run_sweep(path)

def analyze_and_write():
    results = {}
    for n in [1000, 2000]:
        rand_path = os.path.join(base_dir, f"results/raw/seed_random_r2_n{n}.json")
        targ_path = os.path.join(base_dir, f"results/raw/seed_targeted_r2_n{n}.json")
        
        rand_raw = load_raw_results(rand_path)
        targ_raw = load_raw_results(targ_path)
        
        rand_anal = analyze_sweep(rand_raw)
        targ_anal = analyze_sweep(targ_raw)
        
        results[n] = {
            "random": rand_anal,
            "targeted": targ_anal,
            "raw_random": rand_raw,
            "raw_targeted": targ_raw
        }
    
    commit_hash = "dirty-or-unknown"
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=base_dir
        )
        if res.returncode == 0:
            commit_hash = res.stdout.strip()
    except Exception:
        pass
        
    out_payload = {
        "metadata": {
            "n_values": [1000, 2000],
            "r": 2,
            "base_seed": 20260629
        },
        "comparison_summary": {},
        "empirical_thresholds": {}
    }
    
    for n, data in results.items():
        rand_cells = data["random"]["processed_cells"]
        targ_cells = data["targeted"]["processed_cells"]
        
        rand_map = {(c["mean_fear"], c["seed_size"]): c for c in rand_cells}
        targ_map = {(c["mean_fear"], c["seed_size"]): c for c in targ_cells}
        
        z_tests = []
        sig_count = 0
        total_cells = 0
        
        for key in rand_map:
            if key in targ_map:
                rc = rand_map[key]
                tc = targ_map[key]
                
                n1 = len(rc["failed_fractions"])
                n2 = len(tc["failed_fractions"])
                s1 = sum(1 for ff in rc["failed_fractions"] if ff >= 0.5)
                s2 = sum(1 for ff in tc["failed_fractions"] if ff >= 0.5)
                
                p1 = s1 / n1
                p2 = s2 / n2
                p_pool = (s1 + s2) / (n1 + n2)
                
                if 0 < p_pool < 1:
                    se = math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
                    z = (p1 - p2) / se
                    p_val = stats.norm.sf(abs(z)) * 2
                else:
                    z = 0.0
                    p_val = 1.0
                
                diff = p2 - p1
                z_tests.append({
                    "mu": key[0],
                    "seed_size": key[1],
                    "p_random": p1,
                    "p_targeted": p2,
                    "diff": diff,
                    "z_stat": z,
                    "p_value": p_val
                })
                
                if p_val < 0.05:
                    sig_count += 1
                total_cells += 1
        
        sig_percentage = (sig_count / total_cells) * 100 if total_cells > 0 else 0.0
        
        rand_thresh = data["random"]["empirical_thresholds"]
        targ_thresh = data["targeted"]["empirical_thresholds"]
        
        thresh_diffs = []
        for mu_str, rand_a in rand_thresh.items():
            targ_a = targ_thresh.get(mu_str)
            if rand_a is not None and targ_a is not None and not math.isnan(rand_a) and not math.isnan(targ_a):
                diff = targ_a - rand_a
                thresh_diffs.append(diff)
                
        out_payload["comparison_summary"][str(n)] = {
            "total_cells": total_cells,
            "sig_percentage": sig_percentage,
            "sig_count": sig_count,
            "mean_thresh_diff": float(np.mean(thresh_diffs)) if thresh_diffs else None,
            "max_abs_thresh_diff": float(np.max(np.abs(thresh_diffs))) if thresh_diffs else None
        }
        
        # Clean serialization of empirical thresholds (convert NaN to null)
        clean_rand = {}
        for k, v in rand_thresh.items():
            clean_rand[k] = None if (v is None or math.isnan(v)) else float(v)
            
        clean_targ = {}
        for k, v in targ_thresh.items():
            clean_targ[k] = None if (v is None or math.isnan(v)) else float(v)
            
        out_payload["empirical_thresholds"][str(n)] = {
            "random": clean_rand,
            "targeted": clean_targ
        }
        
    out_payload["metadata_tracking"] = {
        "origin_file": "seed_random_r2_n1000.json, seed_targeted_r2_n1000.json, seed_random_r2_n2000.json, seed_targeted_r2_n2000.json",
        "data_generation_commit": commit_hash,
        "analysis_runtime_commit": commit_hash,
        "base_seed": 20260629,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    analysis_dir = os.path.join(base_dir, "results", "analysis")
    os.makedirs(analysis_dir, exist_ok=True)
    artifact_path = os.path.join(analysis_dir, "targeted_seeding_adherence.json")
    with open(artifact_path, "w") as f:
        json.dump(out_payload, f, indent=2)
    print(f"Saved secondary analysis output to {artifact_path}")

if __name__ == "__main__":
    configs = create_configs()
    run_simulations(configs)
    analyze_and_write()
