"""Plot poster headline comparison: degree heterogeneity effect on cascade ignition."""

import json
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

COLOR_CM = "#BD5A2E"
COLOR_ER = "#2E6E76"
COLOR_GIRG = "#8E4A72"  # okf/poster/poster.tex tcPlum — third family, geometry (GIRG)
BG_COLOR = "#F6F3EA"
TEXT_COLOR = "#1E2530"

# One-hue OKLCH ramps per family: light = low mean fear, dark = high mean
# fear (dark end anchored to the existing brand color). Validated against
# BG_COLOR with the dataviz skill's ordinal-ramp checks (monotone L, >=0.06
# adjacent lightness gap, >=2:1 light-end contrast).
CM_RAMP = {0.0: "#ec8559", 0.4: "#d46f44", 0.7: COLOR_CM}
ER_RAMP = {0.0: "#72b1b9", 0.4: "#508f97", 0.7: COLOR_ER}
GIRG_RAMP = {0.0: "#c087a6", 0.4: "#a8688b", 0.7: COLOR_GIRG}


def main() -> None:
    os.chdir(base_dir)
    proc_path = os.path.join(base_dir, "results", "processed", "poster_comparison.json")
    fig_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    out_png = os.path.join(fig_dir, "poster_comparison.png")

    if not os.path.exists(proc_path):
        raise FileNotFoundError(f"Processed JSON not found at {proc_path}")

    with open(proc_path, "r") as f:
        payload = json.load(f)

    records = payload["records"]

    grouped = {}
    for r in records:
        key = (r["family"], r["mean_fear"])
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)

    for key in grouped:
        grouped[key].sort(key=lambda x: x["seed_size"])

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

    fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=300)
    ax.set_facecolor(BG_COLOR)

    series_config = [
        {"family": "configuration_model", "mu": 0.0, "color": CM_RAMP[0.0], "ls": "-", "marker": "o", "label": r"CM ($\tau=2.5$), $\bar{\mu}=0.0$"},
        {"family": "configuration_model", "mu": 0.4, "color": CM_RAMP[0.4], "ls": "-", "marker": "o", "label": r"CM ($\tau=2.5$), $\bar{\mu}=0.4$"},
        {"family": "configuration_model", "mu": 0.7, "color": CM_RAMP[0.7], "ls": "-", "marker": "o", "label": r"CM ($\tau=2.5$), $\bar{\mu}=0.7$"},
        {"family": "erdos_renyi", "mu": 0.0, "color": ER_RAMP[0.0], "ls": "-", "marker": "^", "label": r"ER ($\langle k \rangle=4.53$), $\bar{\mu}=0.0$"},
        {"family": "erdos_renyi", "mu": 0.4, "color": ER_RAMP[0.4], "ls": "-", "marker": "^", "label": r"ER ($\langle k \rangle=4.53$), $\bar{\mu}=0.4$"},
        {"family": "erdos_renyi", "mu": 0.7, "color": ER_RAMP[0.7], "ls": "-", "marker": "^", "label": r"ER ($\langle k \rangle=4.53$), $\bar{\mu}=0.7$"},
        {"family": "girg", "mu": 0.0, "color": GIRG_RAMP[0.0], "ls": "-", "marker": "P", "label": r"GIRG ($\langle k \rangle=4.53$), $\bar{\mu}=0.0$"},
        {"family": "girg", "mu": 0.4, "color": GIRG_RAMP[0.4], "ls": "-", "marker": "P", "label": r"GIRG ($\langle k \rangle=4.53$), $\bar{\mu}=0.4$"},
        {"family": "girg", "mu": 0.7, "color": GIRG_RAMP[0.7], "ls": "-", "marker": "P", "label": r"GIRG ($\langle k \rangle=4.53$), $\bar{\mu}=0.7$"},
    ]

    for cfg in series_config:
        key = (cfg["family"], cfg["mu"])
        if key not in grouped:
            continue
        items = grouped[key]
        x = np.array([it["seed_size"] for it in items])
        y = np.array([it["p_systemic"] for it in items])

        ax.plot(
            x, y,
            color=cfg["color"], linestyle=cfg["ls"], marker=cfg["marker"],
            linewidth=2.0, markersize=6,
            label=cfg["label"]
        )

    ax.set_xscale("log")
    ax.set_xlabel("Seed size (a)", fontsize=12, fontweight="bold", labelpad=8)
    ax.set_ylabel("P(systemic)", fontsize=12, fontweight="bold", labelpad=8)
    ax.set_ylim(-0.03, 1.03)
    ax.set_title("Degree Heterogeneity Effect on Cascade Ignition ($n=10000$, $\\langle k \\rangle \\approx 4.53$)",
                 fontsize=12, fontweight="bold", pad=12, color=TEXT_COLOR)

    ax.grid(True, linestyle=":", alpha=0.5, color=TEXT_COLOR)
    ax.legend(frameon=True, facecolor=BG_COLOR, edgecolor=TEXT_COLOR, fontsize=10, loc="best")

    plt.tight_layout()
    fig.savefig(
        out_png, dpi=300, facecolor=BG_COLOR,
        metadata={"Creation Time": None, "Software": None},
    )
    plt.close(fig)
    print(f"Plot saved to {out_png}")


if __name__ == "__main__":
    main()
