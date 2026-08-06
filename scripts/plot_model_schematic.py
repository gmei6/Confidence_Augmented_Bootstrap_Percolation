"""Draw the poster's model schematic (D-046, S-065 advisor directive).

A small hand-placed network illustrating the two activation routes:
  - solvency/percolation: a node with >= r = 2 failed neighbors fails next
    round (dashed red outline);
  - fear: any node can fail with probability f_i * g_t, even far from the
    failed cluster (rust ring, thickness/darkness = fear level f_i).

NOT a simulation output -- a deliberately legible illustration for the
presenter to point at (the advisor's framing: the poster is a prop for the
conversation). Every coordinate is hand-set so the figure is deterministic
with no RNG and no layout dependency (no networkx). Wide-short aspect
(~2.7:1) so it fits the poster's left column without displacing the QR
block (verified by tectonic compile, S-066).

Colors match okf/poster/poster.tex's palette exactly (D-046: colors used
consistently to distinguish node states; red = infected/failed per the
advisor, distinct encoding for fear):
  failed  #B3282D  (true red -- advisor's directive; NOT tcRust)
  fear    #BD5A2E  (tcRust, the poster's warm "fear" accent, as a RING)
  healthy #2E6E76  (tcTeal, the poster's structure accent)
  ink     #1E2530 / #5B6672, background #F6F3EA (tcCream)

Usage:
    arch -arm64 python3 scripts/plot_model_schematic.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG_PATH = os.path.join(REPO_ROOT, "results", "figures", "model_schematic.png")

CREAM = "#F6F3EA"
INK = "#1E2530"
INK_SOFT = "#5B6672"
RULE = "#D8D2C2"
TEAL = "#2E6E76"
RUST = "#BD5A2E"
RED = "#B3282D"

# --- hand-placed graph (wide-short canvas) ---------------------------------
# id: (x, y)
NODES = {
    "F1": (1.30, 2.20), "F2": (2.30, 3.10), "F3": (2.15, 1.30),
    "P":  (3.35, 2.30),
    "H1": (0.95, 3.90), "H2": (3.75, 3.95), "H3": (5.15, 3.30),
    "H4": (4.80, 1.05), "H5": (6.10, 0.75), "H6": (7.55, 3.55),
    "H7": (9.05, 0.85), "H8": (0.80, 0.55),
    "E1": (8.70, 2.15),  # high fear, failing via the fear route
    "E2": (6.40, 2.35),  # moderate fear
    "E3": (7.45, 0.55),  # mild fear
}
EDGES = [
    ("F1", "F2"), ("F1", "F3"), ("F2", "F3"),
    ("F2", "P"), ("F3", "P"),
    ("F1", "H1"), ("F2", "H2"), ("F3", "H8"), ("F1", "H8"),
    ("P", "H2"), ("P", "H4"),
    ("H2", "H3"), ("H3", "E2"), ("H3", "H6"),
    ("H4", "H5"), ("H4", "E2"), ("H5", "E3"),
    ("E2", "H6"), ("H6", "E1"), ("E1", "H7"),
    ("E3", "H7"), ("E1", "E3"), ("H5", "H8"),
]
FAILED = {"F1", "F2", "F3"}
PERC_NEXT = {"P"}                      # >= r failed neighbors, fails next round
FEAR_RING = {"E1": 1.00, "E2": 0.60, "E3": 0.30}  # ring weight ~ fear level f_i

R_NODE = 0.24


def main():
    fig, ax = plt.subplots(figsize=(10.4, 3.9))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    ax.set_xlim(0.15, 13.9)
    ax.set_ylim(0.05, 4.55)
    ax.set_aspect("equal")
    ax.axis("off")

    for a, b in EDGES:
        (x1, y1), (x2, y2) = NODES[a], NODES[b]
        ax.plot([x1, x2], [y1, y2], color=RULE, lw=2.2, zorder=1,
                solid_capstyle="round")

    for name, (x, y) in NODES.items():
        if name in FAILED:
            face, edge, lw, ls = RED, RED, 1.5, "-"
        elif name in PERC_NEXT:
            face, edge, lw, ls = CREAM, RED, 2.6, (0, (4, 2.2))
        else:
            face, edge, lw, ls = TEAL, TEAL, 1.5, "-"
        if name in FEAR_RING:
            f = FEAR_RING[name]
            ax.add_patch(Circle((x, y), R_NODE + 0.12, facecolor="none",
                                edgecolor=RUST, lw=2.0 + 3.2 * f,
                                alpha=0.45 + 0.55 * f, zorder=2))
        ax.add_patch(Circle((x, y), R_NODE, facecolor=face, edgecolor=edge,
                            lw=lw, linestyle=ls, zorder=3))

    # --- right-side annotation panel (x >= 10.2 is text-only space) --------
    ann_kw = dict(fontsize=12, color=INK, ha="left", va="center", zorder=4)
    arrow_kw = dict(arrowstyle="-", color=INK_SOFT, lw=1.4,
                    shrinkA=2, shrinkB=8)

    fx, fy = NODES["F2"]
    ax.annotate("failed cluster --- drives\nthe global fear field $g_t$",
                xy=(fx - 0.05, fy + 0.28), xytext=(0.45, 4.25),
                arrowprops=arrow_kw, **ann_kw)

    px, py = NODES["P"]
    ax.annotate("solvency route: $\\geq r=2$ failed\nneighbors "
                "$\\Rightarrow$ fails next round",
                xy=(px + 0.10, py - 0.26), xytext=(3.45, 0.55),
                arrowprops=arrow_kw, **ann_kw)

    ex, ey = NODES["E1"]
    ax.annotate("fear route: fails w.p. $f_i\\,g_t$,\n"
                "even far from the cluster",
                xy=(ex + 0.26, ey + 0.20), xytext=(10.25, 3.05),
                arrowprops=arrow_kw, **ann_kw)

    legend_items = [
        Line2D([], [], marker="o", ls="none", markersize=12,
               markerfacecolor=RED, markeredgecolor=RED, label="failed"),
        Line2D([], [], marker="o", ls="none", markersize=12,
               markerfacecolor=TEAL, markeredgecolor=TEAL, label="healthy"),
        Line2D([], [], marker="o", ls="none", markersize=12,
               markerfacecolor=TEAL, markeredgecolor=RUST, markeredgewidth=2.8,
               label="feeling fear (ring $\\propto f_i$)"),
        Line2D([], [], marker="o", ls="none", markersize=12,
               markerfacecolor=CREAM, markeredgecolor=RED, markeredgewidth=2.0,
               label="fails next round ($r$-rule)"),
    ]
    leg = ax.legend(handles=legend_items, loc="lower right",
                    bbox_to_anchor=(1.0, -0.02), frameon=True,
                    fontsize=10.5, borderpad=0.55, labelspacing=0.45,
                    handletextpad=0.45)
    leg.get_frame().set_facecolor(CREAM)
    leg.get_frame().set_edgecolor(RULE)

    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=300, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"wrote {FIG_PATH}")


if __name__ == "__main__":
    main()
