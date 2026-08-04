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
THEORY_COLOR = "#767676"  # neutral gray: computed reference, not a measured series


def main() -> None:
    with open(INPUT_PATH) as f:
        d = json.load(f)

    family_curves = d["family_curves"]
    theory = d["theory_curve"]

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

    # Theory line drawn first, dashed and gray, and explicitly labeled as
    # computed rather than measured (project lesson: a computed value must be
    # visually distinct from a measured one, never sharing a solid line style
    # or a family's own color).
    ax.plot(
        theory["mean_fear"], theory["pct_decrease"],
        color=THEORY_COLOR, linestyle="--", linewidth=2.0, zorder=1,
        label="ER-only theory $(1-\\bar\\mu)^2$ (computed, not measured)",
    )

    near_floor_present = False
    for fam, rows in family_curves.items():
        style = FAMILY_STYLE.get(fam, {"color": "#333333", "marker": "s", "label": fam})
        mus = [r["mean_fear"] for r in rows]
        pct = [r["pct_decrease"] for r in rows]
        lo = [r["pct_decrease"] - r["pct_decrease_ci_low"] for r in rows]
        hi = [r["pct_decrease_ci_high"] - r["pct_decrease"] for r in rows]

        ax.errorbar(
            mus, pct, yerr=[lo, hi],
            color=style["color"], marker=style["marker"], linestyle="-",
            linewidth=2.0, markersize=8, capsize=4, elinewidth=1.2,
            markeredgecolor="white", markeredgewidth=0.8,
            label=style["label"], zorder=3,
        )

        # Near-floor footnote marker: an open ring around the point, not a
        # color change (color already carries family identity here).
        for r in rows:
            if r["near_floor"]:
                near_floor_present = True
                ax.scatter(
                    [r["mean_fear"]], [r["pct_decrease"]],
                    s=220, facecolors="none", edgecolors=style["color"],
                    linewidths=1.6, zorder=4,
                )
                ax.annotate(
                    "*", xy=(r["mean_fear"], r["pct_decrease"]),
                    xytext=(6, 8), textcoords="offset points",
                    fontsize=13, color=style["color"], fontweight="bold",
                )

    ax.set_xlabel(r"Mean fear $\bar\mu$", fontsize=12, fontweight="bold", labelpad=8)
    # Plain "vs." (no LaTeX "\ " idiom): that only expands under real LaTeX,
    # and matplotlib's default text renderer prints the backslash literally
    # outside of $...$ math mode -- same class of bug as the nu-figure title.
    ax.set_ylabel(r"Decrease in $a_c(\bar\mu)$ vs. own $\bar\mu=0$ anchor (%)",
                  fontsize=12, fontweight="bold", labelpad=8)
    ax.set_xlim(-0.02, 0.75)
    ax.set_ylim(-3, 100)
    ax.set_title(
        "Fear × Structure: Hubs Blunt Fear's Effect on the Tipping Point\n"
        r"$n=10{,}000$, each family normalized to its own $\bar\mu=0$ crossing",
        fontsize=11.5, fontweight="bold", pad=12, color=TEXT_COLOR,
    )
    ax.grid(True, linestyle=":", alpha=0.5, color=TEXT_COLOR)
    ax.legend(loc="upper left", fontsize=9.5, frameon=True, facecolor=BG_COLOR, edgecolor=TEXT_COLOR)

    # Plain wording, not the internal "/verify-gated" shorthand: this image
    # prints on the poster, same reasoning as the poster.tex prose substitution.
    footnote = (
        "Self-checked (not independently re-verified on its own; the underlying "
        "comparison sweeps are verified). Source: results/processed/poster_fear_structure.json "
        f"(commit {d['metadata']['git_commit'][:7]})."
    )
    if near_floor_present:
        footnote = (
            "* crossing within 2.2x of the structural floor a=r=2 -- some compression "
            "from the floor itself is possible there, independent of the fear effect. "
        ) + footnote

    fig.text(0.5, -0.02, footnote, ha="center", fontsize=7.5, color="#666666", wrap=True)

    fig.savefig(
        FIG_PATH, dpi=300, facecolor=BG_COLOR,
        bbox_inches="tight", pad_inches=0.15,
        metadata={"Creation Time": None, "Software": None},
    )
    plt.close(fig)
    print(f"Saved {FIG_PATH}")


if __name__ == "__main__":
    main()
