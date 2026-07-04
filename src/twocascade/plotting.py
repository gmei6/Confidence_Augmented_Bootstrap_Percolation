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


def plot_theta_robustness(analyzed_sweeps_by_theta: Dict[str, Dict[str, Any]], output_dir: str, filename: str = "theta_robustness.png") -> None:
    """
    Plot empirical critical seed boundaries a_c(mu) for different theta values to show robustness.
    
    Args:
        analyzed_sweeps_by_theta: Dict mapping stringified theta (e.g., "0.35") to analyzed sweep data.
        output_dir: Directory to save the generated plot.
        filename: Output image filename.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Sort the stringified thetas by their float values
    sorted_thetas = sorted(analyzed_sweeps_by_theta.keys(), key=float)
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(sorted_thetas)))
    
    first_sweep = next(iter(analyzed_sweeps_by_theta.values()))
    meta = first_sweep["metadata"]
    n = meta["n"]
    p = meta["p"]
    r = meta["r"]
    
    mu_dense = np.linspace(0.0, 0.9, 200)
    a_c_raw = np.array([critical_seed_scaling(n, p, r, mu) for mu in mu_dense])
    ax.plot(mu_dense, a_c_raw, ":", color="gray", label="Asymptotic $a_c(\\mu)$ Theory", linewidth=1.5)
    
    for idx, theta_str in enumerate(sorted_thetas):
        sweep = analyzed_sweeps_by_theta[theta_str]
        emp_thresholds = sweep["empirical_thresholds"]
        
        mu_vals = []
        a_emp_vals = []
        
        for mu_str, a_emp in emp_thresholds.items():
            if a_emp is not None and not np.isnan(a_emp):
                mu_vals.append(float(mu_str))
                a_emp_vals.append(float(a_emp))
                
        if len(mu_vals) > 0:
            sort_idx = np.argsort(mu_vals)
            mu_sorted = np.array(mu_vals)[sort_idx]
            a_emp_sorted = np.array(a_emp_vals)[sort_idx]
            
            ax.plot(mu_sorted, a_emp_sorted, "o-", label=f"$\\theta = {theta_str}$", color=colors[idx], linewidth=2, markersize=5)
            
    ax.set_xlabel("Mean Global Fear ($\\mu$)")
    ax.set_ylabel("Critical Seed Size Threshold ($a_{\\text{emp}}$)")
    ax.set_title(f"Boundary Robustness to Systemic Threshold $\\theta$ ($N={n}, r={r}$)")
    ax.set_xlim(-0.02, 0.92)
    ax.legend(title="Systemic Threshold")
    
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()


def plot_kappa_robustness(analyzed_sweeps_by_kappa: Dict[str, Dict[str, Any]], output_dir: str, filename: str = "kappa_robustness_r2.png") -> None:
    """
    Plot empirical critical seed boundaries a_c(mu) for different concentration kappa values.
    
    Args:
        analyzed_sweeps_by_kappa: Dict mapping stringified kappa (e.g., "50.0") to analyzed sweep data.
        output_dir: Directory to save the generated plot.
        filename: Output image filename.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Sort the stringified kappas by their float values
    sorted_kappas = sorted(analyzed_sweeps_by_kappa.keys(), key=float)
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(sorted_kappas)))
    
    first_sweep = next(iter(analyzed_sweeps_by_kappa.values()))
    meta = first_sweep["metadata"]
    n = meta["n"]
    p = meta["p"]
    r = meta["r"]
    
    min_seed_size = r
    for sweep in analyzed_sweeps_by_kappa.values():
        cells = sweep.get("processed_cells", [])
        if cells:
            min_seed_size = min(min_seed_size, min(cell["seed_size"] for cell in cells))
            
    mu_dense = np.linspace(0.0, 0.9, 200)
    a_c_raw = np.array([critical_seed_scaling(n, p, r, mu) for mu in mu_dense])
    ax.plot(mu_dense, a_c_raw, ":", color="gray", label="Asymptotic $a_c(\\mu)$ Theory", linewidth=1.5)
    ax.axhline(min_seed_size, color="red", linestyle="--", linewidth=1.2, alpha=0.6, label=f"Physical Floor ($a={min_seed_size}$)")
    
    for idx, kappa_str in enumerate(sorted_kappas):
        sweep = analyzed_sweeps_by_kappa[kappa_str]
        emp_thresholds = sweep["empirical_thresholds"]
        
        mu_vals = []
        a_emp_vals = []
        
        for mu_str, a_emp in emp_thresholds.items():
            if a_emp is not None and not np.isnan(a_emp):
                mu_vals.append(float(mu_str))
                a_emp_vals.append(float(a_emp))
                
        if len(mu_vals) > 0:
            sort_idx = np.argsort(mu_vals)
            mu_sorted = np.array(mu_vals)[sort_idx]
            a_emp_sorted = np.array(a_emp_vals)[sort_idx]
            
            is_clamped = a_emp_sorted <= min_seed_size
            valid_mask = ~is_clamped
            clamped_mask = is_clamped
            
            ax.plot(mu_sorted, a_emp_sorted, "-", color=colors[idx], linewidth=2, alpha=0.8)
            
            if np.any(valid_mask):
                ax.plot(mu_sorted[valid_mask], a_emp_sorted[valid_mask], "o", 
                        color=colors[idx], label=f"$\\kappa = {kappa_str}$", markersize=6)
            if np.any(clamped_mask):
                ax.plot(mu_sorted[clamped_mask], a_emp_sorted[clamped_mask], "s", 
                        markerfacecolor="none", markeredgecolor=colors[idx], markersize=6, markeredgewidth=1.5)
                
    ax.set_xlabel("Mean Global Fear ($\\mu$)")
    ax.set_ylabel("Critical Seed Size Threshold ($a_{\\text{emp}}$)")
    ax.set_title(f"Boundary Sensitivity to Heterogeneity $\\kappa$ ($N={n}, r={r}$)")
    ax.set_xlim(-0.02, 0.92)
    ax.legend(title="Beta Concentration")

    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()


