"""Q4 / Task X: the size-biased collapse test, C-Q4(ii), shown as a figure.

Regenerates `results/figures/q4_size_biased_collapse.png` from the committed
analysis `results/processed/q4_size_biased_collapse_analysis.json`. Runs no
simulation, so it is deterministic given that committed input.

What the figure is for
----------------------
Conjecture C-Q4 clause (ii) (`docs/research/q4_config_model_scoping.md` §5)
predicts that the critical seed collapses onto ONE curve when plotted against
the size-biased mean fear mu* rather than the plain mean mu-bar. mu* is not an
arbitrary rescaling: under the edge map on the configuration model's local-tree
limit (size-biased offspring; vdH Vol. II), the fear term carries
E_q[mu(D*)] = mu*, so mu* is the quantity the analytics force.

The two panels are the test. LEFT is the boundary against mu-bar; RIGHT is the
same boundary against mu*. Collapse would mean the right panel shows one curve.
Instead the spread roughly doubles (1.51 -> 3.11) and, inside the only mu* window
where all three tilts exist, the ordering INVERTS. That refutes clause (ii).

Honesty note carried on the figure: the three tilt slices barely overlap in the
mu* they realize, so the comparison happens in a narrow band and the MAGNITUDE
of the effect is grid-limited. The SIGN -- mu* makes the spread worse, not
better -- is the robust part.

Usage (from the repository root):

    python scripts/plot_q4_size_biased_collapse.py
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

ANALYSIS_PATH = os.path.join(base_dir, "results", "processed",
                             "q4_size_biased_collapse_analysis.json")
OUT_PATH = os.path.join(base_dir, "results", "figures", "q4_size_biased_collapse.png")

# gamma is SIGNED with a natural neutral at 0, so this is a diverging encoding:
# two poles plus a neutral grey midpoint, never three categorical hues (three
# hues cannot be separated under deuteranopia at these lightnesses). Marker
# shape is a second, redundant channel and points the way the tilt points.
STYLE = {
    -1.0: dict(color="#2a78d6", marker="v", label="γ = −1   panic on low-degree banks"),
    0.0: dict(color="#5b6672", marker="o", label="γ = 0    panic spread evenly"),
    1.0: dict(color="#bd5a2e", marker="^", label="γ = +1   panic on hubs"),
}
INK = "#1e2530"
SOFT = "#5b6672"
PAPER = "#f6f3ea"
GRID = "#d7d1c2"


def load_analysis():
    if not os.path.exists(ANALYSIS_PATH):
        print(f"Error: committed analysis not found at {ANALYSIS_PATH}")
        sys.exit(1)
    with open(ANALYSIS_PATH) as f:
        return json.load(f)


def main():
    data = load_analysis()
    points, collapse = data["points_by_gamma"], data["collapse"]

    series = {}
    for key, style in STYLE.items():
        raw = points.get(str(key))
        if raw is None:
            print(f"Error: gamma={key} missing from the committed analysis")
            sys.exit(1)
        rows = [p for p in raw if p.get("resolved")]
        series[key] = (
            np.array([p["mu_bar"] for p in rows]),
            np.array([p["mu_star"] for p in rows]),
            np.array([p["a_c_emp"] for p in rows]),
        )

    # The mu* window where all three tilts actually have data. Outside it the
    # "matched mu*" comparison is an extrapolation, so we shade it explicitly.
    lo = max(s[1].min() for s in series.values())
    hi = min(s[1].max() for s in series.values())

    plt.rcParams.update({
        "font.size": 10.5,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": SOFT,
        "ytick.color": SOFT,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
    })

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11.4, 5.1), sharey=True,
                                            gridspec_kw={"wspace": 0.09})

    for ax in (ax_left, ax_right):
        ax.grid(True, color=GRID, lw=0.7, alpha=0.9)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    for key, style in STYLE.items():
        mu_bar, mu_star, a_c = series[key]
        common = dict(color=style["color"], marker=style["marker"], ms=7,
                      lw=1.8, mec=PAPER, mew=1.2)
        ax_left.plot(mu_bar, a_c, label=style["label"], **common)
        ax_right.plot(mu_star, a_c, **common)

    ax_left.set_xlabel("plain average panic  μ̄", color=INK)
    ax_left.set_ylabel("critical seed  $a_c^{\\mathrm{emp}}$", color=INK)
    ax_left.set_title("What we plot it against now: μ̄\n"
                      "three separated curves, cleanly ordered",
                      fontsize=11.5, color=INK, loc="left", pad=10)
    ax_left.legend(frameon=False, loc="upper right", fontsize=9.4, labelcolor=INK,
                   handletextpad=0.6, borderaxespad=0.2)

    ax_right.axvspan(lo, hi, color=SOFT, alpha=0.10, zorder=0)
    ax_right.set_xlabel("size-biased panic  μ*   (what the edge map carries)", color=INK)
    ax_right.set_title("What C-Q4(ii) said to plot it against: μ*\n"
                       "prediction was ONE curve — instead they spread and invert",
                       fontsize=11.5, color=INK, loc="left", pad=10)
    ax_right.set_ylim(2.85, 11.0)
    ax_right.annotate(f"the only μ* window where\nall three tilts have data\n({lo:.2f}–{hi:.2f})",
                      xy=((lo + hi) / 2, 2.95), color=SOFT, fontsize=9,
                      ha="center", va="bottom")

    # The ordering flip, called out on both panels at a matched location.
    ax_left.annotate("at μ̄ = 0.4:\nhub-tilt is LOWEST", xy=(0.4, 5.41), xytext=(0.115, 3.55),
                     color=SOFT, fontsize=9, ha="left",
                     arrowprops=dict(arrowstyle="->", color=SOFT, lw=0.9,
                                     connectionstyle="arc3,rad=-0.15"))
    ax_right.annotate("at matched μ* ≈ 0.30:\nhub-tilt is HIGHEST", xy=(0.301, 8.95),
                      xytext=(0.50, 10.2), color=SOFT, fontsize=9, ha="left",
                      arrowprops=dict(arrowstyle="->", color=SOFT, lw=0.9))

    fig.suptitle("Matching on size-biased panic was supposed to collapse these onto one curve",
                 fontsize=13.2, color=INK, x=0.008, ha="left", y=0.985, fontweight="bold")
    fig.text(0.008, 0.905,
             f"It does the opposite: the spread between tilts roughly doubles "
             f"({collapse['matched_mu_bar_spread_mean']:.2f} → "
             f"{collapse['matched_mu_star_spread_mean']:.2f}, ratio "
             f"{collapse['spread_ratio_mustar_over_mubar']:.2f}), and the ordering inverts.",
             fontsize=10.6, color=SOFT, ha="left", va="center")
    fig.text(0.008, 0.012,
             "Collapse would have required the spread ratio to fall below 1. The SIGN is robust; the "
             "MAGNITUDE is grid-limited — the three tilt slices\nbarely overlap in realized μ*, so "
             "the matched comparison happens only inside the shaded band.\n"
             "Config model, τ=2.5, n=10000, cap-fixed sampler. "
             "Source: results/processed/q4_size_biased_collapse_analysis.json.",
             fontsize=8.6, color=SOFT, ha="left", va="bottom")

    fig.subplots_adjust(top=0.775, bottom=0.235, left=0.062, right=0.988)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=170)
    plt.close(fig)

    print(f"Wrote {OUT_PATH}")
    print(f"  matched-μ̄ spread   = {collapse['matched_mu_bar_spread_mean']:.4f}")
    print(f"  matched-μ* spread   = {collapse['matched_mu_star_spread_mean']:.4f}")
    print(f"  spread ratio        = {collapse['spread_ratio_mustar_over_mubar']:.4f} "
          f"(collapse_supported={collapse['collapse_supported']})")
    print(f"  μ* overlap window   = {lo:.4f} – {hi:.4f}")


if __name__ == "__main__":
    main()
