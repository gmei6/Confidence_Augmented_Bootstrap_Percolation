"""Q3: finite-size transition-width figure (r=2, seven sizes, mu = 0 vs 0.3).

Regenerates `results/figures/q3_nu_transition_width.png` from the committed fit
`results/processed/task_a_nu_n10000.json`. This is a presentation figure only --
it runs no simulation and reads no raw file, so it is deterministic given that
committed input.

The figure deliberately carries two panels:

  * LEFT  -- the log-log scaling w ~ n^(-1/nu) with both fitted power laws. On
    its own this panel is close to unreadable: the two fits nearly overlap, and
    the only visible signal is nu in the legend.
  * RIGHT -- the ratio w(mu=0.3) / w(mu=0). This is the panel that makes the
    actual claim legible. nu is a statement about the SLOPE (how fast the window
    narrows as n grows), not about the width at any single n. The ratio crosses
    1 and comes back above it at n=20000, so at a fixed n the sign of the effect
    is not even stable -- at n=1000 fear makes the window 16% WIDER. Showing the
    left panel alone invites the reader to conclude "fear narrows the window",
    which the data does not support.

nu is inverted: a SMALLER nu means FASTER narrowing. It is fitted against node
count n, so it is not a lattice correlation-length exponent.

Usage (from the repository root):

    python scripts/plot_q3_nu_transition_width.py
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

FIT_PATH = os.path.join(base_dir, "results", "processed", "task_a_nu_n10000.json")
OUT_PATH = os.path.join(base_dir, "results", "figures", "q3_nu_transition_width.png")

# Series colours. The site's own teal falls below the perceptual chroma floor at
# chart scale (it reads grey), so the cool slot uses a validated blue instead;
# the warm slot is the site accent unchanged. The pair clears the colour-vision
# separation check with a wide margin (protan dE 24.7 against a >= 8 target).
COOL = "#2a78d6"   # mu = 0    (no fear)
WARM = "#bd5a2e"   # mu = 0.3  (with fear)
INK = "#1e2530"
SOFT = "#5b6672"
PAPER = "#f6f3ea"
GRID = "#d7d1c2"

XTICK_LABELS = ["1k", "2k", "5k", "10k", "20k", "40k", "80k"]


def load_fit():
    if not os.path.exists(FIT_PATH):
        print(f"Error: committed fit not found at {FIT_PATH}")
        sys.exit(1)
    with open(FIT_PATH) as f:
        return json.load(f)


def main():
    data = load_fit()
    widths, fits = data["widths_by_mu"], data["exponent_fits_by_mu"]

    n = np.array([x["n"] for x in widths["0.0"]], dtype=float)
    if not np.array_equal(n, np.array([x["n"] for x in widths["0.3"]], dtype=float)):
        print("Error: the mu=0 and mu=0.3 series are on different n grids")
        sys.exit(1)
    if len(n) != len(XTICK_LABELS):
        print(f"Error: expected {len(XTICK_LABELS)} sizes, found {len(n)}")
        sys.exit(1)

    w0 = np.array([x["width"] for x in widths["0.0"]])
    e0 = np.array([x["width_err"] for x in widths["0.0"]])
    w3 = np.array([x["width"] for x in widths["0.3"]])
    e3 = np.array([x["width_err"] for x in widths["0.3"]])

    nu0, nu0_err = fits["0.0"]["nu"], fits["0.0"]["nu_err"]
    nu3, nu3_err = fits["0.3"]["nu"], fits["0.3"]["nu_err"]

    grid = np.logspace(np.log10(n.min() * 0.85), np.log10(n.max() * 1.18), 200)

    def fitline(key):
        f = fits[key]
        # The committed fit is ln w = intercept + slope * ln n, with slope = -1/nu.
        return np.exp(f["intercept"]) * grid ** f["slope"]

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

    fig, (ax_left, ax_right) = plt.subplots(
        1, 2, figsize=(11.4, 4.7),
        gridspec_kw={"width_ratios": [1.22, 1.0], "wspace": 0.26})

    for ax in (ax_left, ax_right):
        ax.set_xscale("log")
        ax.grid(True, which="major", color=GRID, lw=0.7, alpha=0.9)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_xticks(n)
        ax.set_xticklabels(XTICK_LABELS)
        ax.set_xlim(grid.min(), grid.max())
        ax.set_xlabel("network size $n$  (log scale)", color=SOFT)

    # ------------------------------------------------------------ left panel
    ax_left.set_yscale("log")
    ax_left.plot(grid, fitline("0.0"), color=COOL, lw=1.6, alpha=0.55, zorder=2)
    ax_left.plot(grid, fitline("0.3"), color=WARM, lw=1.6, alpha=0.55, zorder=2)
    ax_left.errorbar(n, w0, yerr=e0, fmt="o", ms=6.5, color=COOL, mec=PAPER, mew=1.4,
                     ecolor=COOL, elinewidth=1.3, capsize=3, zorder=4,
                     label=f"no fear  (μ = 0)      ν = {nu0:.2f} ± {nu0_err:.2f}")
    ax_left.errorbar(n, w3, yerr=e3, fmt="s", ms=6.2, color=WARM, mec=PAPER, mew=1.4,
                     ecolor=WARM, elinewidth=1.3, capsize=3, zorder=4,
                     label=f"with fear  (μ = 0.3)   ν = {nu3:.2f} ± {nu3_err:.2f}")

    ax_left.set_ylabel("transition window width  $w$", color=INK)
    ax_left.set_ylim(0.31, 1.12)
    ax_left.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    ax_left.set_yticklabels(["0.4", "0.5", "0.6", "0.7", "0.8", "0.9"])
    ax_left.yaxis.set_minor_formatter(NullFormatter())
    ax_left.set_title("The window narrows as the network grows —\n"
                      "and slightly faster when there is fear",
                      fontsize=11.5, color=INK, loc="left", pad=10)
    ax_left.legend(frameon=False, loc="upper right", fontsize=9.6, labelcolor=INK,
                   handletextpad=0.6, borderaxespad=0.2)

    # ----------------------------------------------------------- right panel
    ratio = w3 / w0
    ratio_err = ratio * np.hypot(e3 / w3, e0 / w0)

    ax_right.axhspan(1.0, 1.28, color=WARM, alpha=0.07, zorder=0)
    ax_right.axhspan(0.72, 1.0, color=COOL, alpha=0.07, zorder=0)
    ax_right.axhline(1.0, color=SOFT, lw=1.2, ls=(0, (5, 3)), zorder=1)
    ax_right.errorbar(n, ratio, yerr=ratio_err, fmt="o-", ms=6.5, lw=1.5, color=INK,
                      mfc=INK, mec=PAPER, mew=1.4, ecolor=SOFT, elinewidth=1.2,
                      capsize=3, zorder=4)

    ax_right.text(78000, 1.225, "fear makes the window WIDER", color=WARM,
                  fontsize=9.8, fontweight="bold", va="center", ha="right")
    ax_right.text(1060, 0.775, "fear makes the window NARROWER", color=COOL,
                  fontsize=9.8, fontweight="bold", va="center", ha="left")
    ax_right.annotate("+16%", xy=(n[0], ratio[0]), xytext=(1180, 1.192),
                      color=SOFT, fontsize=9.2, ha="left", va="center")
    ax_right.annotate("back above 1", xy=(n[4], ratio[4]), xytext=(22500, 1.085),
                      color=SOFT, fontsize=9.2, ha="left", va="center")

    ax_right.set_ylim(0.72, 1.28)
    ax_right.set_ylabel("width ratio   $w(μ{=}0.3)\\ /\\ w(μ{=}0)$", color=INK)
    ax_right.set_title("At any single size the sign is not stable —\n"
                       "only the downward trend is",
                       fontsize=11.5, color=INK, loc="left", pad=10)

    # ----------------------------------------------------------------- chrome
    fig.suptitle("Fear makes the tipping window narrow FASTER as the network grows",
                 fontsize=13.2, color=INK, x=0.008, ha="left", y=0.985, fontweight="bold")
    fig.text(0.008, 0.905,
             "The effect is in the RATE of narrowing, not the width at any one size.",
             fontsize=10.6, color=SOFT, ha="left", va="center")
    fig.text(0.008, 0.012,
             "ν is inverted: a smaller ν means faster narrowing. ν is fitted "
             "against node count n, so it is not a lattice correlation-length exponent.\n"
             "Source: results/processed/task_a_nu_n10000.json (7 sizes, C++ engine, 500 "
             "bootstrap reps). Error bars are 1σ on the fitted width.",
             fontsize=8.6, color=SOFT, ha="left", va="bottom")

    fig.subplots_adjust(top=0.775, bottom=0.20, left=0.062, right=0.988)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=170)
    plt.close(fig)

    print(f"Wrote {OUT_PATH}")
    print(f"  nu(mu=0)   = {nu0:.3f} +- {nu0_err:.3f}")
    print(f"  nu(mu=0.3) = {nu3:.3f} +- {nu3_err:.3f}")
    print("  width ratio w(0.3)/w(0) by n: "
          + ", ".join(f"{int(a)}:{b:.3f}" for a, b in zip(n, ratio)))


if __name__ == "__main__":
    main()
