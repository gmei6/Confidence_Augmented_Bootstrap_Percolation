"""Draw the model schematic (D-046, S-065 advisor directive; site variant S-066).

A small hand-placed network illustrating the two activation routes:
  - solvency/percolation: a node with >= r = 2 failed neighbors fails next
    round (dashed outline);
  - fear: any node can fail with probability f_i * g_t, even far from the
    failed cluster.

NOT a simulation output -- a deliberately legible illustration. Every
coordinate is hand-set so the figure is deterministic with no RNG and no
layout dependency (no networkx). The node positions and edge list are
shared by both variants; only the palette, per-node styling, annotation
text, and canvas/output differ, via the CONFIGS dict below.

Two variants (--variant):
  poster (default) -- okf/poster/poster.tex's cream palette, with a
    fear ring (thickness/darkness ~ f_i) on E1/E2/E3 and an in-figure
    legend. Written to results/figures/model_schematic.png. This is the
    original figure; its bytes must not change when this script is
    invoked with no flags (verified by md5, S-066).
      failed  #B3282D (true red -- advisor's directive; NOT tcRust)
      fear    #BD5A2E (tcRust ring)
      healthy #2E6E76 (tcTeal)
  site -- the QR demo's dark palette (poster-demo/style.css), matching
    the landing screen's legend-key vocabulary exactly: teal = still
    standing, rust = failed structurally, plum = failed by fear. No
    rings (the site does not encode susceptibility, only failure
    cause), no in-figure legend (the page's own legend-key sits below
    the image). Written to poster-demo/img/model_schematic_dark.png.
    Phone-friendly aspect (~1.9:1); the poster's legend corner is
    reclaimed for the fear annotation.

Usage:
    arch -arm64 python3 scripts/plot_model_schematic.py
    arch -arm64 python3 scripts/plot_model_schematic.py --variant site
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTER_FIG_PATH = os.path.join(REPO_ROOT, "results", "figures", "model_schematic.png")
SITE_FIG_PATH = os.path.join(REPO_ROOT, "poster-demo", "img", "model_schematic_dark.png")

# --- hand-placed graph (wide-short canvas), shared by both variants -------
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
PERC_NEXT = {"P"}  # >= r failed neighbors, fails next round

R_NODE = 0.24

# --- per-variant configuration ---------------------------------------------
POSTER = dict(
    variant="poster",
    out_path=POSTER_FIG_PATH,
    figsize=(10.4, 3.9),
    dpi=300,
    xlim=(0.15, 13.9),
    ylim=(0.05, 4.55),
    background="#F6F3EA",
    edge_color="#D8D2C2",
    ink="#1E2530",
    ink_soft="#5B6672",
    teal="#2E6E76",
    rust="#BD5A2E",
    failed_face="#B3282D",
    perc_edge="#B3282D",
    perc_face="#F6F3EA",
    plum_fear=None,          # poster encodes fear via rings, not fill
    fear_ring={"E1": 1.00, "E2": 0.60, "E3": 0.30},
    draw_legend=True,
    annotations=[
        dict(node="F2", text="failed cluster --- drives\nthe global fear field $g_t$",
             xy_off=(-0.05, 0.28), xytext=(0.45, 4.25)),
        dict(node="P", text="solvency route: $\\geq r=2$ failed\nneighbors "
             "$\\Rightarrow$ fails next round",
             xy_off=(0.10, -0.26), xytext=(3.45, 0.55)),
        dict(node="E1", text="fear route: fails w.p. $f_i\\,g_t$,\n"
             "even far from the cluster",
             xy_off=(0.26, 0.20), xytext=(10.25, 3.05)),
    ],
)

SITE = dict(
    variant="site",
    out_path=SITE_FIG_PATH,
    figsize=(10.4, 5.0),
    dpi=200,
    xlim=(0.15, 10.4),
    ylim=(0.05, 5.30),
    background="#0d1117",
    edge_color="#30363d",
    ink="#c9d1d9",
    ink_soft="#8b949e",
    teal="#2E6E76",
    rust="#BD5A2E",
    failed_face="#BD5A2E",   # failed structurally -- rust fill
    perc_edge="#BD5A2E",     # about to fail by the neighbour rule
    perc_face="#0d1117",
    plum_fear={"E1"},        # failed by fear -- plum fill, no ring
    plum="#8E4A72",
    fear_ring=None,          # site does not encode susceptibility
    draw_legend=False,       # the landing page's legend-key covers this
    annotations=[
        dict(node="F2", text="failed by neighbours ---\nthese drive the fear level $g_t$",
             xy_off=(-0.05, 0.28), xytext=(0.30, 5.00)),
        dict(node="P", text="$\\geq r = 2$ failed neighbours\n$\\Rightarrow$ fails next round",
             xy_off=(0.10, -0.26), xytext=(2.55, 0.45)),
        dict(node="E1", text="failed by FEAR: chance $f_i\\,g_t$,\nno failed neighbours at all",
             xy_off=(0.15, 0.24), xytext=(6.35, 4.55)),
    ],
)


def node_style(name, cfg):
    """Return (face, edge, lw, ls) for one node under a variant config."""
    if name in FAILED:
        return cfg["failed_face"], cfg["failed_face"], 1.5, "-"
    if name in PERC_NEXT:
        return cfg["perc_face"], cfg["perc_edge"], 2.6, (0, (4, 2.2))
    if cfg["plum_fear"] and name in cfg["plum_fear"]:
        return cfg["plum"], cfg["plum"], 1.5, "-"
    return cfg["teal"], cfg["teal"], 1.5, "-"


def draw(cfg):
    fig, ax = plt.subplots(figsize=cfg["figsize"])
    fig.patch.set_facecolor(cfg["background"])
    ax.set_facecolor(cfg["background"])
    ax.set_xlim(*cfg["xlim"])
    ax.set_ylim(*cfg["ylim"])
    ax.set_aspect("equal")
    ax.axis("off")

    for a, b in EDGES:
        (x1, y1), (x2, y2) = NODES[a], NODES[b]
        ax.plot([x1, x2], [y1, y2], color=cfg["edge_color"], lw=2.2, zorder=1,
                solid_capstyle="round")

    for name, (x, y) in NODES.items():
        face, edge, lw, ls = node_style(name, cfg)
        if cfg["fear_ring"] and name in cfg["fear_ring"]:
            f = cfg["fear_ring"][name]
            ax.add_patch(Circle((x, y), R_NODE + 0.12, facecolor="none",
                                edgecolor=cfg["rust"], lw=2.0 + 3.2 * f,
                                alpha=0.45 + 0.55 * f, zorder=2))
        ax.add_patch(Circle((x, y), R_NODE, facecolor=face, edgecolor=edge,
                            lw=lw, linestyle=ls, zorder=3))

    ann_kw = dict(fontsize=12, color=cfg["ink"], ha="left", va="center", zorder=4)
    arrow_kw = dict(arrowstyle="-", color=cfg["ink_soft"], lw=1.4,
                    shrinkA=2, shrinkB=8)
    for ann in cfg["annotations"]:
        nx, ny = NODES[ann["node"]]
        dx, dy = ann["xy_off"]
        ax.annotate(ann["text"], xy=(nx + dx, ny + dy), xytext=ann["xytext"],
                    arrowprops=arrow_kw, **ann_kw)

    if cfg["draw_legend"]:
        legend_items = [
            Line2D([], [], marker="o", ls="none", markersize=12,
                   markerfacecolor=cfg["failed_face"], markeredgecolor=cfg["failed_face"],
                   label="failed"),
            Line2D([], [], marker="o", ls="none", markersize=12,
                   markerfacecolor=cfg["teal"], markeredgecolor=cfg["teal"],
                   label="healthy"),
            Line2D([], [], marker="o", ls="none", markersize=12,
                   markerfacecolor=cfg["teal"], markeredgecolor=cfg["rust"], markeredgewidth=2.8,
                   label="feeling fear (ring $\\propto f_i$)"),
            Line2D([], [], marker="o", ls="none", markersize=12,
                   markerfacecolor=cfg["background"], markeredgecolor=cfg["failed_face"],
                   markeredgewidth=2.0, label="fails next round ($r$-rule)"),
        ]
        leg = ax.legend(handles=legend_items, loc="lower right",
                        bbox_to_anchor=(1.0, -0.02), frameon=True,
                        fontsize=10.5, borderpad=0.55, labelspacing=0.45,
                        handletextpad=0.45)
        leg.get_frame().set_facecolor(cfg["background"])
        leg.get_frame().set_edgecolor(cfg["edge_color"])

    fig.tight_layout()
    out_path = cfg["out_path"]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=cfg["dpi"], bbox_inches="tight",
                facecolor=cfg["background"])
    plt.close(fig)
    print(f"wrote {out_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=["poster", "site"], default="poster",
                        help="poster: cream palette for okf/poster/poster.tex (default); "
                             "site: dark palette for the poster-demo QR landing screen")
    args = parser.parse_args()
    cfg = POSTER if args.variant == "poster" else SITE
    draw(cfg)


if __name__ == "__main__":
    main()
