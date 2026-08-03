"""Finite-size scaling figure for the poster's "Sharper Transition" panel.

Reads results/processed/task_a_nu_n10000.json (written by scripts/analyze_q3_nu.py,
Task W's 7-point n in [1e3, 8e4] fit) and renders
results/figures/finite_size_scaling_r2_n10000.png. Read-only on the processed
artifact -- never writes or overwrites a results JSON (precedent:
scripts/plot_q4_mumap.py).

This is a standalone replacement for the plotting half of analyze_q3_nu.py,
which conflates analysis (recomputing bootstrap widths + writing the JSON) and
plotting (drawing the PNG, with a "Preliminary" watermark) in one file. Kept
as a separate script rather than overwriting scripts/plot_finite_size_scaling.py,
which is a DIFFERENT, older Task A 3-point script (n in {1000,2000,5000}, output
finite_size_scaling_r2.png with no _n10000 suffix) still cited by
docs/queue/reports/task_a_report.md -- overwriting it would break that citation.

2026-08-03 poster-defect fixes vs. the analyze_q3_nu.py rendering:
  - No "Preliminary, pending advisor alignment" watermark (cannot print red text
    over data on a poster).
  - Log-x ticks relabeled to short "1k".."80k" strings (the raw 5-digit
    ScalarFormatter labels ran into each other at this many ticks).
  - Family + engine stated explicitly in the title (Erdos-Renyi / G(n,p), C++).
  - The two power-law fits are extended across the full x-range and their
    crossing (~n=9,400, right at the poster's "near n~1e4" claim) is marked
    with an explicit vertical guide + annotation, instead of a reader having to
    notice two lines happen to touch.
"""

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANALYSIS_PATH = os.path.join(base_dir, "results/processed/task_a_nu_n10000.json")
FIG_PATH = os.path.join(base_dir, "results/figures/finite_size_scaling_r2_n10000.png")

# Okabe-Ito blue / orange: colorblind-safe pair, consistent with the project's
# other figures (e.g. scripts/plot_q4_mumap.py's SERIES blue).
COLOR_MU0 = "#0072B2"
COLOR_MU03 = "#E69F00"


def format_n(n: int) -> str:
    """1000 -> '1k', 10000 -> '10k', etc. Short labels so 7 log-x ticks don't
    run into each other (the defect this replaces: 5-digit ScalarFormatter
    labels like '10000' next to '20000' read as one smashed-together string)."""
    if n % 1000 == 0:
        return f"{n // 1000}k"
    return str(n)


def main() -> None:
    with open(ANALYSIS_PATH) as f:
        d = json.load(f)

    meta = d["metadata"]
    n_list = meta["n_list"]
    mu_list = meta["mu_list"]
    widths_by_mu = d["widths_by_mu"]
    fits_by_mu = d["exponent_fits_by_mu"]

    colors = {0.0: COLOR_MU0, 0.3: COLOR_MU03}

    fig, ax = plt.subplots(figsize=(7.2, 6.2), dpi=300)

    n_fit = np.linspace(min(n_list) * 0.8, max(n_list) * 1.2, 200)
    fit_lines = {}
    for mu in mu_list:
        rows = widths_by_mu[str(mu)]
        fit = fits_by_mu[str(mu)]
        ns = [r["n"] for r in rows]
        ws = [r["width"] for r in rows]
        werr = [r["width_err"] for r in rows]

        ax.errorbar(
            ns, ws, yerr=werr, fmt="o", color=colors[mu], capsize=4,
            markersize=6, elinewidth=1.3, label=rf"Data $\mu={mu:g}$", zorder=3,
        )
        w_fit = np.exp(fit["slope"] * np.log(n_fit) + fit["intercept"])
        fit_lines[mu] = (fit["slope"], fit["intercept"])
        ax.plot(
            n_fit, w_fit, color=colors[mu], linewidth=2.0, zorder=2,
            label=rf"Fit $\mu={mu:g}$ ($\nu={fit['nu']:.2f} \pm {fit['nu_err']:.2f}$)",
        )

    # Honest crossing marker: solve the two log-log fit lines for the n where
    # they're equal, rather than leaving it for a reader to notice the lines
    # touch. slope*ln(n)+intercept is the same functional form both fits use.
    (slope0, intercept0), (slope3, intercept3) = fit_lines[0.0], fit_lines[0.3]
    ln_n_cross = (intercept3 - intercept0) / (slope0 - slope3)
    n_cross = float(np.exp(ln_n_cross))
    w_cross = float(np.exp(slope0 * ln_n_cross + intercept0))
    ax.axvline(n_cross, color="#888888", linestyle=":", linewidth=1.3, zorder=1)
    ax.annotate(
        f"fits cross\n$n \\approx {n_cross:,.0f}$",
        xy=(n_cross, w_cross), xytext=(n_cross * 1.35, w_cross * 1.12),
        fontsize=9, color="#555555", ha="left", va="bottom",
        arrowprops=dict(arrowstyle="-", color="#888888", lw=1.0),
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(n_list)
    ax.set_xticklabels([format_n(n) for n in n_list])
    ax.minorticks_off()
    ax.set_xlabel("System size $n$", fontsize=12, fontweight="bold", labelpad=8)
    ax.set_ylabel("Transition width $w$", fontsize=12, fontweight="bold", labelpad=8)
    # Plain unicode, not the LaTeX \H{o}/\'e accent commands: this script runs
    # with matplotlib's default mathtext renderer (no local LaTeX install, and
    # a plotting script shouldn't require one), which renders \H{o} literally
    # instead of expanding it -- caught by eyeballing the actual PNG.
    ax.set_title(
        "Finite-Size Scaling of the Transition Width\n"
        r"Erdős–Rényi / $G(n,p)$, C++ engine $-$ $w \sim n^{-1/\nu}$",
        fontsize=12, fontweight="bold", pad=12,
    )
    ax.grid(True, which="major", alpha=0.3, linestyle="--")
    ax.legend(loc="lower left", fontsize=10, frameon=True)

    fig.text(
        0.5, -0.02,
        rf"Source: {os.path.relpath(ANALYSIS_PATH, base_dir)} "
        rf"(commit {meta['analysis_runtime_commit'][:7]}); "
        rf"{meta['bootstrap_reps']}-rep bootstrap, seed {meta['bootstrap_seed']}. "
        rf"$\theta={meta['theta']}$; $n \in [{min(n_list):,}, {max(n_list):,}]$.",
        ha="center", fontsize=8, color="#666666",
    )

    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {FIG_PATH}")


if __name__ == "__main__":
    main()
