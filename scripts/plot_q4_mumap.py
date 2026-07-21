"""
Q4 figure: the mu_bar x n ignition map (C-Q4(iii) refinement).

Reads results/processed/q4_mumap_analysis.json (written by analyze_q4_mumap.py)
and renders results/figures/q4_mumap_ignition.png. Read-only on analysis
artifacts -- never writes or overwrites a results JSON.

Small multiples, one panel per mean fear mu_bar. Faceting (not 5 overlaid lines)
is deliberate: 5 single-hue sequential lines fail the normal-vision adjacent-pair
separation floor, so identity is carried by POSITION and color is freed to mean
one thing -- blue = this panel's series, gray = the mu=0 control repeated in every
panel as a fixed reference.

The two readouts it carries:
  (a) P(systemic) is monotone increasing in mu_bar at every n -- each panel sits
      progressively higher above the shared gray control.
  (b) P(systemic) DECLINES with n at every mu_bar INCLUDING mu=0 -- every panel
      slopes down, so the decline is not fear-specific. Fear multiplies the
      ignition rate (per-panel ratio annotated: ~3x at mu_bar=0.4, progressively
      less below it) and that multiplier is stable in n, so fear raises the rate
      without changing how it scales with n. Note the multiplier is constant in
      n at fixed mu_bar, NOT constant across mu_bar.
"""

import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANALYSIS_PATH = os.path.join(base_dir, "results/processed/q4_mumap_analysis.json")
FIG_PATH = os.path.join(base_dir, "results/figures/q4_mumap_ignition.png")

# House Okabe-Ito blue for the series; neutral gray for the control reference.
# The gray is intentionally achromatic -- it is a reference, not a category.
SERIES = "#0072B2"
CONTROL = "#767676"


def cochran_armitage(counts, trials, scores):
    """Trend test of P(systemic) against log(n). Negative z = declining in n.
    Ordered alternative -- more powered here than an omnibus homogeneity chi2
    (project convention, cf. scripts/analyze_q4_ignition.py)."""
    tot, ntot = sum(counts), sum(trials)
    pbar = tot / ntot
    num = sum(t * (x - N * pbar) for t, x, N in zip(scores, counts, trials))
    var = pbar * (1 - pbar) * (
        sum(N * t * t for N, t in zip(trials, scores))
        - sum(N * t for N, t in zip(trials, scores)) ** 2 / ntot
    )
    z = num / math.sqrt(var)
    return z, math.erfc(abs(z) / math.sqrt(2))


def main():
    with open(ANALYSIS_PATH) as f:
        d = json.load(f)
    meta = d["metadata"]
    ns = meta["n_grid"]
    mus = meta["mu_grid"]
    cells = {(c["n"], c["mean_fear"]): c for c in d["cells"]}

    ctrl_p = [cells[(n, 0.0)]["p_systemic"] for n in ns]
    ctrl_k = sum(cells[(n, 0.0)]["n_systemic"] for n in ns)

    fig, axes = plt.subplots(
        1, len(mus), figsize=(13.0, 3.5), sharey=True, sharex=True
    )

    for ax, mu in zip(axes, mus):
        cell = [cells[(n, mu)] for n in ns]
        p = [c["p_systemic"] for c in cell]
        k = [c["n_systemic"] for c in cell]
        trials = [c["n_trials"] for c in cell]
        lo = [c["p_systemic"] - c["wilson_95"][0] for c in cell]
        hi = [c["wilson_95"][1] - c["p_systemic"] for c in cell]

        # Shared control reference in every panel.
        ax.plot(ns, ctrl_p, color=CONTROL, lw=1.4, ls="--", zorder=1,
                label=r"$\bar\mu=0$ control")

        ax.errorbar(ns, p, yerr=[lo, hi], color=SERIES, lw=2.0, marker="o",
                    ms=5.5, capsize=2.5, elinewidth=1.2, zorder=3,
                    markeredgecolor="white", markeredgewidth=0.8)

        z, pv = cochran_armitage(k, trials, [math.log(n) for n in ns])
        ratio = (sum(k) / ctrl_k) if ctrl_k else float("nan")

        ax.set_xscale("log")
        ax.set_yscale("log")
        # Explicit limits: log autoscale otherwise expands to decade boundaries
        # and squeezes the 4k-80k data into a corner.
        ax.set_xlim(3000, 110000)
        ax.set_ylim(0.008, 0.20)
        ax.set_xticks([4000, 20000, 80000])
        ax.set_xticklabels(["4k", "20k", "80k"])
        ax.set_yticks([0.01, 0.02, 0.05, 0.10])
        ax.set_yticklabels(["0.01", "0.02", "0.05", "0.10"])
        ax.minorticks_off()

        ax.set_title(rf"$\bar\mu = {mu:g}$", fontsize=11, pad=8)
        ax.grid(True, which="major", alpha=0.18, lw=0.6)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#cccccc")
        ax.tick_params(colors="#555555", labelsize=8.5)

        p_txt = "p < 0.0001" if pv < 1e-4 else f"p = {pv:.4f}"
        tag = "(the control)" if mu == 0.0 else rf"${ratio:.1f}\times$ control"
        ax.annotate(
            f"trend z = {z:+.2f}\n{p_txt}\n{tag}",
            xy=(0.05, 0.05), xycoords="axes fraction", fontsize=8,
            color="#333333", ha="left", va="bottom", linespacing=1.5,
        )

    axes[0].set_ylabel(r"$P(\mathrm{systemic})$", fontsize=10)
    for ax in axes:
        ax.set_xlabel(r"$n$", fontsize=10)

    # One figure-level legend: identity is carried by panel position, so the
    # only thing needing a key is series-vs-control.
    handles, labels = axes[0].get_legend_handles_labels()
    order = [labels.index(l) for l in sorted(set(labels), key=labels.index)]
    fig.legend([handles[i] for i in order], [labels[i] for i in order],
               loc="upper center", bbox_to_anchor=(0.5, 0.99), ncol=2,
               fontsize=8.5, frameon=False)

    fig.suptitle(
        r"Ignition declines with $n$ at every fear level $\bar\mu$ — including $\bar\mu=0$",
        fontsize=12.5, y=1.10, x=0.5,
    )
    # Provenance travels WITH the image: this sweep is an independent replicate
    # of the main tau=2.5 ignition series, and at mu_bar=0.4 its cells differ
    # from that series by sampling variation. Stated here (not only in the page
    # that embeds it) because a figure pasted into a slide or an email arrives
    # with no table beside it, which is exactly where the difference would look
    # like an error instead of a second measurement.
    fig.text(
        0.5, -0.10,
        rf"$\tau=2.5$ configuration model, bounded seed $a=r=2$, "
        rf"{cells[(ns[0], mus[0])]['n_trials']} trials/cell, Wilson 95% intervals.",
        ha="center", fontsize=7.5, color="#666666",
    )
    fig.text(
        0.5, -0.165,
        r"Independent replicate of the $\tau=2.5$ ignition sweep: the $\bar\mu=0$ panel "
        r"matches that series trial-for-trial (same seeds); $\bar\mu=0.4$ draws a separate "
        r"RNG stream and differs by sampling variation ($|z|\leq1.7$, joint $p=0.56$).",
        ha="center", fontsize=7.5, color="#666666",
    )
    fig.text(
        0.5, -0.225,
        rf"Source: {os.path.relpath(ANALYSIS_PATH, base_dir)} "
        rf"(commit {meta['analysis_runtime_commit'][:7]}).",
        ha="center", fontsize=7.5, color="#666666",
    )
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {FIG_PATH}")


if __name__ == "__main__":
    main()
