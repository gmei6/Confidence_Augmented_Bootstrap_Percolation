"""
Plotting module to generate professional figures for reporting.
"""

import os
from typing import Dict, Any, Optional
import numpy as np
import matplotlib.pyplot as plt
from twocascade.meanfield import scaling_ratio, critical_seed_scaling
from twocascade.analysis import evaluate_scaling_adherence

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

def plot_mu_sweep(analyzed_data: Dict[str, Any], output_dir: str, filename: str = "mu_sweep_1d.png", title: Optional[str] = None) -> None:
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
    
    if title is None:
        r = analyzed_data["metadata"]["r"]
        n = analyzed_data["metadata"]["n"]
        ax.set_title(f"1-D $\\mu$-Sweep ($N={n}, r={r}$)")
    else:
        ax.set_title(title)
        
    ax.set_xlim(-0.02, 0.92)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(title="Initial Seed Size")
    
    filepath = os.path.join(output_dir, filename)
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

def plot_critical_scaling_validation(analyzed_data: Dict[str, Any], output_dir: str, filename: str = "scaling_validation.png", adherence: Optional[Dict[str, Any]] = None) -> None:
    """
    Plot empirical threshold ratio vs mu and overlay theoretical scaling law (1-mu)**(r/(r-1)).
    
    Raises:
        ValueError: If the mu=0 baseline threshold is missing or corrupted.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    if adherence is None:
        adherence = evaluate_scaling_adherence(analyzed_data)
        
    r = analyzed_data["metadata"]["r"]
    
    mu_vals = []
    ratio_emp_vals = []
    
    for row in adherence["results_table"]:
        if not row["is_clamped"] and row["ratio_emp"] is not None:
            mu_vals.append(row["mu"])
            ratio_emp_vals.append(row["ratio_emp"])
            
    if len(mu_vals) == 0:
        print(f"Warning: No valid empirical crossing points found for scaling validation plot (r={r}).")
        return
        
    mu_dense = np.linspace(0.0, 0.9, 100)
    ratio_theory = scaling_ratio(mu_dense, r)
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(mu_dense, ratio_theory, "-", color="#1f77b4", label=f"Theoretical $(1-\\mu)^{{{r}/({r}-1)}}$", linewidth=2.5)
    ax.plot(mu_vals, ratio_emp_vals, "o", color="#d62728", label="Empirical Crossings", markersize=8)
    
    ax.set_xlabel("Mean Global Fear ($\\mu$)")
    ax.set_ylabel("Empirical Crossing Threshold Ratio")
    ax.set_title(f"Critical Threshold Scaling vs Theory ($r={r}$)")
    ax.legend()
    ax.set_xlim(-0.02, 0.92)
    ax.set_ylim(-0.05, 1.05)
    
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()

def plot_phase_diagram_overlay(analyzed_data: Dict[str, Any], output_dir: str, filename: str, adherence: Dict[str, Any]) -> None:
    """
    Plot P(systemic) as a 2D phase diagram heatmap (initial seed size a vs. mean fear mu)
    and overlay the theoretical critical threshold a_c(mu) and empirical crossing points.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    meta = analyzed_data["metadata"]
    r = meta["r"]
    n = meta["n"]
    p = meta["p"]
    
    # Extract unique sorted mean_fear and seed_size grids
    cells = analyzed_data["processed_cells"]
    mean_fear_grid = sorted(list(set(cell["mean_fear"] for cell in cells)))
    seed_size_grid = sorted(list(set(cell["seed_size"] for cell in cells)))
    
    # Construct 2D matrix of P(systemic)
    p_sys_matrix = np.zeros((len(seed_size_grid), len(mean_fear_grid)))
    
    size_to_idx = {size: idx for idx, size in enumerate(seed_size_grid)}
    mu_to_idx = {mu: idx for idx, mu in enumerate(mean_fear_grid)}
    
    for cell in cells:
        mu = cell["mean_fear"]
        a = cell["seed_size"]
        p_sys = cell["p_systemic"]
        p_sys_matrix[size_to_idx[a], mu_to_idx[mu]] = p_sys
        
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot P(systemic) heatmap
    X, Y = np.meshgrid(mean_fear_grid, seed_size_grid)
    mesh = ax.pcolormesh(X, Y, p_sys_matrix, cmap="RdBu_r", shading="auto", vmin=0, vmax=1, alpha=0.85)
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_label("Probability of Systemic Cascade $P(\\text{systemic})$")
    
    # Plot empirical crossings (where P(systemic) = 0.5)
    mu_emp = []
    a_emp = []
    for row in adherence["results_table"]:
        if not row["is_clamped"] and row["a_emp"] is not None:
            mu_emp.append(row["mu"])
            a_emp.append(row["a_emp"])
            
    ax.plot(mu_emp, a_emp, "o", color="#d62728", label="Empirical Crossings ($P=0.5$)", markersize=8, markeredgecolor="black")
    
    # Plot raw theoretical critical threshold a_c(mu)
    mu_dense = np.linspace(0.0, 0.9, 200)
    a_c_raw = np.array([critical_seed_scaling(n, p, r, mu) for mu in mu_dense])
    ax.plot(mu_dense, a_c_raw, "-", color="#2ca02c", label="Asymptotic Theoretical $a_c(\\mu)$", linewidth=2.5)
    
    # Plot empirical-anchored/scaled theoretical shape
    a_emp_0 = adherence["a_emp_0"]
    a_c_scaled = a_emp_0 * np.array([scaling_ratio(mu, r) for mu in mu_dense])
    ax.plot(mu_dense, a_c_scaled, "--", color="black", label="Scaled Theory $a_{\\text{emp}}(0)(1-\\mu)^{r/(r-1)}$", linewidth=2)
    
    # Annotate finite size offset
    a_c_0_theory = critical_seed_scaling(n, p, r, 0.0)
    offset_pct = (a_emp_0 / a_c_0_theory - 1.0) * 100
    
    ax.annotate(
        f"Finite-size offset at $\\mu=0$: +{offset_pct:.1f}%\n($a_{{emp}}(0)={a_emp_0:.2f}$ vs $a_c(0)={a_c_0_theory:.2f}$)",
        xy=(0.02, (a_emp_0 + a_c_0_theory) / 2),
        xytext=(0.15, (a_emp_0 + a_c_0_theory) / 2 + (10 if r > 2 else 2)),
        arrowprops=dict(facecolor='black', arrowstyle='->', shrinkA=0, shrinkB=0),
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5)
    )
    
    ax.set_xlabel("Mean Global Fear ($\\mu$)")
    ax.set_ylabel("Initial Seed Size ($a$)")
    ax.set_title(f"Systemic Collapse Phase Diagram ($N={n}, r={r}$)")
    ax.set_xlim(-0.02, 0.92)
    ax.set_ylim(min(seed_size_grid) - 0.5, max(seed_size_grid) + 0.5)
    ax.legend(loc="upper right")
    
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
