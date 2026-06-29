import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep
from twocascade.analysis import load_raw_results

def run_simulations():
    print("=== Step 1: Running Sweeps for X in {1, 4, 8} ===")
    configs = ["window_r2_X1.json", "window_r2_X4.json", "window_r2_X8.json"]
    for config_name in configs:
        config_path = os.path.join(base_dir, "configs", config_name)
        if not os.path.exists(config_path):
            print(f"Error: Config file not found at {config_path}")
            continue
            
        with open(config_path, "r") as f:
            cfg = json.load(f)
        raw_output_path = os.path.join(base_dir, cfg["output"]["raw_filepath"])
        
        print(f"Running sweep for {config_name} using C++ engine...")
        run_sweep(config_path, engine="cpp")

def analyze_results():
    print("\n=== Step 2: Analyzing Results ===")
    x_values = [1, 4, 8]
    data_by_x = {}
    
    for x in x_values:
        raw_path = os.path.join(base_dir, "results", "raw", f"window_r2_X{x}.json")
        if not os.path.exists(raw_path):
            print(f"Error: Raw file {raw_path} not found.")
            return
        data_by_x[x] = load_raw_results(raw_path)
    
    # 1. Boundary Invariance Check: P(systemic) within +-0.03
    theta = 0.5
    print(f"Performing boundary invariance check (theta={theta})...")
    
    mean_fear_grid = data_by_x[1]["sweep_parameters"]["mean_fear_grid"]
    seed_multiples = data_by_x[1]["sweep_parameters"]["seed_multiples"]
    
    p_systemic_grid = {x: np.zeros((len(mean_fear_grid), len(seed_multiples))) for x in x_values}
    mean_duration_grid = {x: np.zeros((len(mean_fear_grid), len(seed_multiples))) for x in x_values}
    
    for x in x_values:
        results = data_by_x[x]["results"]
        for cell in results:
            mu_idx = cell["mean_fear_idx"]
            mult_idx = cell["seed_multiple_idx"]
            failed_fracs = np.array(cell["failed_fractions"])
            rounds = np.array(cell["rounds_completed"])
            
            # P(systemic)
            p_sys = np.mean(failed_fracs >= theta)
            p_systemic_grid[x][mu_idx, mult_idx] = p_sys
            
            # Duration (mean rounds completed)
            mean_dur = np.mean(rounds)
            mean_duration_grid[x][mu_idx, mult_idx] = mean_dur

    max_delta_p = 0.0
    violating_cells = []
    
    for i, mu in enumerate(mean_fear_grid):
        for j, mult in enumerate(seed_multiples):
            p_vals = [p_systemic_grid[x][i, j] for x in x_values]
            delta = max(p_vals) - min(p_vals)
            if delta > max_delta_p:
                max_delta_p = delta
            if delta > 0.03:
                violating_cells.append((mu, mult, p_vals, delta))
                
    print(f"Max |Delta P(systemic)| across all cells: {max_delta_p:.4f}")
    if max_delta_p <= 0.03:
        print("✅ PASS: P(systemic) boundary invariance within +-0.03 is satisfied!")
    else:
        print(f"❌ FAIL: Boundary invariance violated at {len(violating_cells)} cells:")
        for mu, mult, p_vals, delta in violating_cells:
            print(f"  mu={mu}, mult={mult}: P_sys={p_vals} (delta={delta:.4f})")
            
    # 2. Duration growth check
    mu_idx_05 = next(i for i, val in enumerate(mean_fear_grid) if np.isclose(val, 0.5))
    mult_idx_06 = next(i for i, val in enumerate(seed_multiples) if np.isclose(val, 0.6))
    
    print("\nCascade Duration Growth Check at mu=0.5, seed_multiple=0.6 (a=6):")
    durations_a6 = []
    for x in x_values:
        dur = mean_duration_grid[x][mu_idx_05, mult_idx_06]
        durations_a6.append(dur)
        print(f"  X={x}: mean duration = {dur:.2f} rounds")
        
    if durations_a6[0] < durations_a6[1] < durations_a6[2]:
        print("✅ PASS: Cascade duration grows monotonically with X!")
    else:
        print("❌ FAIL: Cascade duration is not monotonically growing with X.")
        
    print("\nOverall Average Duration at mu=0.5:")
    for x in x_values:
        avg_dur_mu05 = np.mean(mean_duration_grid[x][mu_idx_05, :])
        print(f"  X={x}: overall average duration = {avg_dur_mu05:.2f} rounds")

    plot_figures(mean_fear_grid, seed_multiples, p_systemic_grid, mean_duration_grid, durations_a6, x_values)

def plot_figures(mean_fear_grid, seed_multiples, p_systemic_grid, mean_duration_grid, durations_a6, x_values):
    print("\n=== Step 3: Generating Plots ===")
    figures_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    # Plot 1: P(systemic) overlay showing collapse
    plt.figure(figsize=(10, 6))
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(mean_fear_grid)))
    
    for i, mu in enumerate(mean_fear_grid):
        color = colors[i]
        plt.plot(seed_multiples, p_systemic_grid[1][i, :], label=f"mu={mu}, X=1", linestyle="-", color=color, alpha=0.8)
        plt.plot(seed_multiples, p_systemic_grid[4][i, :], label=f"mu={mu}, X=4", linestyle="--", color=color, alpha=0.8)
        plt.plot(seed_multiples, p_systemic_grid[8][i, :], label=f"mu={mu}, X=8", linestyle=":", color=color, alpha=0.8)
        
    plt.xlabel("Seed Size Multiple (a / a_c)")
    plt.ylabel("P(systemic)")
    plt.title("Memory-Window X-Invariance: P(systemic) Overlay")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")
    plt.tight_layout()
    
    invariance_plot_path = os.path.join(figures_dir, "window_r2_invariance.png")
    plt.savefig(invariance_plot_path, dpi=300)
    plt.close()
    print(f"Saved boundary invariance overlay plot to {invariance_plot_path}")
    
    # Plot 2: Cascade duration vs X at mu=0.5
    plt.figure(figsize=(8, 5))
    x_labels = [f"X={x}" for x in x_values]
    
    mu_idx_05 = next(i for i, val in enumerate(mean_fear_grid) if np.isclose(val, 0.5))
    overall_avgs = [np.mean(mean_duration_grid[x][mu_idx_05, :]) for x in x_values]
    
    x_indices = np.arange(len(x_values))
    plt.bar(x_indices - 0.2, durations_a6, width=0.4, label="Pilot Point (a=6, mu=0.5)", color="royalblue", alpha=0.8)
    plt.bar(x_indices + 0.2, overall_avgs, width=0.4, label="Overall Average (mu=0.5)", color="orange", alpha=0.8)
    
    plt.xticks(x_indices, x_labels)
    plt.xlabel("Memory Window Length (X)")
    plt.ylabel("Cascade Duration (rounds)")
    plt.title("Cascade Duration vs. Memory Window Length X")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    
    duration_plot_path = os.path.join(figures_dir, "window_r2_duration.png")
    plt.savefig(duration_plot_path, dpi=300)
    plt.close()
    print(f"Saved cascade duration plot to {duration_plot_path}")

if __name__ == "__main__":
    run_simulations()
    analyze_results()
