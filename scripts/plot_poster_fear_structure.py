"""Fear x Structure poster figure: percentage decrease in each family's own
measured a_c(mu_bar), normalized to its own mu_bar=0 anchor -- replacing the
old D-012 measured/predicted-ratio framing (ER-only theory as an implicit
baseline for every family).

Reads results/processed/poster_fear_structure.json (written by
scripts/analyze_poster_fear_structure.py). Read-only on that artifact -- never
writes or overwrites a results JSON (same discipline as plot_poster_comparison.py
and plot_finite_size_scaling_r2_n10000.py).

Family curves are drawn by iterating whatever keys are present in the JSON's
family_curves dict -- no hardcoded family list or mu_bar grid, so a future
densification arm (e.g. GIRG at mu_bar in {0.1, 0.2, 0.3}) appears
automatically the next time analyze_poster_fear_structure.py is re-run and
this script is re-run after it.
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INPUT_PATH = os.path.join(base_dir, "results", "processed", "poster_fear_structure.json")
FIG_PATH = os.path.join(base_dir, "results", "figures", "poster_fear_structure.png")

# Same family palette/markers as plot_poster_comparison.py, for visual
# continuity between the poster's two data figures.
FAMILY_STYLE = {
    "configuration_model": {"color": "#BD5A2E", "marker": "o", "label": "Power-law (CM, $\\tau=2.5$)"},
    "erdos_renyi": {"color": "#2E6E76", "marker": "^", "label": "ER"},
    "girg": {"color": "#8E4A72", "marker": "P", "label": "GIRG"},
}
BG_COLOR = "#F6F3EA"
TEXT_COLOR = "#1E2530"


def main() -> None:
    with open(INPUT_PATH) as f:
        d = json.load(f)

    # theory_curve is intentionally never read here: the figure compares
    # measured families against each other, and the ER-only (1-mu_bar)^2
    # reference is the one element that isn't a cross-model measurement, so
    # it's been dropped from the plot. The JSON keeps it -- this is a
    # plotting choice, not an analysis-artifact change.
    family_curves = d["family_curves"]

    plt.rcParams.update({
        "figure.facecolor": BG_COLOR,
        "axes.facecolor": BG_COLOR,
        "axes.edgecolor": TEXT_COLOR,
        "axes.labelcolor": TEXT_COLOR,
        "xtick.color": TEXT_COLOR,
        "ytick.color": TEXT_COLOR,
        "text.color": TEXT_COLOR,
        "font.family": "sans-serif",
        "font.size": 11,
    })

    fig, ax = plt.subplots(figsize=(7.0, 6.0), dpi=300)
    ax.set_facecolor(BG_COLOR)

    for fam, rows in family_curves.items():
        style = FAMILY_STYLE.get(fam, {"color": "#333333", "marker": "s", "label": fam})
        mus = [r["mean_fear"] for r in rows]
        # Plotted as negative so a percentage DECREASE reads downward on the
        # page (mu_bar=0 anchor at 0%, curves descend as fear grows).
        pct = [-r["pct_decrease"] for r in rows]

        # Plain line + markers -- no CI errorbars (owner call, 2026-08-04):
        # the poster reads cleaner without them and the underlying comparison
        # sweeps are already verified elsewhere.
        ax.plot(
            mus, pct,
            color=style["color"], marker=style["marker"], linestyle="-",
            linewidth=2.0, markersize=8,
            markeredgecolor="white", markeredgewidth=0.8,
            label=style["label"], zorder=3,
        )

        # near_floor flags remain in the JSON (poster_fear_structure.json,
        # per-row "near_floor"), but the ring/asterisk visual that used to
        # mark them is removed (owner call, 2026-08-04). Rationale: the
        # a=r=2 structural-floor argument is deterministic only at mu_bar=0
        # -- once fear is active, a fear-channel failure can supply the
        # second failed neighbor, so ignition from a single seed has
        # positive probability and the floor is not absolute at mu_bar>0.
        # Flagging points as "near the floor" therefore overstated a
        # boundary that doesn't actually bind here.

    ax.set_xlabel(r"Mean fear $\bar\mu$", fontsize=12, fontweight="bold", labelpad=8)
    # Plain "vs." (no LaTeX "\ " idiom): that only expands under real LaTeX,
    # and matplotlib's default text renderer prints the backslash literally
    # outside of $...$ math mode -- same class of bug as the nu-figure title.
    ax.set_ylabel(r"Decrease in $a_c(\bar\mu)$ vs. own $\bar\mu=0$ anchor (%)",
                  fontsize=12, fontweight="bold", labelpad=8)
    ax.set_xlim(-0.02, 0.75)
    # Inverted: 0% (the mu_bar=0 anchor) at the top, -100% at the bottom, so
    # a bigger decrease reads as further down the page. Small headroom above
    # 0 (3 units) mirrors the original's headroom below 0.
    ax.set_ylim(-100, 3)
    ax.set_yticks([0, -25, -50, -75, -100])
    ax.set_yticklabels(["0%", "-25%", "-50%", "-75%", "-100%"])
    ax.set_title(
        "Hubs Blunt Fear's Effect\n"
        r"$n=10{,}000$, each family normalized to its own $\bar\mu=0$ crossing",
        fontsize=11.5, fontweight="bold", pad=12, color=TEXT_COLOR,
    )
    ax.grid(True, linestyle=":", alpha=0.5, color=TEXT_COLOR)
    # Curves now start near 0% (top-left, low mu_bar) and descend toward
    # -100% (bottom-right, high mu_bar) -- the mirror image of the old
    # ascending layout. "upper left" would now sit right on top of the
    # curves' starting points, so the legend moves to "lower left", the
    # empty corner under the inverted layout (matches the reasoning that
    # placed it at "upper left" before: away from where the lines are).
    # Still the empty corner now that the errorbars/near-floor rings are
    # gone -- rechecked, nothing else moved into it.
    ax.legend(loc="lower left", fontsize=9.5, frameon=True, facecolor=BG_COLOR, edgecolor=TEXT_COLOR)

    # Footnote/provenance text block removed (owner call, 2026-08-04):
    # provenance stays recorded in the JSON metadata (results/processed/
    # poster_fear_structure.json) and in the poster.tex comments. No bottom
    # text block means no reserved space for it -- pad_inches trimmed since
    # there's no longer a caption to leave room for, so the figure doesn't
    # carry a dead band at the bottom.
    fig.savefig(
        FIG_PATH, dpi=300, facecolor=BG_COLOR,
        bbox_inches="tight", pad_inches=0.08,
        metadata={"Creation Time": None, "Software": None},
    )
    plt.close(fig)
    print(f"Saved {FIG_PATH}")


if __name__ == "__main__":
    main()
