import os
import sys
import json
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.analysis import analyze_sweep, load_raw_results, evaluate_scaling_adherence
from twocascade.plotting import plot_bimodality_histograms, apply_plot_style, plot_critical_scaling_validation, plot_mu_sweep

def generate_plots_for_r(r_val):
    raw_path = os.path.join(base_dir, "results", "raw", f"sweep_wk3_4_r{r_val}.json")
    figures_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    if not os.path.exists(raw_path):
        print(f"File {raw_path} not found.")
        return
        
    print(f"Loading raw results from: {raw_path}")
    raw_data = load_raw_results(raw_path)
    
    print(f"Running sweep analysis for r={r_val}...")
    analyzed = analyze_sweep(raw_data)
    
    # 1. Tabular Presentation and Metrics Printing
    adherence = evaluate_scaling_adherence(analyzed)
    meta = analyzed["metadata"]
    n = meta["n"]
    p = meta["p"]
    theta = meta["theta"]
    a_emp_0 = adherence["a_emp_0"]
    
    print(f"=========================================================================================")
    print(f"Scaling Analysis for r={r_val} (N={n}, p={p:.6f}, theta={theta})")
    print(f"Baseline a_emp(0) = {a_emp_0:.4f}" if a_emp_0 is not None else "Baseline a_emp(0) = N/A")
    print(f"=========================================================================================")
    print(f"{'μ':<6} | {'a_emp':<10} | {'Ratio_emp':<10} | {'Ratio_theory':<12} | {'Diff':<10} | {'Predicted_ac':<12} | {'Status':<10}")
    print("-" * 90)
    
    for row in adherence["results_table"]:
        mu = row["mu"]
        a_emp = row["a_emp"]
        ratio_theory = row["ratio_theory"]
        pred_ac = row["predicted_ac"]
        status = "Clamped" if row["is_clamped"] else "Valid"
        
        if row["is_clamped"]:
            ratio_emp_str = ""
            diff_str = ""
        else:
            ratio_emp_str = f"{row['ratio_emp']:.4f}"
            diff_str = f"{row['diff']:.4f}"
            
        print(f"{mu:<6.2f} | {a_emp:<10.4f} | {ratio_emp_str:<10} | {ratio_theory:<12.4f} | {diff_str:<10} | {pred_ac:<12.4f} | {status:<10}")
        
    print("-" * 90)
    print("Summary evaluation for non-clamped rows:")
    max_d = adherence['max_diff']
    mean_d = adherence['mean_diff']
    max_d_str = f"{max_d:.6f}" if max_d is not None else "N/A"
    mean_d_str = f"{mean_d:.6f}" if mean_d is not None else "N/A"
    print(f"  max(|diff|)  = {max_d_str}")
    print(f"  mean(|diff|) = {mean_d_str}")
    print("\n")

    # 2. Call Centralized 1-D mu-Sweep Plot
    try:
        plot_mu_sweep(analyzed, figures_dir, filename=f"wk3_4_mu_sweep_r{r_val}.png")
        print(f"Saved wk3_4_mu_sweep_r{r_val}.png")
    except Exception as e:
        print(f"Failed to generate mu sweep plot: {e}")
    
    # 3. Bimodality Histograms for mu=0.3
    try:
        plot_bimodality_histograms(analyzed, 0.3, figures_dir)
        default_hist = os.path.join(figures_dir, "bimodality_histograms.png")
        new_hist = os.path.join(figures_dir, f"wk3_4_bimodality_histograms_r{r_val}.png")
        if os.path.exists(default_hist):
            if os.path.exists(new_hist):
                os.remove(new_hist)
            os.rename(default_hist, new_hist)
            print(f"Saved {new_hist}")
       
    except Exception as e:
        print(f"Failed to plot histograms: {e}")
        
    # 4. Relocate JSON Analysis Outputs and Stamp Metadata
    analysis_dir = os.path.join(base_dir, "results", "analysis")
    os.makedirs(analysis_dir, exist_ok=True)
    
    # Resolve the active analysishead git commit
    try:
        current_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=base_dir).decode("utf-8").strip()
    except Exception:
        current_head = "unknown"
    
    # Add validation metadata tracking schema
    adherence["metadata_tracking"] = {
        "origin_file": os.path.basename(raw_path),
        "data_generation_commit": meta.get("git_commit", "unknown"),
        "analysis_runtime_commit": current_head,
        "base_seed": meta.get("base_seed", "unknown"),
        "timestamp": meta.get("timestamp", "unknown")
    }
    
    adherence_path = os.path.join(analysis_dir, f"sweep_wk3_4_r{r_val}_adherence.json")
    with open(adherence_path, "w") as f:
        json.dump(adherence, f, indent=2)
    print(f"Saved adherence analysis data to: {adherence_path}")

    # 5. Call Centralized Scaling Validation Plot (passing precomputed adherence)
    try:
        plot_critical_scaling_validation(analyzed, figures_dir, filename=f"wk3_4_scaling_validation_r{r_val}.png", adherence=adherence)
        print(f"Saved wk3_4_scaling_validation_r{r_val}.png")
    except Exception as e:
        print(f"Failed to generate scaling validation plot: {e}")

if __name__ == "__main__":
    for r in [2, 3, 4]:
        generate_plots_for_r(r)
