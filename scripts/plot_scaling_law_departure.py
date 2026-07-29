"""Plot scaling law departure: critical seed scaling a_c(mu) / a_c(0) vs D-012 theory."""

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
    out_png = os.path.join(fig_dir, "scaling_law_departure.png")

    if not os.path.exists(proc_path):
        raise FileNotFoundError(f"Processed JSON not found at {proc_path}")

    with open(proc_path, "r") as f:
        payload = json.load(f)

    d012_table = payload["d012_table"]

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

    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=300)
    ax.set_facecolor(BG_COLOR)

    # 1. Overlay D-012 theory curve (1 - mu)^2
    mu_grid = np.linspace(0.0, 0.75, 200)
    y_theory = (1.0 - mu_grid) ** 2
    ax.plot(mu_grid, y_theory, "k--", linewidth=1.5, label=r"D-012: $(1 - \bar{\mu})^2$", zorder=2)

    # Calculate CM floor threshold in terms of mu where D-012 pred < 2
    # For CM, a_c(0) ~ 10.22 -> 10.22 * (1 - mu)^2 < 2 => mu > 1 - sqrt(2/10.22) ~ 0.558
    cm_anchor = [r["measured_crossing"] for r in d012_table if r["family"] == "configuration_model" and r["mean_fear"] == 0.0][0]
    mu_floor_cm = 1.0 - np.sqrt(2.0 / cm_anchor)

    # Shade the region where D-012 prediction falls below r = 2 for CM
    ax.axvspan(mu_floor_cm, 0.75, color="#D0C8B8", alpha=0.35, zorder=1, label=r"Structural floor (CM pred $< r=2$)")
    ax.text(
        (mu_floor_cm + 0.75) / 2.0, 0.65,
        "Structural floor\n($a_c^{\\mathrm{pred}} < r=2$)",
        fontsize=9, color=TEXT_COLOR, fontstyle="italic", ha="center", va="center", alpha=0.85
    )

    families = [
        ("erdos_renyi", "Erdős–Rényi", COLOR_ER, "^"),
        ("configuration_model", "Configuration Model", COLOR_CM, "o"),
    ]

    for fam_key, fam_label, color, marker in families:
        rows = [r for r in d012_table if r["family"] == fam_key]
        rows.sort(key=lambda r: r["mean_fear"])

        mus = np.array([r["mean_fear"] for r in rows])
        y = np.array([r["measured_ratio_to_mu0"] for r in rows])
        y_low = np.array([r["measured_ratio_to_mu0_ci_lower"] for r in rows])
        y_high = np.array([r["measured_ratio_to_mu0_ci_upper"] for r in rows])
        below_floor = np.array([r["below_floor"] for r in rows])

        yerr_lower = np.maximum(0.0, y - y_low)
        yerr_upper = np.maximum(0.0, y_high - y)
        yerr = np.vstack([yerr_lower, yerr_upper])

        # Plot line connecting all points
        ax.plot(mus, y, color=color, linestyle="-", linewidth=1.8, alpha=0.85, zorder=3)

        # Plot points clearing floor vs below floor
        cleared_mask = ~below_floor
        if np.any(cleared_mask):
            ax.errorbar(
                mus[cleared_mask], y[cleared_mask], yerr=yerr[:, cleared_mask],
                color=color, linestyle="None", marker=marker,
                markersize=7, markerfacecolor=color, markeredgecolor=color,
                capsize=3.5, capthick=1.2, linewidth=1.5, zorder=4,
                label=f"{fam_label} (clears floor)"
            )

        if np.any(below_floor):
            ax.errorbar(
                mus[below_floor], y[below_floor], yerr=yerr[:, below_floor],
                color=color, linestyle="None", marker=marker,
                markersize=8, markerfacecolor="white", markeredgecolor=color, markeredgewidth=2.0,
                capsize=3.5, capthick=1.2, linewidth=1.5, zorder=4,
                label=f"{fam_label} (below floor)"
            )

    ax.set_xlabel(r"Mean fear ($\bar{\mu}$)", fontsize=12, fontweight="bold", labelpad=8)
    ax.set_ylabel(r"Critical seed ratio $a_c(\bar{\mu}) \,/\, a_c(0)$", fontsize=12, fontweight="bold", labelpad=8)
    ax.set_xlim(-0.02, 0.73)
    ax.set_ylim(-0.05, 1.25)
    ax.set_title(r"Scaling Law Departure: ER vs CM ($n=10000$, $\langle k \rangle \approx 4.53$)",
                 fontsize=12, fontweight="bold", pad=12, color=TEXT_COLOR)

    ax.grid(True, linestyle=":", alpha=0.5, color=TEXT_COLOR)
    ax.legend(frameon=True, facecolor=BG_COLOR, edgecolor=TEXT_COLOR, fontsize=9.5, loc="upper right")

    plt.tight_layout()
    fig.savefig(
        out_png, dpi=300, facecolor=BG_COLOR,
        metadata={"Creation Time": None, "Software": None},
    )
    plt.close(fig)
    print(f"Plot saved to {out_png}")


if __name__ == "__main__":
    main()
