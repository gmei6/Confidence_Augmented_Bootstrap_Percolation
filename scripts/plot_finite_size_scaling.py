import os
import sys
import json
import math
import numpy as np
import matplotlib.pyplot as plt

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.analysis import load_raw_results, estimate_transition_width, fit_finite_size_exponent
from twocascade.plotting import apply_plot_style

def get_failed_fractions_by_multiple(raw_data, mu_target):
    results = raw_data["results"]
    failed_fractions_by_multiple = {}
    for cell in results:
        mu = float(cell["mean_fear"])
        if math.isclose(mu, mu_target, abs_tol=1e-9):
            mult = float(cell["seed_multiple"])
            failed_fractions_by_multiple[mult] = cell["failed_fractions"]
    return failed_fractions_by_multiple

def main():
    apply_plot_style()
    
    n_list = [1000, 2000, 5000]
    mu_list = [0.0, 0.3]
    theta = 0.5
    
    # Load all raw results
    raw_datasets = {}
    for n in n_list:
        raw_path = os.path.join(base_dir, "results", "raw", f"finite_size_r2_n{n}.json")
        if not os.path.exists(raw_path):
            print(f"Error: raw file not found at {raw_path}")
            sys.exit(1)
        raw_datasets[n] = load_raw_results(raw_path)
        
    # Get seed multiples from one of the datasets
    seed_multiples = raw_datasets[n_list[0]]["sweep_parameters"]["seed_multiples"]
    
    # Setup plotting: 1 row, 2 columns
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Colors and styles
    colors_mu = {0.0: "blue", 0.3: "orange"}
    markers_n = {1000: "o", 2000: "s", 5000: "^"}
    linestyles_n = {1000: ":", 2000: "--", 5000: "-"}
    
    widths_by_mu = {mu: [] for mu in mu_list}
    width_errs_by_mu = {mu: [] for mu in mu_list}
    
    for mu in mu_list:
        print(f"\n--- Analyzing mu = {mu} ---")
        for n in n_list:
            raw_data = raw_datasets[n]
            failed_fractions_by_multiple = get_failed_fractions_by_multiple(raw_data, mu)
            
            res = estimate_transition_width(
                failed_fractions_by_multiple=failed_fractions_by_multiple,
                theta=theta,
                seed_multiples=seed_multiples,
                bootstrap_reps=500,
                seed=20260629
            )
            
            w = res["width"]
            w_err = res["width_err"]
            ci = res["ci"]
            
            widths_by_mu[mu].append(w)
            width_errs_by_mu[mu].append(w_err)
            
            print(f"N = {n}: width = {w:.4f} +/- {w_err:.4f}, 95% CI = [{ci[0]:.4f}, {ci[1]:.4f}]")
            
            # Plot P(systemic) vs seed multiple on the left panel
            p_sys_dict = res["p_systemic"]
            multiples = sorted(seed_multiples)
            p_sys_vals = [p_sys_dict[m] for m in multiples]
            
            label = f"N={n}, $\\mu={mu}$"
            ax_left.plot(
                multiples, p_sys_vals,
                linestyle=linestyles_n[n],
                marker=markers_n[n],
                color=colors_mu[mu],
                label=label,
                alpha=0.8
            )
            
            # Plot logistic fit curve on the left panel (smooth curve)
            x_fit = np.linspace(min(multiples), max(multiples), 100)
            k_fit = res["k"]
            x0_fit = res["x0"]
            y_fit = 1.0 / (1.0 + np.exp(-np.clip(k_fit * (x_fit - x0_fit), -500, 500)))
            ax_left.plot(x_fit, y_fit, color=colors_mu[mu], alpha=0.3)
            
    # Perform exponent fitting on the right panel
    for mu in mu_list:
        widths = widths_by_mu[mu]
        width_errs = width_errs_by_mu[mu]
        
        fit = fit_finite_size_exponent(n_list, widths, width_errs)
        nu = fit["nu"]
        nu_err = fit["nu_err"]
        r2 = fit["r_squared"]
        slope = fit["slope"]
        intercept = fit["intercept"]
        
        print(f"mu = {mu}: nu = {nu:.4f} +/- {nu_err:.4f} (slope = {slope:.4f}, R2 = {r2:.4f})")
        
        # Plot points on right panel (log-log)
        ax_right.errorbar(
            n_list, widths, yerr=width_errs,
            fmt=markers_n[1000],
            color=colors_mu[mu],
            capsize=4,
            label=f"Data $\\mu={mu}$"
        )
        
        # Plot fit line
        n_fit = np.linspace(800, 6000, 100)
        w_fit = np.exp(slope * np.log(n_fit) + intercept)
        ax_right.loglog(
            n_fit, w_fit,
            linestyle="-",
            color=colors_mu[mu],
            label=f"Fit $\\mu={mu}$ ($\\nu={nu:.2f} \\pm {nu_err:.2f}$)"
        )
        
    # Formatting Left Panel
    ax_left.set_xlabel("Seed Multiple ($a / a_c(0)$)")
    ax_left.set_ylabel("$P(\\text{systemic})$")
    ax_left.set_title("Systemic Collapse Probability $P(\\text{systemic})$ vs. Seed Multiple\n(Transition Sharpening)")
    ax_left.axhline(0.5, color="gray", linestyle=":")
    ax_left.axvline(1.0, color="gray", linestyle=":")
    ax_left.legend(loc="lower right")
    ax_left.grid(True)
    
    # Formatting Right Panel
    ax_right.set_xscale("log")
    ax_right.set_yscale("log")
    ax_right.set_xticks(n_list)
    ax_right.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax_right.set_xlabel("System Size $n$")
    ax_right.set_ylabel("Transition Width $w$ (Dimensionless)")
    ax_right.set_title("Transition Width $w$ vs. System Size $n$ (Log-Log Scale)\n(Finite-Size Scaling)")
    ax_right.legend(loc="lower left")
    ax_right.grid(True, which="both")
    
    # Apply watermark "Preliminary, pending advisor alignment"
    for ax in [ax_left, ax_right]:
        ax.text(
            0.5, 0.5, "Preliminary,\npending advisor alignment",
            transform=ax.transAxes,
            fontsize=18, color="red", alpha=0.15,
            ha="center", va="center", rotation=30
        )
        
    # Save figure
    figures_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    fig_path = os.path.join(figures_dir, "finite_size_scaling_r2.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"\nSaved finite-size scaling plot to: {fig_path}")

if __name__ == "__main__":
    main()