def plot_overdispersion_ratio(dispersion_rows: list, t_round: int, r: int, output_dir: str,
                              filename: str = "counting_process_overdispersion_r2.png") -> None:
    """
    Plot the overdispersion ratio D_t at a fixed round t vs system size n,
    one curve per mean fear mu, one panel per seed multiple (log-log axes).

    Args:
        dispersion_rows: List of dicts, one per (n, mu, seed_multiple) cell, each with keys
            "n", "mean_fear", "seed_multiple", "dispersion_ratio", "ci_low", "ci_high".
        t_round: The fixed round t the dispersion was evaluated at (title/label only).
        r: Solvency threshold (title only).
        output_dir: Directory to save the generated plot.
        filename: Output image filename.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)

    multiples = sorted(set(row["seed_multiple"] for row in dispersion_rows))
    mus = sorted(set(row["mean_fear"] for row in dispersion_rows))
    colors = plt.cm.plasma(np.linspace(0.1, 0.75, len(mus)))

    fig, axes = plt.subplots(1, len(multiples), figsize=(6 * len(multiples), 5), sharey=True)
    if len(multiples) == 1:
        axes = [axes]

    for ax, mult in zip(axes, multiples):
        for mu, color in zip(mus, colors):
            rows = sorted(
                (row for row in dispersion_rows
                 if row["seed_multiple"] == mult and row["mean_fear"] == mu
                 and np.isfinite(row["dispersion_ratio"])),
                key=lambda row: row["n"]
            )
            if not rows:
                continue
            n_vals = np.array([row["n"] for row in rows], dtype=float)
            d_vals = np.array([row["dispersion_ratio"] for row in rows])
            err_lo = d_vals - np.array([row["ci_low"] for row in rows])
            err_hi = np.array([row["ci_high"] for row in rows]) - d_vals
            ax.errorbar(n_vals, d_vals, yerr=[np.clip(err_lo, 0, None), np.clip(err_hi, 0, None)],
                        fmt="o-", color=color, linewidth=2, markersize=6, capsize=4,
                        label=f"$\\mu = {mu}$")

        ax.axhline(1.0, color="gray", linestyle=":", linewidth=1.5, label="Binomial ($D_t = 1$)")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("System Size ($n$)")
        ax.set_title(f"$a = {mult}\\,a_c(0)$")
        ax.legend()

    axes[0].set_ylabel(f"Overdispersion Ratio $D_{{t={t_round}}}$")
    fig.suptitle(f"Counting-Process Overdispersion vs Binomial Benchmark ($t = {t_round}$, $r = {r}$)")

    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()


def plot_fear_field_concentration(concentration: Dict[str, Any], output_dir: str, filename: str = "fear_concentration_relvar_r2.png") -> None:
    """
    Plot the across-trial relative variance of the fear field g_k vs. system size n
    on log-log axes (Task E), one panel per (mean_fear, seed_multiple) cell, one
    series per active round k, annotated with the fitted decay rate gamma from
    log(rel var) ~ -gamma log(n). Expects the output of
    analyze_fear_field_concentration.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)

    cells = concentration["cells"]
    n_values = np.array(concentration["n_values"], dtype=float)

    ncols = 2
    nrows = int(np.ceil(len(cells) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(5.0 * ncols, 4.0 * nrows), sharex=True, sharey=True)
    axes = np.atleast_1d(axes).ravel()

    # Okabe-Ito colorblind-safe hues, fixed order per round; marker shape as secondary encoding.
    round_colors = ["#0072B2", "#E69F00", "#009E73"]
    round_markers = ["o", "s", "^"]

    guide_anchor = None
    for ax, cell in zip(axes, cells):
        for idx, entry in enumerate(cell["per_round"]):
            k = entry["round"]
            pts = [(n, rv) for n, rv in zip(n_values, entry["rel_var"]) if rv is not None and rv > 0.0]
            if not pts:
                continue
            xs = np.array([n for n, _ in pts])
            ys = np.array([rv for _, rv in pts])
            fit = entry["fit"]
            if fit is not None and fit["gamma_err"] is not None:
                label = f"$k={k}$ ($\\hat\\gamma = {fit['gamma']:.2f} \\pm {fit['gamma_err']:.2f}$)"
            elif fit is not None:
                label = f"$k={k}$ ($\\hat\\gamma = {fit['gamma']:.2f}$)"
            else:
                label = f"$k={k}$"
            ax.plot(xs, ys, linestyle="-", marker=round_markers[idx % len(round_markers)],
                    color=round_colors[idx % len(round_colors)], linewidth=2, markersize=6, label=label)
            if guide_anchor is None:
                guide_anchor = (xs[0], ys[0])

        # 1/n reference guide (slope -1 in log-log), anchored to the first plotted point.
        if guide_anchor is not None:
            ax.plot(n_values, guide_anchor[1] * guide_anchor[0] / n_values,
                    linestyle=":", color="gray", linewidth=1.5, label="$\\propto 1/n$")

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"$\\mu = {cell['mean_fear']}$, $a = {cell['seed_multiple']}\\,a_c$")
        ax.legend(fontsize=9)

    for ax in axes[len(cells):]:
        ax.set_visible(False)
    for ax in axes.reshape(nrows, ncols)[-1, :]:
        ax.set_xlabel("System Size ($n$)")
    for ax in axes.reshape(nrows, ncols)[:, 0]:
        ax.set_ylabel("$\\mathrm{Var}(g_k) / \\mathbb{E}[g_k]^2$")

    fig.suptitle("Fear-Field Trajectory Concentration ($r=2$): Relative Variance vs. $n$")

