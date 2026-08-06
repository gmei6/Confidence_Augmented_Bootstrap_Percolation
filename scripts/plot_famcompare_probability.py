"""Fear Amplifies cross-family comparison: raw P(systemic) vs fear figure.

Reads results/processed/famcompare_analysis.json (written by
scripts/analyze_famcompare.py) and renders results/figures/famcompare_probability.png.
Read-only on the analysis artifact -- never writes or overwrites a results JSON.

Design (2026-08-06, Gary): plots P(systemic | mu_bar) directly rather than
the fear-multiplier RATIO scripts/plot_famcompare_ratio.py draws, because the
ratio figure's ER-matched line dominates visually from its own tiny baseline
seed, obscuring the CM/GIRG comparison that's the actual point.
  - x = mu_bar (fear), y = P(systemic cascade), LINEAR scale -- probabilities
    span 0-0.25 here, a log axis would exaggerate small differences.
  - Two real curves, both at the SAME bounded seed a=2, n=10000: CM
    (configuration_model, "Power-law model") and GIRG -- the apples-to-apples
    comparison. erdos_renyi_matched is dropped entirely: it used its own
    seed calibrated to match CM/GIRG's mu_bar=0 baseline, never a=2, so it
    was never on this axis's scale to begin with.
  - erdos_renyi_bounded included as a third line at a=2 -- flat zero through
    mu_bar=0.7 (ER's own transition sits at a_c ~ 250-475, far above a=2), but
    NOT flat beyond that: 1.8% at 0.8, 7.6% at 0.9, 25.6% at 1.0 (2026-08-06
    extension). This is the mechanism in okf/lessons.md S-064/D-043 -- a
    fear-channel failure can supply the second failed neighbour the r=2 rule
    needs -- becoming visible at 500 trials/cell once mu_bar approaches 1.
  - Caption (bottom of figure) states a=2 for all curves explicitly -- the
    source of the prior figure's confusion.
  - Standalone figure only -- not wired into okf/poster/poster.tex yet.

REVISION (2026-08-06, Gary): title shortened to "The effect of fear";
Power-law/GIRG labels moved into an upper-left in-axes legend (was an
end-of-line label past mu=0.7, which forced xlim out to 1.05 just to fit
text -- that reserved axis space is now real plot area, so mu in [0,0.7]
fills more of the figure width); ER re-labeled in the legend (Gary,
2026-08-06, reversing the earlier drop-the-label call); the caption moved from a
subtitle under the title to a footer under the x-axis label, and the "(no
matched-baseline arm)" clause was cut as redundant now that the ratio
figure's ER-matched arm isn't drawn here at all.

EXTENSION (2026-08-06, Gary): mu_bar in {0.8, 0.9, 1.0} added (CM/GIRG/
erdos_renyi_bounded all newly run at n=10000/a=2, see
scripts/run_famcompare_ext2.py + scripts/analyze_famcompare.py's
EXT2_MU_GRID) -- mu_bar -> 1 is R_fear's own subcriticality boundary
(okf/lessons.md), not just "more slope". y-axis extended to 55% (CM reaches
51% at mu_bar=1.0) and ER-bounded is no longer flat across the full range.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANALYSIS_PATH = os.path.join(base_dir, "results/processed/famcompare_analysis.json")
FIG_PATH = os.path.join(base_dir, "results/figures/famcompare_probability.png")

COLOR_CM = "#BD5A2E"
COLOR_ER = "#2E6E76"
COLOR_GIRG = "#8E4A72"
CREAM_BG = "#F6F3EA"
TEXT_COLOR = "#1E2530"
SURFACE = "#FCFBF6"

INK_PRIMARY = TEXT_COLOR
INK_SECONDARY = (0.118, 0.145, 0.188, 0.72)
INK_MUTED = (0.118, 0.145, 0.188, 0.50)
GRID = (0.118, 0.145, 0.188, 0.12)
AXIS_LINE = (0.118, 0.145, 0.188, 0.35)

N_REP = 10000
MU_GRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

FIGSIZE = (10, 10)
DPI = 300
TITLE_FS = 26
SUBTITLE_FS = 16
AXIS_LABEL_FS = 16
TICK_FS = 16
ANNOT_FS = 15

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK_PRIMARY,
    "axes.edgecolor": AXIS_LINE,
    "axes.labelcolor": INK_PRIMARY,
    "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY,
})


def main():
    with open(ANALYSIS_PATH) as f:
        d = json.load(f)
    rc = d["raw_cells"]
    cm = rc["configuration_model"][str(N_REP)]
    girg = rc["girg"][str(N_REP)]
    er_flat = d["erdos_renyi_bounded_flat_zero"][str(N_REP)]

    def mu_key(mu):
        # Matches json.dump's default float-key stringification exactly
        # (str(1.0) == "1.0", not the "1" that an f"{mu:g}" format would give
        # -- that mismatch silently KeyErrors on mu_bar=1.0's cell).
        return str(mu)

    cm_ys = [cm[mu_key(mu)]["p_systemic"] for mu in MU_GRID]
    girg_ys = [girg[mu_key(mu)]["p_systemic"] for mu in MU_GRID]
    er_ys = [er_flat[mu_key(mu)] for mu in MU_GRID]

    TITLE_TEXT = "The effect of fear when a = 2"
    AX_BOTTOM = 0.16
    AX_HEIGHT = 0.76
    ax_top = AX_BOTTOM + AX_HEIGHT

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=CREAM_BG)

    # Measure the title's rendered height so the whitespace above the title
    # (figure top -> title top) equals the whitespace below it (title bottom
    # -> plot top), rather than two arbitrarily-chosen margins.
    probe = fig.text(0.5, 0.5, TITLE_TEXT, fontsize=TITLE_FS, fontweight="bold",
                      ha="center", va="top")
    fig.canvas.draw()
    title_h = probe.get_window_extent(renderer=fig.canvas.get_renderer()).height / (
        FIGSIZE[1] * DPI)
    probe.remove()
    gap = (1.0 - title_h - ax_top) / 2.0
    title_y = 1.0 - gap

    fig.text(0.5, title_y, TITLE_TEXT,
              fontsize=TITLE_FS, fontweight="bold", ha="center", va="top",
              color=INK_PRIMARY)

    ax = fig.add_axes([0.13, AX_BOTTOM, 0.80, AX_HEIGHT])
    ax.set_facecolor(SURFACE)

    (line_cm,) = ax.plot(
        MU_GRID, cm_ys, color=COLOR_CM, lw=4.0, marker="o", markersize=11,
        markerfacecolor=COLOR_CM, markeredgecolor=SURFACE, markeredgewidth=2.0,
        zorder=4, solid_capstyle="round", label="Power-law model")
    (line_girg,) = ax.plot(
        MU_GRID, girg_ys, color=COLOR_GIRG, lw=4.0, marker="P", markersize=12,
        markerfacecolor=COLOR_GIRG, markeredgecolor=SURFACE, markeredgewidth=2.0,
        zorder=4, solid_capstyle="round", label="GIRG")
    # ER in the legend too (Gary, 2026-08-06 -- reverses the earlier
    # drop-the-label call: the flat-then-spike ER line is the panel's point
    # and must be nameable by the viewer).
    (line_er,) = ax.plot(
        MU_GRID, er_ys, color=COLOR_ER, lw=4.0, marker="^", markersize=11,
        markerfacecolor=COLOR_ER, markeredgecolor=SURFACE, markeredgewidth=2.0,
        zorder=3, solid_capstyle="round", label="Erdős–Rényi")

    legend = ax.legend(handles=[line_cm, line_girg, line_er], loc="upper left",
                        frameon=False, fontsize=ANNOT_FS,
                        handlelength=1.6, borderaxespad=0.6)
    for text, line in zip(legend.get_texts(), [line_cm, line_girg, line_er]):
        text.set_color(line.get_color())
        text.set_fontweight("bold")

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.025, 0.55)
    ax.set_xticks(MU_GRID)
    ax.set_xticklabels([f"{m:g}" for m in MU_GRID])
    ax.set_yticks([0.0, 0.10, 0.20, 0.30, 0.40, 0.50])
    ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%", "50%"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS_LINE)
        ax.spines[s].set_linewidth(1.2)
    ax.tick_params(axis="both", labelsize=TICK_FS)
    ax.grid(True, which="major", axis="y", color=GRID, lw=1.0, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylabel("P(systemic cascade)", fontsize=AXIS_LABEL_FS)
    ax.set_xlabel("μ̄  (fear multiplier)", fontsize=AXIS_LABEL_FS)

    fig.text(0.5, 0.055,
              "P(systemic | μ̄), n=10,000. Every curve uses the same bounded seed a=2.",
              fontsize=SUBTITLE_FS, ha="center", va="top", color=INK_SECONDARY)

    fig.savefig(FIG_PATH, dpi=DPI, facecolor=CREAM_BG)
    plt.close(fig)
    print(f"wrote {FIG_PATH}")


if __name__ == "__main__":
    main()
