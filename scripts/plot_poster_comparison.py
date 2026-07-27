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
BG_COLOR = "#F6F3EA"
TEXT_COLOR = "#1E2530"


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
        {"family": "configuration_model", "mu": 0.0, "color": COLOR_CM, "ls": "-", "marker": "o", "label": r"CM ($\tau=2.5$), $\bar{\mu}=0.0$"},
        {"family": "configuration_model", "mu": 0.4, "color": COLOR_CM, "ls": "--", "marker": "s", "label": r"CM ($\tau=2.5$), $\bar{\mu}=0.4$"},
        {"family": "configuration_model", "mu": 0.7, "color": COLOR_CM, "ls": ":", "marker": "D", "label": r"CM ($\tau=2.5$), $\bar{\mu}=0.7$"},
        {"family": "erdos_renyi", "mu": 0.0, "color": COLOR_ER, "ls": "-", "marker": "^", "label": r"ER ($\langle k \rangle=4.53$), $\bar{\mu}=0.0$"},
        {"family": "erdos_renyi", "mu": 0.4, "color": COLOR_ER, "ls": "--", "marker": "v", "label": r"ER ($\langle k \rangle=4.53$), $\bar{\mu}=0.4$"},
        {"family": "erdos_renyi", "mu": 0.7, "color": COLOR_ER, "ls": ":", "marker": "<", "label": r"ER ($\langle k \rangle=4.53$), $\bar{\mu}=0.7$"},
    ]

    for cfg in series_config:
        key = (cfg["family"], cfg["mu"])
        if key not in grouped:
            continue
        items = grouped[key]
        x = np.array([it.get("a_over_ac", it["seed_size"] / it["janson_a_c"]) for it in items])
        y = np.array([it["p_systemic"] for it in items])
        y_low = np.array([it["wilson_ci_lower"] for it in items])
        y_high = np.array([it["wilson_ci_upper"] for it in items])

        yerr = np.vstack([y - y_low, y_high - y])

        ax.errorbar(
            x, y, yerr=yerr,
            color=cfg["color"], linestyle=cfg["ls"], marker=cfg["marker"],
            linewidth=2.0, markersize=6, capsize=3, capthick=1.2,
            label=cfg["label"]
        )

    ax.set_xlabel("Seed size relative to Janson prediction (a / a_c)", fontsize=12, fontweight="bold", labelpad=8)
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
