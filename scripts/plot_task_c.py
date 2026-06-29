import os
import sys
import json
import matplotlib.pyplot as plt

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.plotting import apply_plot_style

def plot_comparison():
    apply_plot_style()
    
    analysis_path = os.path.join(base_dir, "results", "analysis", "targeted_seeding_adherence.json")
    if not os.path.exists(analysis_path):
        print(f"Analysis file not found at {analysis_path}. Please run run_task_c.py first.")
        sys.exit(1)
        
    with open(analysis_path, "r") as f:
        payload = json.load(f)
        
    empirical_thresholds = payload["empirical_thresholds"]
    n_values = payload["metadata"]["n_values"]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    
    for idx, n_str in enumerate(map(str, n_values)):
        ax = axes[idx]
        data = empirical_thresholds[n_str]
        
        rand_thresh = data["random"]
        targ_thresh = data["targeted"]
        
        mus_str = sorted(rand_thresh.keys(), key=float)
        mus = [float(m) for m in mus_str]
        rand_y = [rand_thresh[m] for m in mus_str]
        targ_y = [targ_thresh.get(m) for m in mus_str]
        
        # Filter out None/NaN for plotting lines
        rand_plot_x, rand_plot_y = [], []
        for mu, y in zip(mus, rand_y):
            if y is not None:
                rand_plot_x.append(mu)
                rand_plot_y.append(y)
                
        targ_plot_x, targ_plot_y = [], []
        for mu, y in zip(mus, targ_y):
            if y is not None:
                targ_plot_x.append(mu)
                targ_plot_y.append(y)
        
        ax.plot(rand_plot_x, rand_plot_y, 'o-', color='#1f77b4', label='Random Seeding', linewidth=2)
        ax.plot(targ_plot_x, targ_plot_y, 's--', color='#ff7f0e', label='Targeted (High-Degree)', linewidth=2)
        
        ax.set_title(f"Boundary $a_{{emp}}(\\mu)$ for $N = {n_str}$", fontsize=13)
        ax.set_xlabel("Mean Fear $\\mu$", fontsize=11)
        if idx == 0:
            ax.set_ylabel("Empirical Critical Seed Size $a_{emp}$", fontsize=11)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(fontsize=10)
        
    plt.tight_layout()
    figures_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    fig_path = os.path.join(figures_dir, "targeted_seeding_comparison.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Generated comparison plot from analysis artifact at: {fig_path}")

if __name__ == "__main__":
    plot_comparison()
