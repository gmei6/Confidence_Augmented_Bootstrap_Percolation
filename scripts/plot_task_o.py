"""
Task O (Q5) figure: nucleation law and coverage-entropy homogenization.

Reads results/processed/task_o_locality_analysis.json (written by
analyze_task_o.py) and renders results/figures/q5_locality_r2.png.
Read-only on analysis artifacts.

Panel A: global-field E[N_nuc] vs g_t (log-log) per mean fear, with the fitted
         slopes and a slope-2 reference - the C-Q5(i) readout (observed ~1.2-1.5:
         constant leak, not the predicted r=2 barrier).
Panel B: coverage entropy H at the theta-crossing per field and mean fear, with
         the mu=0 control baseline - the C-Q5(iii) homogenization readout.
"""

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANALYSIS_PATH = os.path.join(base_dir, "results/processed/task_o_locality_analysis.json")
FIG_PATH = os.path.join(base_dir, "results/figures/q5_locality_r2.png")

# Okabe-Ito CVD-safe hues (validated for the light surface in plot_task_n.py).
MU_COLORS = {"0.2": "#0072B2", "0.4": "#E69F00", "0.6": "#009E73"}
FIELD_COLORS = {"global": "#0072B2", "local_4": "#E69F00", "local_1": "#009E73"}
FIELD_LABELS = {"global": "global field",
                "local_4": r"local, $\ell = 4 r_n$",
                "local_1": r"local, $\ell = r_n$"}


def main():
    with open(ANALYSIS_PATH) as f:
        d = json.load(f)
    meta = d["metadata"]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11, 4.4))

    # --- Panel A: nucleation law, global field ---
    for mu, cell in sorted(d["nucleation"]["global"].items()):
        curve, fit = cell["curve"], cell["fit"]
        if not curve:
            continue
        x = np.array(curve["g_bin_centers"])
        y = np.array(curve["mean_n_nuc"])
        keep = y > 0
        ax_a.plot(x[keep], y[keep], "o", markersize=5, color=MU_COLORS[mu],
                  label=rf"$\bar\mu={mu}$ (slope {fit['slope']:.2f})" if fit
                  else rf"$\bar\mu={mu}$")
        if fit:
            xs = np.array([x[keep].min(), x[keep].max()])
            ax_a.plot(xs, np.exp(fit["intercept"]) * xs ** fit["slope"],
                      linewidth=1.5, color=MU_COLORS[mu], alpha=0.7)
    # slope-2 reference
    xr = np.array([0.05, 0.45])
    ax_a.plot(xr, 0.4 * (xr / xr[0]) ** 2, linestyle=":", color="#777777",
              linewidth=1.5)
    ax_a.text(xr[1], 0.4 * (xr[1] / xr[0]) ** 2 * 0.55, "slope 2\n(C-Q5(i) prediction)",
              fontsize=8, color="#777777", ha="right", va="top")
    ax_a.set_xscale("log")
    ax_a.set_yscale("log")
    ax_a.set_xlabel(r"cumulative failed fraction $g_t$")
    ax_a.set_ylabel(r"$\mathbb{E}[N_{\mathrm{nuc}}(t)]$ per round")
    ax_a.set_title("C-Q5(i) nucleation law - global field (systemic trials)",
                   fontsize=10)
    ax_a.grid(alpha=0.25, linewidth=0.5, which="both")
    ax_a.legend(fontsize=8, frameon=False, loc="upper left")

    # --- Panel B: H at theta-crossing per field ---
    mus = [m for m in meta["mean_fear_grid"]]
    control = d["mu0_control_entropy"]["mean"]
    for field in ["global", "local_4", "local_1"]:
        ys, errs = [], []
        for mu in mus:
            v = d["entropy_at_theta"][field][str(mu)]
            ys.append(v["mean"] if v else np.nan)
            errs.append(v["se"] if v and v["se"] else 0.0)
        ax_b.errorbar(mus, ys, yerr=errs, marker="o", markersize=5, linewidth=2,
                      capsize=3, color=FIELD_COLORS[field], label=FIELD_LABELS[field])
    ax_b.axhline(control, linestyle=":", color="#777777", linewidth=1.5)
    ax_b.text(0.02, control + 0.006, r"$\mu=0$ control", fontsize=8, color="#777777")
    ax_b.axhline(0.9, linestyle="--", color="#bbbbbb", linewidth=1)
    ax_b.text(0.02, 0.905, "pre-registered global threshold (0.9)", fontsize=7,
              color="#999999")
    ax_b.set_xlabel(r"mean fear $\bar\mu$")
    ax_b.set_ylabel(r"coverage entropy $H$ at $\theta$-crossing")
    ax_b.set_title("C-Q5(iii) homogenization by fear-field range", fontsize=10)
    ax_b.grid(alpha=0.25, linewidth=0.5)
    ax_b.legend(fontsize=8, frameon=False, loc="center left")

    fig.suptitle(
        "Q5 hard RGG, disc seed: global fear homogenizes the cascade; "
        r"$\ell=r_n$ locality is fully preserved; nucleation grows as a "
        "constant leak (slope ~1.2-1.5, not the predicted 2)",
        fontsize=10.5)
    fig.text(0.5, 0.005,
             f"Preliminary, pending advisor alignment - source: {meta['source_raw_file']} - "
             f"n={meta['n']}, r={meta['r']}, base_seed={meta['base_seed']}, "
             f"trials/cell={meta['trials_per_cell']}, "
             f"analysis commit {meta['analysis_runtime_commit'][:10]}",
             ha="center", fontsize=6, color="#777777")

    fig.tight_layout(rect=[0, 0.02, 1, 0.9])
    os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
    fig.savefig(FIG_PATH, dpi=300, bbox_inches="tight")
    print(f"Wrote {os.path.relpath(FIG_PATH, base_dir)}")


if __name__ == "__main__":
    main()
