"""
Q3 nu tightening (Task A machinery + n = 10000, 20000 C++ points).

Recomputes the finite-size transition-width exponent nu with the
results/raw/finite_size_r2_n10000.json (S-047) and
results/raw/finite_size_r2_n20000.json (S-051) points added to the Task A
n-grid {1000, 2000, 5000}. Uses the same machinery as
scripts/plot_finite_size_scaling.py: estimate_transition_width (logistic
10-90% width, 500 bootstrap reps) and fit_finite_size_exponent
(log w ~ -(1/nu) log n).

Writes results/processed/task_a_nu_n10000.json and
results/figures/finite_size_scaling_r2_n10000.png. (Output filenames are
kept as-is for continuity with the existing S-047 artifact lineage even
though the n-grid now extends to 20000 -- see metadata.n_list for the
actual grid used.)
"""

import os
import sys
import json
import math
import datetime

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash
from twocascade.analysis import (
    load_raw_results,
    estimate_transition_width,
    fit_finite_size_exponent,
)
from twocascade.plotting import apply_plot_style

N_LIST = [1000, 2000, 5000, 10000, 20000]
MU_LIST = [0.0, 0.3]
THETA = 0.5
BOOTSTRAP_SEED = 20260629  # same as scripts/plot_finite_size_scaling.py
OUTPUT_PATH = "results/processed/task_a_nu_n10000.json"
FIGURE_NAME = "finite_size_scaling_r2_n10000.png"

# Task A three-point fit (docs/queue/reports/task_a_report.md, S-036) for
# comparison in the output artifact.
PRIOR_FIT = {
    "0.0": {"nu": 8.39, "nu_err": 1.57, "n_list": [1000, 2000, 5000]},
    "0.3": {"nu": 5.33, "nu_err": 0.51, "n_list": [1000, 2000, 5000]},
}


def failed_fractions_by_multiple(raw_data, mu_target):
    out = {}
    for cell in raw_data["results"]:
        if math.isclose(float(cell["mean_fear"]), mu_target, abs_tol=1e-9):
            out[float(cell["seed_multiple"])] = cell["failed_fractions"]
    return out


def main():
    apply_plot_style()

    raws = {}
    source_commits = {}
    for n in N_LIST:
        rel = f"results/raw/finite_size_r2_n{n}.json"
        raws[n] = load_raw_results(os.path.join(base_dir, rel))
        source_commits[rel] = raws[n]["metadata"]["git_commit"]
    seed_multiples = raws[N_LIST[0]]["sweep_parameters"]["seed_multiples"]

    widths = {}
    fits = {}
    for mu in MU_LIST:
        rows = []
        for n in N_LIST:
            res = estimate_transition_width(
                failed_fractions_by_multiple=failed_fractions_by_multiple(raws[n], mu),
                theta=THETA,
                seed_multiples=seed_multiples,
                bootstrap_reps=500,
                seed=BOOTSTRAP_SEED,
            )
            rows.append({
                "n": n,
                "width": res["width"],
                "width_err": res["width_err"],
                "ci_95": list(res["ci"]),
                "k": res["k"],
                "x0": res["x0"],
            })
            print(f"mu={mu} n={n}: w={res['width']:.4f} +/- {res['width_err']:.4f}")
        widths[str(mu)] = rows

        fit = fit_finite_size_exponent(
            [r["n"] for r in rows],
            [r["width"] for r in rows],
            [r["width_err"] for r in rows],
        )
        fits[str(mu)] = {
            "nu": fit["nu"], "nu_err": fit["nu_err"],
            "slope": fit["slope"], "intercept": fit["intercept"],
            "r_squared": fit["r_squared"],
            "n_list": N_LIST,
            "prior_three_point_fit": PRIOR_FIT[str(mu)],
        }
        print(f"mu={mu}: nu={fit['nu']:.3f} +/- {fit['nu_err']:.3f} "
              f"(R2={fit['r_squared']:.4f}); prior 3-pt nu="
              f"{PRIOR_FIT[str(mu)]['nu']} +/- {PRIOR_FIT[str(mu)]['nu_err']}")

    # Figure: log-log widths + fits, four-point version of the Task A panel.
    fig, ax = plt.subplots(figsize=(7, 6))
    colors = {0.0: "blue", 0.3: "orange"}
    for mu in MU_LIST:
        rows = widths[str(mu)]
        f = fits[str(mu)]
        ax.errorbar([r["n"] for r in rows], [r["width"] for r in rows],
                    yerr=[r["width_err"] for r in rows],
                    fmt="o", color=colors[mu], capsize=4, label=f"Data $\\mu={mu}$")
        n_fit = np.linspace(800, 24000, 100)
        ax.loglog(n_fit, np.exp(f["slope"] * np.log(n_fit) + f["intercept"]),
                  color=colors[mu],
                  label=f"Fit $\\mu={mu}$ ($\\nu={f['nu']:.2f} \\pm {f['nu_err']:.2f}$)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(N_LIST)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_xlabel("System Size $n$")
    ax.set_ylabel("Transition Width $w$")
    ax.set_title("Finite-Size Scaling, $n \\in [1000, 20000]$ (C++ engine)\n"
                 "$w \\sim n^{-1/\\nu}$")
    ax.legend(loc="lower left")
    ax.grid(True, which="both")
    ax.text(0.5, 0.5, "Preliminary,\npending advisor alignment",
            transform=ax.transAxes, fontsize=18, color="red", alpha=0.15,
            ha="center", va="center", rotation=30)
    figures_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    fig_path = os.path.join(figures_dir, FIGURE_NAME)
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {fig_path}")

    out = {
        "metadata": {
            "task": "A extension (Q3 nu tightening with n = 10000, C++ engine)",
            "n_list": N_LIST,
            "mu_list": MU_LIST,
            "theta": THETA,
            "bootstrap_reps": 500,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "source_commits": source_commits,
            "analysis_runtime_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "figure": f"results/figures/{FIGURE_NAME}",
        },
        "widths_by_mu": widths,
        "exponent_fits_by_mu": fits,
    }
    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
