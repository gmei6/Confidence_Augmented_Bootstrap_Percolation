"""
Task N (Q4 Phase 1b) figure: C-Q4(i) tilt monotonicity on the configuration model.

Reads results/processed/task_n_tilt_analysis.json (written by analyze_task_n.py)
and renders results/figures/q4_tilt_monotonicity_r2.png. Strictly read-only on
analysis artifacts (provenance rule: plotting never writes analysis JSONs).

Panel A: empirical critical seed a_c^emp vs mean fear, one curve per tilt gamma.
Panel B: realized population mean fear vs nominal (the epsilon-cap diagnostic
         explaining why the gamma=+1 curve is artifact-suspect at high mu-bar).
"""

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ANALYSIS_PATH = os.path.join(base_dir, "results/processed/task_n_tilt_analysis.json")
FIG_PATH = os.path.join(base_dir, "results/figures/q4_tilt_monotonicity_r2.png")

# Okabe-Ito CVD-safe trio, fixed order by gamma; validated (light surface).
COLORS = {"-1.0": "#0072B2", "0.0": "#E69F00", "1.0": "#009E73"}
MARKERS = {"-1.0": "o", "0.0": "s", "1.0": "^"}
LABELS = {"-1.0": r"$\gamma=-1$ (hubs calmer)",
          "0.0": r"$\gamma=0$ (flat)",
          "1.0": r"$\gamma=+1$ (hubs more fearful)"}


def main():
    with open(ANALYSIS_PATH) as f:
        d = json.load(f)

    meta = d["metadata"]
    gammas = [str(g) for g in meta["gammas"]]
    mu_grid = [m for m in d["sweep_parameters"]["mean_fear_grid"] if m > 0.0]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11, 4.4))

    # --- Panel A: a_c^emp(mu-bar) per gamma ---
    for g in gammas:
        thr = d["empirical_thresholds_by_gamma"][g]
        xs, ys = [], []
        for mu in mu_grid:
            t = thr[str(float(mu))]
            if t["resolved"]:
                xs.append(mu)
                ys.append(t["a_emp"])
        # gamma=+1 is cap-affected at every mu-bar on this grid: draw dashed.
        cap_affected = all(
            not row["cap_free"]
            for row in d["verdict"]["pair_verdicts"].get(f"{float(g)}_vs_0.0", {}).get("rows", [])
        ) if g == "1.0" else False
        ax_a.plot(xs, ys, linestyle="--" if cap_affected else "-",
                  marker=MARKERS[g], markersize=5, linewidth=2,
                  color=COLORS[g], label=LABELS[g])
        gtxt = {"-1.0": "-1", "0.0": "0", "1.0": "+1"}[g]
        ax_a.annotate(rf"$\gamma={gtxt}$", (xs[-1], ys[-1]),
                      textcoords="offset points", xytext=(6, -2),
                      color=COLORS[g], fontsize=9)

    ax_a.set_xlabel(r"nominal mean fear $\bar\mu$")
    ax_a.set_ylabel(r"empirical critical seed $a_c^{\mathrm{emp}}$")
    ax_a.set_title(r"C-Q4(i): boundary vs tilt ($\tau=2.5$, $n=4000$, $r=2$)",
                   fontsize=10)
    ax_a.grid(alpha=0.25, linewidth=0.5)
    ax_a.legend(fontsize=8, frameon=False)

    # --- Panel B: realized mu-bar vs nominal (cap diagnostic) ---
    diag = d["cap_diagnostics"]["per_mu_gamma"]
    mus = sorted(float(m) for m in diag if float(m) > 0.0)
    ax_b.plot([0, 0.75], [0, 0.75], color="#999999", linewidth=1,
              linestyle=":", label="no cap (identity)")
    for g in gammas:
        ys = [diag[str(m)][g]["realized_mu_bar"] for m in mus]
        # gamma=-1 and gamma=0 both sit exactly on the identity: draw gamma=-1
        # as a larger open marker so it stays visible under the gamma=0 curve.
        if g == "-1.0":
            ax_b.plot(mus, ys, marker=MARKERS[g], markersize=11, linewidth=0,
                      markerfacecolor="none", markeredgewidth=1.6,
                      color=COLORS[g], label=LABELS[g])
        else:
            ax_b.plot(mus, ys, marker=MARKERS[g], markersize=5, linewidth=2,
                      color=COLORS[g], label=LABELS[g])
    ax_b.set_xlabel(r"nominal mean fear $\bar\mu$")
    ax_b.set_ylabel(r"realized population mean fear")
    ax_b.set_title(r"$\varepsilon$-cap compression (equal-total-fear check)",
                   fontsize=10)
    ax_b.grid(alpha=0.25, linewidth=0.5)
    ax_b.legend(fontsize=8, frameon=False)

    fig.suptitle(
        "Q4 configuration model: tilt monotonicity holds on the cap-free pair "
        r"($\gamma=-1\to0$: 7/7 rows); $\gamma=+1$ artifact-suspect (cap)",
        fontsize=11)
    fig.text(0.5, 0.005,
             f"Preliminary, pending advisor alignment - "
             f"sources: {', '.join(meta['source_raw_files'])} - "
             f"base_seed={meta['base_seed']}, trials/cell={meta['trials_per_cell']}, "
             f"analysis commit {meta['analysis_runtime_commit'][:10]}",
             ha="center", fontsize=6, color="#777777")

    fig.tight_layout(rect=[0, 0.02, 1, 0.93])
    os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
    fig.savefig(FIG_PATH, dpi=300, bbox_inches="tight")
    print(f"Wrote {os.path.relpath(FIG_PATH, base_dir)}")


if __name__ == "__main__":
    main()
