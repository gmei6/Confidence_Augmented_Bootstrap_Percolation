"""
Plotting module to generate professional figures for reporting.
"""

import os
from typing import Dict, Any
import numpy as np
import matplotlib.pyplot as plt
from twocascade.meanfield import scaling_ratio

def apply_plot_style() -> None:
    """Set professional design standards for matplotlib."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "figure.constrained_layout.use": True
    })

def plot_mu_sweep(analyzed_data: Dict[str, Any], output_dir: str) -> None:
    """Plot P(systemic) vs. mean fear mu for curves of seed size multiples."""
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(7, 5))
    
    cells = analyzed_data["processed_cells"]
    
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
    ax.set_title("1-D $\\mu$-Sweep ($N=2000, r=2$)")
    ax.set_xlim(-0.02, 0.92)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(title="Initial Seed Size")
    
    filepath = os.path.join(output_dir, "mu_sweep_1d.png")
    plt.savefig(filepath, dpi=300)
    plt.close()

def plot_bimodality_histograms(analyzed_data: Dict[str, Any], selected_mu: float, output_dir: str) -> None:
    """Plot failed fraction histograms for subcritical, near-critical, and supercritical seeds."""
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    available_mus = sorted(list(set(c["mean_fear"] for c in analyzed_data["processed_cells"])))
    if not any(abs(mu - selected_mu) < 1e-9 for mu in available_mus):
        if available_mus:
            original_mu = selected_mu
            selected_mu = min(available_mus, key=lambda mu: abs(mu - selected_mu))
            print(f"Warning: Selected mu={original_mu} not found in data. Dynamically resolved to closest mu={selected_mu}")
        else:
            raise ValueError("No simulation data found in processed_cells.")
            
    cells = [c for c in analyzed_data["processed_cells"] if abs(c["mean_fear"] - selected_mu) < 1e-9]
    if not cells:
        raise ValueError(f"No simulation data found for mu = {selected_mu}")
        
    available_multiples = sorted(list(set(c["seed_multiple"] for c in cells)))
    target_multiples = [0.5, 1.0, 1.5]
    if not all(m in available_multiples for m in target_multiples):
        if len(available_multiples) >= 3:
            target_multiples = [available_multiples[0], available_multiples[len(available_multiples)//2], available_multiples[-1]]
        else:
            target_multiples = available_multiples
            
    selected_cells = {c["seed_multiple"]: c for c in cells if c["seed_multiple"] in target_multiples}
    
    fig, axes = plt.subplots(1, len(target_multiples), figsize=(4 * len(target_multiples), 4), sharey=True)
    if len(target_multiples) == 1:
        axes = [axes]
        
    bins = np.linspace(0.0, 1.0, 31)
    titles = {}
    for m in target_multiples:
        if m < 0.9:
            lbl = "Subcritical"
        elif abs(m - 1.0) < 1e-9:
            lbl = "Near-Critical"
        else:
            lbl = "Supercritical"
        titles[m] = f"{lbl} ($a={m}a_c$, $\\mu={selected_mu}$)"
        
    # Pick colors based on number of subplots
    import matplotlib
    cmap = matplotlib.colormaps["tab10"] if len(target_multiples) > 3 else lambda idx: ["#3182bd", "#e6550d", "#de2d26"][idx]
    
    for i, mult in enumerate(target_multiples):
        ax = axes[i]
        cell = selected_cells.get(mult)
        if cell is None:
            continue
            
        ffs = cell["failed_fractions"]
        color = cmap(i) if len(target_multiples) > 3 else cmap[i] if isinstance(cmap, list) else cmap(i)
        ax.hist(ffs, bins=bins, weights=np.ones_like(ffs) / len(ffs), color=color, edgecolor="black", alpha=0.7)
        ax.axvline(0.5, color="black", linestyle="--", linewidth=1.5, label="Threshold $\\theta=0.5$")
        ax.set_title(titles[mult])
        ax.set_xlabel("Final Failed Fraction ($|A^*|/n$)")
        if i == 0:
            ax.set_ylabel("Relative Frequency")
            
    filepath = os.path.join(output_dir, "bimodality_histograms.png")
    plt.savefig(filepath, dpi=300)
    plt.close()

def plot_critical_scaling_validation(analyzed_data: Dict[str, Any], output_dir: str) -> None:
    """Plot empirical threshold ratio vs mu and overlay theoretical scaling law (1-mu)^2."""
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    emp_thresholds = analyzed_data["empirical_thresholds"]
    r = analyzed_data["metadata"]["r"]
    
    grid_floor = r
    min_seed_size = min(cell["seed_size"] for cell in analyzed_data["processed_cells"]) if "processed_cells" in analyzed_data else 0
    
    mu_vals = []
    a_emp_vals = []
    
    for mu_str, a_emp in emp_thresholds.items():
        if a_emp is not None and not np.isnan(a_emp):
            a_val = float(a_emp)
            # Filter out clamped crossing points
            if a_val > grid_floor and a_val > min_seed_size:
                mu_vals.append(float(mu_str))
                a_emp_vals.append(a_val)
            
    sort_idx = np.argsort(mu_vals)
    mu_sorted = np.array(mu_vals)[sort_idx]
    a_emp_sorted = np.array(a_emp_vals)[sort_idx]
    
    if len(a_emp_sorted) == 0:
        print("Warning: No valid empirical crossing points found for Plot 3.")
        return
        
    mu0_idx = np.argmin(np.abs(mu_sorted))
    a_emp_0 = a_emp_sorted[mu0_idx]
    
    if a_emp_0 == 0.0 or np.isnan(a_emp_0) or a_emp_0 is None:
         print("Warning: Empirical threshold at mu=0 is invalid (0, NaN, or None). Skipping scaling validation plot.")
         return
         
    ratio_emp = a_emp_sorted / a_emp_0
    
    mu_dense = np.linspace(0.0, 0.9, 100)
    ratio_theory = scaling_ratio(mu_dense, r)
    
    fig, ax = plt.subplots(figsize=(7, 5))
    
    ax.plot(mu_dense, ratio_theory, "-", color="#1f77b4", label=f"Theoretical $(1-\\mu)^{{{r}/({r}-1)}}$", linewidth=2.5)
    ax.plot(mu_sorted, ratio_emp, "o", color="#d62728", label="Empirical Crossings $a_{\\text{emp}}(\\mu)/a_{\\text{emp}}(0)$", markersize=8)
    
    ax.set_xlabel("Mean Global Fear ($\\mu$)")
    ax.set_ylabel("Empirical Crossing Threshold Ratio")
    ax.set_title(f"Critical Threshold Scaling vs Theory ($r={r}$)")
    ax.legend()
    ax.set_xlim(-0.02, 0.92)
    ax.set_ylim(-0.05, 1.05)
    
    filepath = os.path.join(output_dir, "scaling_validation.png")
    plt.savefig(filepath, dpi=300)
    plt.close()

if __name__ == "__main__":
    import json
    from twocascade.analysis import analyze_sweep, load_raw_results
    
    # Path setup
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_path = os.path.join(base_dir, "results", "raw", "sweep_week2.json")
    figures_dir = os.path.join(base_dir, "results", "figures")
    
    print(f"Loading raw results from: {raw_path}")
    raw_data = load_raw_results(raw_path)
    
    print("Running sweep analysis...")
    analyzed = analyze_sweep(raw_data)
    
    print("Generating mu sweep plot...")
    plot_mu_sweep(analyzed, figures_dir)
    
    # Default selected_mu to 0.3
    selected_mu = 0.3
    print("Generating bimodality histograms...")
    plot_bimodality_histograms(analyzed, selected_mu, figures_dir)
    
    print("Generating critical scaling validation plot...")
    plot_critical_scaling_validation(analyzed, figures_dir)
    
    print("All plots generated successfully.")
