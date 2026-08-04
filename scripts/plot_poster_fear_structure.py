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

Typography restyle (owner call, 2026-08-04): title/subtitle hierarchy, ink
colors, DejaVu Sans font family, and spine/grid treatment now match
scripts/plot_famcompare_ratio.py so the poster's two data figures read as
one typographic system -- large bold title in primary ink, small
regular-weight subtitle in faded secondary ink, regular-weight (non-bold)
axis labels in primary ink, tick labels in secondary ink. Title/subtitle/
label/tick sizes are famcompare's constants scaled down by this figure's
canvas width vs. famcompare's 10in canvas, so the visual weight matches
despite the smaller figure. Content is unchanged: three plain lines,
inverted y-axis, legend at lower-left, family colors/markers, cream
background.
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

# Ink hierarchy + font/spine treatment, matched to plot_famcompare_ratio.py's
# INK_PRIMARY / INK_SECONDARY / AXIS_LINE / GRID constants (same underlying
# RGB as TEXT_COLOR, same alpha values) so the two poster figures share one
# typographic system.
INK_PRIMARY = TEXT_COLOR
INK_SECONDARY = (0.118, 0.145, 0.188, 0.72)
AXIS_LINE = (0.118, 0.145, 0.188, 0.35)
GRID_COLOR = (0.118, 0.145, 0.188, 0.12)

FIGSIZE = (7.0, 6.0)
DPI = 300

# famcompare's TITLE_FS/SUBTITLE_FS/AXIS_LABEL_FS/TICK_FS constants, scaled
# by this figure's canvas width vs. famcompare's 10in-wide canvas
# (scripts/plot_famcompare_ratio.py FIGSIZE=(10, 10)), so title/label/tick
# text reads at matching visual weight despite the smaller figure. Note
# famcompare's *applied* axis-label size is AXIS_LABEL_FS - 4 = 16, and its
# subtitle/applied-axis-label/tick sizes are all 16 -- only the title (26)
# is set apart as the dominant element; that hierarchy carries through here.
_FAMCOMPARE_CANVAS_W_IN = 10.0
_SCALE = FIGSIZE[0] / _FAMCOMPARE_CANVAS_W_IN
TITLE_FS = round(26 * _SCALE, 1)
SUBTITLE_FS = round(16 * _SCALE, 1)
AXIS_LABEL_FS = round(16 * _SCALE, 1)
TICK_FS = round(16 * _SCALE, 1)


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
        "axes.edgecolor": AXIS_LINE,
        "axes.labelcolor": INK_PRIMARY,
        "xtick.color": INK_SECONDARY,
        "ytick.color": INK_SECONDARY,
        "text.color": INK_PRIMARY,
        "font.family": "DejaVu Sans",
        "font.size": TICK_FS,
    })

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
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

    # Axis labels: regular weight (not bold), primary ink -- matches
    # famcompare's axes.labelcolor=INK_PRIMARY with no fontweight override.
    ax.set_xlabel(r"Mean fear $\bar\mu$", fontsize=AXIS_LABEL_FS,
                  fontweight="normal", color=INK_PRIMARY, labelpad=8)
    # Plain "vs." (no LaTeX "\ " idiom): that only expands under real LaTeX,
    # and matplotlib's default text renderer prints the backslash literally
    # outside of $...$ math mode -- same class of bug as the nu-figure title.
    ax.set_ylabel(r"Decrease in $a_c(\bar\mu)$ vs. own $\bar\mu=0$ anchor (%)",
                  fontsize=AXIS_LABEL_FS, fontweight="normal",
                  color=INK_PRIMARY, labelpad=8)
    ax.set_xlim(-0.02, 0.75)
    # Inverted: 0% (the mu_bar=0 anchor) at the top, -100% at the bottom, so
    # a bigger decrease reads as further down the page. Small headroom above
    # 0 (3 units) mirrors the original's headroom below 0.
    ax.set_ylim(-100, 3)
    ax.set_yticks([0, -25, -50, -75, -100])
    ax.set_yticklabels(["0%", "-25%", "-50%", "-75%", "-100%"])
    ax.tick_params(axis="both", labelsize=TICK_FS, colors=INK_SECONDARY)

    # Title/subtitle split (owner call, 2026-08-04): large bold title in
    # primary ink via fig.suptitle, small regular-weight subtitle in faded
    # secondary ink via ax.set_title -- same hierarchy as famcompare's
    # place_title_block, without needing its custom wrap/layout machinery
    # since this figure's single-axes layout + bbox_inches="tight" already
    # auto-sizes around whatever title/subtitle height is needed.
    fig.suptitle("Hubs Blunt Fear's Effect", fontsize=TITLE_FS,
                 fontweight="bold", color=INK_PRIMARY, y=0.985)
    ax.set_title(
        "n = 10,000, each family normalized to its own μ̄ = 0 crossing",
        fontsize=SUBTITLE_FS, fontweight="normal", color=INK_SECONDARY,
        pad=14,
    )
    # No separate `alpha=` kwarg: GRID_COLOR is already an RGBA tuple with
    # its own alpha (0.12, matching famcompare's GRID constant) -- passing
    # `alpha=` here would override that component instead of compounding it.
    ax.grid(True, linestyle=":", linewidth=1.0, color=GRID_COLOR)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS_LINE)
        ax.spines[s].set_linewidth(1.2)
    # Curves now start near 0% (top-left, low mu_bar) and descend toward
    # -100% (bottom-right, high mu_bar) -- the mirror image of the old
    # ascending layout. "upper left" would now sit right on top of the
    # curves' starting points, so the legend moves to "lower left", the
    # empty corner under the inverted layout (matches the reasoning that
    # placed it at "upper left" before: away from where the lines are).
    # Still the empty corner now that the errorbars/near-floor rings are
    # gone -- rechecked, nothing else moved into it.
    ax.legend(loc="lower left", fontsize=9.5, frameon=True, facecolor=BG_COLOR, edgecolor=AXIS_LINE)

    # Footnote/provenance text block removed (owner call, 2026-08-04):
    # provenance stays recorded in the JSON metadata (results/processed/
    # poster_fear_structure.json) and in the poster.tex comments. No bottom
    # text block means no reserved space for it -- pad_inches trimmed since
    # there's no longer a caption to leave room for, so the figure doesn't
    # carry a dead band at the bottom.
    fig.savefig(
        FIG_PATH, dpi=DPI, facecolor=BG_COLOR,
        bbox_inches="tight", pad_inches=0.08,
        metadata={"Creation Time": None, "Software": None},
    )
    plt.close(fig)
    print(f"Saved {FIG_PATH}")


if __name__ == "__main__":
    main()
