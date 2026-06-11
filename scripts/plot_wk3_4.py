import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.analysis import analyze_sweep, load_raw_results
from twocascade.plotting import plot_mu_sweep, plot_bimodality_histograms, plot_critical_scaling_validation, apply_plot_style

def generate_plots_for_r(r_val):
    raw_path = os.path.join(base_dir, "results", "raw", f"sweep_wk3_4_r{r_val}.json")
    figures_dir = os.path.join(base_dir, "results", "figures")
    
    if not os.path.exists(raw_path):
        print(f"File {raw_path} not found.")
        return
        
    print(f"Loading raw results from: {raw_path}")
    raw_data = load_raw_results(raw_path)
    
    print(f"Running sweep analysis for r={r_val}...")
    analyzed = analyze_sweep(raw_data)
    
    # Custom filenames for Wk 3-4 plots
    apply_plot_style()
    fig, ax = plt.subplots(figsize=(7, 5))
    cells = analyzed["processed_cells"]
    multiples_data = {}
    for cell in cells:
        mult = cell["seed_multiple"]
        if mult not in multiples_data:
            multiples_data[mult] = {"mu": [], "p_sys": []}
        multiples_data[mult]["mu"].append(cell["mean_fear"])
        multiples_data[mult]["p_sys"].append(cell["p_systemic"])
        
    colors = plt.cm.coolwarm(np.linspace(0.1, 0.9, len(multiples_data)))
    for idx, (mult, data) in enumerate(sorted(multiples_data.items())):
        sort_idx = np.argsort(data["mu"])
        mu_sorted = np.array(data["mu"])[sort_idx]
        psys_sorted = np.array(data["p_sys"])[sort_idx]
        ax.plot(mu_sorted, psys_sorted, "o-", label=f"$a = {mult}a_c(0)$", color=colors[idx], linewidth=2)
        
    ax.axhline(0.5, color="gray", linestyle=":", alpha=0.7)
    ax.set_xlabel("Mean Global Fear ($\\mu$)")
    ax.set_ylabel("Probability of Systemic Cascade ($P(\\text{systemic})$)")
    ax.set_title(f"1-D $\\mu$-Sweep ($N=1000, r={r_val}$)")
    ax.set_xlim(-0.02, 0.92)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(title="Initial Seed Size")
    
    filepath = os.path.join(figures_dir, f"wk3_4_mu_sweep_r{r_val}.png")
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"Saved {filepath}")
    
    # 2. Bimodality Histograms for mu=0.3
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
        
    # 3. Scaling Validation
    apply_plot_style()
    emp_thresholds = analyzed["empirical_thresholds"]
    grid_floor = r_val
    min_seed_size = min(cell["seed_size"] for cell in cells) if cells else 0
    
    mu_vals = []
    a_emp_vals = []
    for mu_str, a_emp in emp_thresholds.items():
        if a_emp is not None and not np.isnan(a_emp):
            a_val = float(a_emp)
            if a_val > grid_floor and a_val > min_seed_size:
                mu_vals.append(float(mu_str))
                a_emp_vals.append(a_val)
                
    sort_idx = np.argsort(mu_vals)
    mu_sorted = np.array(mu_vals)[sort_idx]
    a_emp_sorted = np.array(a_emp_vals)[sort_idx]
    
    if len(a_emp_sorted) > 0:
        mu0_idx = np.argmin(np.abs(mu_sorted))
        a_emp_0 = a_emp_sorted[mu0_idx]
        if a_emp_0 > 0.0 and not np.isnan(a_emp_0):
            ratio_emp = a_emp_sorted / a_emp_0
            mu_dense = np.linspace(0.0, 0.9, 100)
            from twocascade.meanfield import scaling_ratio
            ratio_theory = scaling_ratio(mu_dense, r_val)
            
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.plot(mu_dense, ratio_theory, "-", color="#1f77b4", label=f"Theoretical $(1-\\mu)^{{{r_val}/({r_val}-1)}}$", linewidth=2.5)
            ax.plot(mu_sorted, ratio_emp, "o", color="#d62728", label="Empirical Crossings", markersize=8)
            ax.set_xlabel("Mean Global Fear ($\\mu$)")
            ax.set_ylabel("Empirical Crossing Threshold Ratio")
            ax.set_title(f"Critical Threshold Scaling vs Theory ($r={r_val}$)")
            ax.legend()
            ax.set_xlim(-0.02, 0.92)
            ax.set_ylim(-0.05, 1.05)
            
            filepath = os.path.join(figures_dir, f"wk3_4_scaling_validation_r{r_val}.png")
            plt.savefig(filepath, dpi=300)
            plt.close()
            print(f"Saved {filepath}")

if __name__ == "__main__":
    for r in [2, 3, 4]:
        generate_plots_for_r(r)