def plot_extended_scaling_validation(fits_by_r: Dict[int, list], output_dir: str, filename: str = "extended_scaling_validation.png") -> None:
    """
    Plot empirical threshold ratio vs mu for r in {2, 3, 4} and overlay theoretical scaling law.
    
    Args:
        fits_by_r: Dictionary mapping r to a list of fit dicts (as returned by fit_scaling_exponent).
        output_dir: Output directory.
        filename: Output filename.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    if not isinstance(axes, np.ndarray):
        axes = [axes]
        
    r_values = sorted(fits_by_r.keys())
    
    mu_dense = np.linspace(0.0, 0.9, 200)
    
    for i, r in enumerate(r_values):
        ax = axes[i]
        fits = fits_by_r[r]
        
        # Plot theoretical curve
        gamma_theory = r / (r - 1.0)
        ratio_theory = (1.0 - mu_dense) ** gamma_theory
        ax.plot(mu_dense, ratio_theory, "--", color="black", label=f"Theory $(1-\\mu)^{{{r}/({r}-1)}}$", linewidth=2.5)
        
        # Collect points across all system sizes
        n_values = sorted({fit["n"] for fit in fits})
        colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(n_values)))
        
        for idx, n in enumerate(n_values):
            # Find the fit for this n
            fit = next((f for f in fits if f["n"] == n), None)
            if fit is None:
                continue
            
            mu_vals = []
            ratio_vals = []
            
            for pt in fit["points"]:
                if not pt["is_clamped"] and pt["ratio"] is not None:
                    mu_vals.append(pt["mu"])
                    ratio_vals.append(pt["ratio"])
                    
            if mu_vals:
                ax.plot(mu_vals, ratio_vals, "o", color=colors[idx], label=f"N={n}", markersize=6, alpha=0.8)
                
        ax.set_title(f"$r={r}$ (Theory $\\gamma={gamma_theory:.2f}$)")
        ax.set_xlabel("Mean Global Fear ($\\mu$)")
        if i == 0:
            ax.set_ylabel("Threshold Ratio $a_c(\\mu)/a_c(0)$")
            
        ax.set_xlim(-0.02, 0.92)
        ax.set_ylim(-0.05, 1.05)
        ax.legend()
        
    plt.tight_layout()
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()


def plot_clock_collapse_bias(bias_results: Dict[int, Dict[str, Any]], output_dir: str, filename: str = "clock_collapse_bias.png") -> None:
    r"""
    Plot the average and maximum clock-collapse bias E[\Delta P] vs a_{k-1}/n.
    """
    apply_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    n_values = sorted(bias_results.keys())
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(n_values)))
    
    for idx, n in enumerate(n_values):
        res = bias_results[n]
        ratios = res["ratios"]
        if not ratios:
            continue
            
        axes[0].plot(ratios, res["mean_bias"], "o", color=colors[idx], label=f"$n={n}$", markersize=4, alpha=0.7)
        axes[1].plot(ratios, res["max_bias"], "s", color=colors[idx], label=f"$n={n}$", markersize=4, alpha=0.7)
        
    axes[0].set_title("Average Bias $\\mathbb{E}[\\Delta P]$")
    axes[0].set_ylabel("$\\Delta P = P_{\\text{step}} - P_{\\text{gen}}$")
    axes[1].set_title("Maximum Bias $\\max(\\Delta P)$")
    
    for ax in axes:
        ax.set_xlabel("Generation Size Ratio ($a_{k-1}/n$)")
        ax.axhline(0, color="black", linestyle="--", alpha=0.5)
        ax.legend()
        
    fig.suptitle("Geometric Clock Collapse Bias ($P_{\\text{step}}$ vs $P_{\\text{gen}}$)")
    
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
