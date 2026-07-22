"""Q4 / Task N phase 2: critical seed vs degree-tilt, n=10000, cap-fixed sampler.

Regenerates `results/figures/q4_tilt_monotonicity_capfix_n10000.png` from the
committed analysis `results/processed/q4_size_biased_collapse_analysis.json`,
whose points come from the three cap-fixed raws
`results/q4_phase2_n10000_gamma{neg1,0,pos1}_capfix_raw.json`. Runs no
simulation, so it is deterministic given that input.

Why this script exists
----------------------
The advisor site was carrying the PRE-water-filling-fix figure at n=4000 on a
card whose text describes the POST-fix n=10000 result, with alt-text that
claimed "at n=10000". The figure contradicted its own narrative. This regenerates
the figure the text actually describes.

The old figure also bundled a second "epsilon-cap compression" panel, which is an
illustration of the sampler bug rather than part of the tilt result. That story
now lives in the implementation section next to the water-filling diagram, and
the tilt card links to it, so this figure is deliberately single-panel.

Usage (from the repository root):

    python scripts/plot_q4_tilt_monotonicity_capfix.py
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
OUT_PATH = os.path.join(base_dir, "results", "figures",
                        "q4_tilt_monotonicity_capfix_n10000.png")

# gamma is signed with a natural neutral at 0 -> diverging encoding (two poles
# plus a neutral grey midpoint), never three categorical hues: no hue triplet
# separates under deuteranopia at these lightnesses. Marker shape is a redundant
# second channel and points the way the tilt points.
STYLE = {
    -1.0: dict(color="#2a78d6", marker="v", label="γ = −1   panic on low-degree banks"),
    0.0: dict(color="#5b6672", marker="o", label="γ = 0    panic spread evenly"),
    1.0: dict(color="#bd5a2e", marker="^", label="γ = +1   panic on hubs"),
}
INK = "#1e2530"
SOFT = "#5b6672"
PAPER = "#f6f3ea"
GRID = "#d7d1c2"

ANNOTATE_MU = 0.4  # the row the card quotes in prose


def main():
    if not os.path.exists(ANALYSIS_PATH):
        print(f"Error: committed analysis not found at {ANALYSIS_PATH}")
        sys.exit(1)
    with open(ANALYSIS_PATH) as f:
        data = json.load(f)

    meta = data.get("metadata", {})
    n_nodes, tau = meta.get("n"), meta.get("tau")
    points = data["points_by_gamma"]

    series = {}
    for key in STYLE:
        raw = points.get(str(key))
        if raw is None:
            print(f"Error: gamma={key} missing from the committed analysis")
            sys.exit(1)
        rows = sorted((p for p in raw if p.get("resolved")), key=lambda p: p["mu_bar"])
        series[key] = (np.array([p["mu_bar"] for p in rows]),
                       np.array([p["a_c_emp"] for p in rows]),
                       all(p.get("cap_free") for p in rows))

    # The claim on the card is that a_c is strictly decreasing in gamma at every
    # mu-bar row. Verify it here rather than trusting the prose.
    mus = series[0.0][0]
    violations = []
    for i, mu in enumerate(mus):
        trio = [series[g][1][i] for g in (-1.0, 0.0, 1.0)]
        if not (trio[0] > trio[1] > trio[2]):
            violations.append((float(mu), trio))
    rows_passed = len(mus) - len(violations)

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

    fig, ax = plt.subplots(figsize=(8.8, 5.3))
    ax.grid(True, color=GRID, lw=0.7, alpha=0.9)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    for key, style in STYLE.items():
        mu, a_c, _ = series[key]
        ax.plot(mu, a_c, color=style["color"], marker=style["marker"], ms=7.5,
                lw=1.9, mec=PAPER, mew=1.2, label=style["label"])

    # Call out the row the card quotes in prose.
    idx = int(np.argmin(np.abs(mus - ANNOTATE_MU)))
    trio = [series[g][1][idx] for g in (-1.0, 0.0, 1.0)]
    # Placed in the empty lower-left quadrant; it names its own mu-bar, so it
    # needs no leader line crossing the curves.
    ax.text(0.103, 4.75,
            f"at μ̄ = {mus[idx]:.1f} the critical seed falls\n"
            f"{trio[0]:.2f} (γ=−1)  →  {trio[1]:.2f} (γ=0)  →  {trio[2]:.2f} (γ=+1)",
            color=SOFT, fontsize=9.4, ha="left", va="center", linespacing=1.5)

    ax.set_xlabel("average panic  μ̄", color=INK)
    ax.set_ylabel("critical seed  $a_c^{\\mathrm{emp}}$   (smaller = easier to ignite)", color=INK)
    ax.legend(frameon=False, loc="upper right", fontsize=9.5, labelcolor=INK,
              handletextpad=0.6, borderaxespad=0.2)

    fig.suptitle("Concentrating panic on the best-connected banks makes collapse easier to trigger",
                 fontsize=12.6, color=INK, x=0.008, ha="left", y=0.985, fontweight="bold")
    fig.text(0.008, 0.902,
             f"Fewer failures are needed to set the cascade off, at every panic level "
             f"({rows_passed}/{len(mus)} μ̄ rows).",
             fontsize=10.4, color=SOFT, ha="left", va="center")

    all_cap_free = all(series[g][2] for g in STYLE)
    fig.text(0.008, 0.015,
             f"Configuration model, τ={tau}, n={n_nodes}, r=2, θ=0.5, paired on base_seed=42.\n"
             f"Re-run on the water-filling sampler; all three slices are "
             f"{'cap-free' if all_cap_free else 'NOT all cap-free'}.\n"
             "Source: results/processed/q4_size_biased_collapse_analysis.json "
             "(from the q4_phase2_n10000_*_capfix raws).",
             fontsize=8.6, color=SOFT, ha="left", va="bottom")

    fig.subplots_adjust(top=0.80, bottom=0.225, left=0.105, right=0.985)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=170)
    plt.close(fig)

    print(f"Wrote {OUT_PATH}")
    print(f"  n={n_nodes}, tau={tau}, all slices cap-free: {all_cap_free}")
    print(f"  strict monotonicity in gamma: {rows_passed}/{len(mus)} mu-bar rows")
    if violations:
        print(f"  VIOLATIONS: {violations}")


if __name__ == "__main__":
    main()
