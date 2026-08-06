"""Fear Amplifies cross-family comparison: single overlaid fear-curves figure.

Reads results/processed/famcompare_analysis.json (written by
scripts/analyze_famcompare.py) and renders results/figures/famcompare_ratio.png.
Read-only on the analysis artifact -- never writes or overwrites a results JSON.

Design (approved 2026-08-04, supersedes the 2026-08-03 four-panel strip):
Gary reviewed rendered candidates of four designs and chose the overlaid
"fear curves" form, then iterated it to this final spec (v4):
  - ONE set of axes: x = mu_bar in {0, 0.1, 0.2, 0.3, 0.4}, log-y fear
    multiplier P(systemic|mu_bar)/P(systemic|mu_bar=0). The old 4-panel
    strip shrank to an unreadable film-strip in the poster's ~square box.
  - One thick line per family at the representative n=10000 ONLY (no ghost
    dots for the other n). n=10000 chosen over n=20000 because the ER
    matched-baseline anchor drifted to 6% at 20k, censoring every cell at
    the 1/baseline ~ 16.7x floor with no measured point left; over n=4000
    because of small-n noise. All lines anchor at the trivial (0, 1x).
  - Hero-figure palette and markers (scripts/plot_poster_comparison.py):
    power-law/CM rust #BD5A2E "o", GIRG plum #8E4A72 "P", ER teal #2E6E76
    "^"; cream background #F6F3EA. CM is labeled "Power-law model" on the
    poster (Gary, 2026-08-04).
  - Ceiling-censored cells (ceiling_censored flag in the JSON, never
    inferred from magnitude): open marker + dashed upward arrow = the
    plotted ratio is a LOWER BOUND (numerator saturated at P=1). At
    n=10000 that is ER mu_bar in {0.2, 0.3, 0.4}; mu_bar=0.1 is a measured
    24.8x and renders filled.
  - NO CI graphics and NO in-figure source note / marker key: per Gary
    (2026-08-04) those live in okf/poster/poster.tex instead -- the
    open-marker explanation as visible caption text, the provenance line
    ("famcompare_analysis.json - 500 trials/cell - n=10000 - 95% bootstrap
    CIs in famcompare_analysis.json - ER's open points are lower bounds")
    as a LaTeX comment. CIs remain in the analysis JSON.
  - The ER bounded-seed (a=r=2) immunity arm is OFF this figure (it is a
    P=0 arm with an undefined ratio); it is stated in the poster prose
    instead. It must never be plotted as a ratio.

EXTENSION (2026-08-04): x-axis now runs to mu_bar=0.7, with per-family
availability read from FAMILY_MU_GRID rather than one shared MU_GRID list,
because the three families are NOT extended symmetrically (see
scripts/analyze_famcompare.py's module docstring for why):
  - erdos_renyi_matched reaches 0.7 (newly run ext arm).
  - girg reaches 0.7 across the full 0.1-0.7 grid (extended with mu=0.5 and 0.6 arms).
  - configuration_model reaches 0.7 too, as of the 2026-08-04 REBASE in
    analyze_famcompare.py: its n=10000 source switched from the q4-sourced
    mean-degree-4.0 series to the matched mean-degree-4.5336 poster_cm arms
    (same ensemble girg/ER-matched already use at n=10000), so all three
    families now run the full mu_bar in {0.1,...,0.7} with no gaps. CM's
    ratios shifted from the pre-rebase 2.0/2.4/3.2/3.5 (mu_bar 0.1-0.4,
    old q4 baseline P=0.024) to 1.26/1.58/2.21/3.05 (new matched baseline
    P=0.038) -- a different ensemble, not a re-measurement, so the change is
    expected and not a regression.
End-of-line declutter labels anchor past each family's own last x; CM's
connector is now the same length as ER-matched's/girg's since all three
reach 0.7.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANALYSIS_PATH = os.path.join(base_dir, "results/processed/famcompare_analysis.json")
FIG_PATH = os.path.join(base_dir, "results/figures/famcompare_ratio.png")

# Palette -- exact match to scripts/plot_poster_comparison.py.
COLOR_CM = "#BD5A2E"
COLOR_ER = "#2E6E76"
COLOR_GIRG = "#8E4A72"
CREAM_BG = "#F6F3EA"
TEXT_COLOR = "#1E2530"
SURFACE = "#FCFBF6"  # slightly lighter than CREAM_BG, chart plot area

# One ink color with alpha for hierarchy, as the hero does.
INK_PRIMARY = TEXT_COLOR
INK_SECONDARY = (0.118, 0.145, 0.188, 0.72)
INK_MUTED = (0.118, 0.145, 0.188, 0.50)
GRID = (0.118, 0.145, 0.188, 0.12)
AXIS_LINE = (0.118, 0.145, 0.188, 0.35)

FAMILY_COLOR = {
    "configuration_model": COLOR_CM,
    "girg": COLOR_GIRG,
    "erdos_renyi_matched": COLOR_ER,
}
FAMILY_MARKER = {
    "configuration_model": "o",
    "girg": "P",
    "erdos_renyi_matched": "^",
}
FAMILY_MARKER_SIZE = {  # P and ^ glyphs read smaller than o at equal `s`;
    "configuration_model": 130,  # bump them for equal visual weight.
    "girg": 150,
    "erdos_renyi_matched": 145,
}
FAMILY_LABEL = {
    "configuration_model": "Power-law model",
    "girg": "GIRG",
    "erdos_renyi_matched": "ER (matched baseline)",
}

FULL_MU_GRID = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
# Per-family availability (see analyze_famcompare.py's module docstring):
# configuration_model now has the full 0.1-0.7 run too (2026-08-04 rebase
# onto the matched poster_cm arms); girg and erdos_renyi_matched both have the full
# 0.1-0.7 run.
FAMILY_MU_GRID = {
    "configuration_model": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
    "girg": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
    "erdos_renyi_matched": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
}
N_REP = 10000

FIGSIZE = (10, 10)
DPI = 300
TITLE_FS = 26
SUBTITLE_FS = 16
AXIS_LABEL_FS = 20
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


def cell(panel, family, n, mu):
    return panel[family][str(n)]["by_mu"][f"{mu:g}"]


def fmt_ratio(ratio, censored):
    s = f"{ratio:.0f}×" if ratio >= 10 else f"{ratio:.1f}×"
    return ("≥" + s) if censored else s


def wrap_text(fig, text, fontsize, bold, max_width_in):
    renderer = fig.canvas.get_renderer()
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        t = fig.text(-10, -10, trial, fontsize=fontsize,
                     fontweight="bold" if bold else "normal")
        width_in = t.get_window_extent(renderer=renderer).width / fig.dpi
        t.remove()
        if width_in <= max_width_in or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def place_title_block(fig, title, subtitle, y_top=0.978, max_width_in=9.2,
                      x=0.5, ha="center"):
    fig_h = fig.get_size_inches()[1]
    y = y_top
    title_lines = wrap_text(fig, title, TITLE_FS, True, max_width_in)
    title_lh = (TITLE_FS / 72 * 1.28) / fig_h
    for line in title_lines:
        fig.text(x, y, line, fontsize=TITLE_FS, fontweight="bold", ha=ha,
                 va="top", color=INK_PRIMARY)
        y -= title_lh
    y -= 0.010
    sub_lines = wrap_text(fig, subtitle, SUBTITLE_FS, False, max_width_in)
    sub_lh = (SUBTITLE_FS / 72 * 1.32) / fig_h
    for line in sub_lines:
        fig.text(x, y, line, fontsize=SUBTITLE_FS, fontweight="normal", ha=ha,
                 va="top", color=INK_SECONDARY)
        y -= sub_lh
    return y


def declutter_log(values, min_gap_decades):
    logs = [np.log10(v) for v in values]
    adj = [logs[0]]
    for lg in logs[1:]:
        adj.append(max(lg, adj[-1] + min_gap_decades))
    return [10 ** a for a in adj]


def main():
    with open(ANALYSIS_PATH) as f:
        d = json.load(f)
    panel = d["main_panel"]
    if str(N_REP) not in panel.get("erdos_renyi_matched", {}):
        raise RuntimeError(
            f"n={N_REP} missing from the analysis main panel -- check "
            f"metadata.n_grid_used_main_panel in {ANALYSIS_PATH}."
        )

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=CREAM_BG)

    content_top = place_title_block(
        fig,
        "Fear amplifies ignition across families",
        "P(systemic | μ̄) / P(systemic | μ̄=0), n=10,000, log scale.",
    )

    ax_top = content_top - 0.015
    ax_bottom = 0.115
    ax = fig.add_axes([0.12, ax_bottom, 0.72, ax_top - ax_bottom])
    ax.set_facecolor(SURFACE)

    families = ["erdos_renyi_matched", "configuration_model", "girg"]

    end_info = []
    for fam in families:
        color = FAMILY_COLOR[fam]
        marker = FAMILY_MARKER[fam]
        msize = FAMILY_MARKER_SIZE[fam]
        mu_grid = FAMILY_MU_GRID[fam]
        xs_full = [0.0] + mu_grid
        ys, cens = [1.0], [False]
        for mu in mu_grid:
            c = cell(panel, fam, N_REP, mu)
            ys.append(c["ratio"])
            cens.append(c["ceiling_censored"])

        # All three families now carry measured cells at every FAMILY_MU_GRID
        # point (girg's 0.5/0.6 gap closed by the 2026-08-04 densification
        # arms), so no segment bridges an unmeasured gap.
        ax.plot(xs_full, ys, color=color, lw=4.0, zorder=4,
                solid_capstyle="round")

        for x, y, c in zip(xs_full, ys, cens):
            if c:
                ax.scatter([x], [y], s=msize + 40, marker=marker,
                           facecolors=SURFACE, edgecolors=color,
                           linewidths=3.0, zorder=6)
                ax.annotate("", xy=(x, y * 1.42), xytext=(x, y * 1.08),
                            arrowprops=dict(arrowstyle="-|>", color=color,
                                            lw=2.4, linestyle=(0, (3, 2))),
                            zorder=6)
            else:
                ax.scatter([x], [y], s=msize, marker=marker, facecolors=color,
                           edgecolors=SURFACE, linewidths=2.2, zorder=5)

        end_info.append([ys[-1], fam, color, marker, cens[-1], xs_full[-1]])

    end_info.sort(key=lambda r: r[0])
    fig_h_in = FIGSIZE[1]
    ax_h_in = (ax_top - ax_bottom) * fig_h_in
    ylim = (0.55, 60)
    decades = np.log10(ylim[1]) - np.log10(ylim[0])
    min_gap_in = 0.30
    min_gap_dec = (min_gap_in / ax_h_in) * decades
    label_ys = declutter_log([r[0] for r in end_info], min_gap_dec)

    # Label anchor column sits just past the RIGHTMOST family endpoint
    # (0.7, erdos_renyi_matched/girg), not a fixed 0.40 -- CM's connector
    # line is correspondingly longer since its own last x is still 0.4.
    LABEL_ANCHOR_X = max(FULL_MU_GRID) + 0.028
    LABEL_TEXT_X = max(FULL_MU_GRID) + 0.048
    for (end_y, fam, color, marker, c_last, end_x), label_y in zip(end_info, label_ys):
        if abs(np.log10(label_y) - np.log10(end_y)) > 1e-6 or end_x != LABEL_ANCHOR_X:
            ax.plot([end_x, LABEL_ANCHOR_X], [end_y, label_y], color=INK_MUTED, lw=1.0,
                    zorder=6)
        ax.scatter([LABEL_ANCHOR_X], [label_y], s=170, marker=marker, color=color,
                   zorder=7, edgecolors=SURFACE, linewidths=2.0)
        label = f"{FAMILY_LABEL[fam]}  {fmt_ratio(end_y, c_last)}"
        ax.text(LABEL_TEXT_X, label_y, label, fontsize=ANNOT_FS, color=INK_PRIMARY,
                va="center", ha="left", zorder=7, fontweight="bold")

    ax.axhline(1.0, color=INK_MUTED, lw=1.6, ls=(0, (5, 3)), zorder=1)
    ax.text(0.90, 1.0, "no effect", fontsize=ANNOT_FS - 3, color=INK_MUTED,
            ha="left", va="bottom")

    ax.set_yscale("log")
    ax.set_xlim(-0.03, 1.16)
    ax.set_ylim(*ylim)
    ax.set_xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    ax.set_xticklabels(["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7"])
    ax.set_yticks([1, 2, 5, 10, 20, 40])
    ax.set_yticklabels(["1×", "2×", "5×", "10×", "20×", "40×"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS_LINE)
        ax.spines[s].set_linewidth(1.2)
    ax.tick_params(axis="y", colors=INK_SECONDARY, labelsize=TICK_FS)
    ax.tick_params(axis="x", colors=INK_SECONDARY, labelsize=TICK_FS,
                   length=4, pad=8)
    ax.grid(True, which="major", axis="y", color=GRID, lw=1.0, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylabel("Fear multiplier  P(systemic | μ̄) / P(systemic | μ̄=0)",
                  fontsize=AXIS_LABEL_FS - 4)

    fig.text(0.48, ax_bottom - 0.058, "μ̄  (fear multiplier)",
             fontsize=AXIS_LABEL_FS - 4, ha="center", color=INK_PRIMARY)

    fig.savefig(FIG_PATH, dpi=DPI, facecolor=CREAM_BG)
    plt.close(fig)
    print(f"wrote {FIG_PATH}")


if __name__ == "__main__":
    main()
