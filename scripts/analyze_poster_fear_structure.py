"""Fear x Structure: percentage decrease in each family's own measured a_c(mu_bar)
relative to its own mu_bar=0 anchor, plus the ER-only (1-mu_bar)^2 theory curve
for reference.

Read-only on results/processed/poster_comparison.json (never rewrites it --
that file is analyze_poster_comparison.py's output). Writes
results/processed/poster_fear_structure.json for
scripts/plot_poster_fear_structure.py to read.

Why this replaces the old D-012 measured/predicted-RATIO framing (okf/decisions,
D-012 poster evidentiary choices): the (1-mu_bar)^2 prediction is derived for
Erdos-Renyi only. Reporting CM/GIRG's measured crossing as a "ratio to
predicted" implicitly treats an ER-only formula as the baseline they were
supposed to hit, then calls their (structurally expected) departure from it a
finding. The self-contained, family-agnostic statement is simpler and doesn't
borrow ER's formula for other families: how far has EACH family's own crossing
moved from ITS OWN zero-fear anchor. Percentage decrease = 1 - a_c(mu)/a_c(0).

mu_bar=0.7 re-enters this figure for every family -- its exclusion in the old
framing was an artifact of the predicted-crossing floor check (D-012's
below_floor flag fires when the ER-derived PREDICTION drops under the
structural floor a=r=2, which is irrelevant here since this figure never uses
that prediction for CM/GIRG). It keeps a near-floor footnote marker instead:
flagged whenever a family's own MEASURED crossing (not the ER-only prediction)
sits within NEAR_FLOOR_RATIO of the actual floor r, since a measurement that
close to the floor can be compressed by the floor itself, independent of the
fear effect being described.

Family curves are read from poster_comparison.json's d012_table by iterating
whatever family/mu_bar rows are actually present -- nothing here is a hardcoded
family or mu_bar list, so a future densification arm (e.g. GIRG at
mu_bar in {0.1, 0.2, 0.3}) appears automatically the next time this is re-run.
"""

import json
import os
import sys

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash

INPUT_PATH = os.path.join(base_dir, "results", "processed", "poster_comparison.json")
OUTPUT_PATH = os.path.join(base_dir, "results", "processed", "poster_fear_structure.json")

# A measured crossing within this multiple of the structural floor r=2 (a
# cascade needs a >= r seeds to be well-defined at all) can be compressed by
# the floor itself, independent of the fear effect this figure is isolating.
# Chosen to flag CM/GIRG's mu_bar=0.7 points (crossings ~4.26 and ~4.31 against
# r=2, i.e. ~2.1-2.2x) while leaving every ER point (>>2x at every mu_bar in
# this sweep) and every mu_bar<=0.4 CM/GIRG point unflagged.
NEAR_FLOOR_RATIO = 2.2


def main() -> None:
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"{INPUT_PATH} not found -- run analyze_poster_comparison.py first")

    with open(INPUT_PATH, "r") as f:
        payload = json.load(f)

    d012 = payload["d012_table"]
    R_FLOOR = 2  # pinned r across every poster_* config (configs/poster_*.json "r": 2)

    family_curves = {}
    for row in d012:
        fam = row["family"]
        mu = row["mean_fear"]
        if mu == 0.0:
            continue  # the anchor itself is 0% decrease by construction; not a data point on this figure
        ratio = row["measured_ratio_to_mu0"]
        ratio_lo = row["measured_ratio_to_mu0_ci_lower"]
        ratio_hi = row["measured_ratio_to_mu0_ci_upper"]
        pct_decrease = (1.0 - ratio) * 100.0
        # CI on the ratio flips direction when converted to a decrease: a
        # higher ratio (less decrease) is the LOW end of pct_decrease.
        pct_decrease_ci_low = (1.0 - ratio_hi) * 100.0
        pct_decrease_ci_high = (1.0 - ratio_lo) * 100.0
        near_floor = bool((row["measured_crossing"] / R_FLOOR) <= NEAR_FLOOR_RATIO)

        family_curves.setdefault(fam, []).append({
            "mean_fear": mu,
            "pct_decrease": pct_decrease,
            "pct_decrease_ci_low": pct_decrease_ci_low,
            "pct_decrease_ci_high": pct_decrease_ci_high,
            "measured_crossing": row["measured_crossing"],
            "near_floor": near_floor,
        })

    for fam in family_curves:
        family_curves[fam].sort(key=lambda r: r["mean_fear"])

    # ER-only theory curve: (1-mu_bar)^2, i.e. the same D-012 prediction formula,
    # plotted here as a labeled reference (dashed, computed-not-measured) rather
    # than as a baseline every family is scored against.
    mu_theory = np.linspace(0.0, 0.75, 76)
    pct_theory = (1.0 - (1.0 - mu_theory) ** 2) * 100.0

    out = {
        "metadata": {
            "script": "scripts/analyze_poster_fear_structure.py",
            "git_commit": get_git_commit_hash(),
            "source": os.path.relpath(INPUT_PATH, base_dir),
            "source_analysis_commit": payload["metadata"]["git_commit"],
            "near_floor_ratio_threshold": NEAR_FLOOR_RATIO,
            "structural_floor_r": R_FLOOR,
            "note": (
                "Percentage decrease in each family's own measured a_c(mu_bar) "
                "relative to its own mu_bar=0 anchor. Self-checked derivation of "
                "poster_comparison.json's d012_table; not independently "
                "/verify-gated on its own (the underlying comparison sweeps are)."
            ),
        },
        "family_curves": family_curves,
        "theory_curve": {
            "label": "ER-only theory (1-mu_bar)^2, computed not measured",
            "mean_fear": mu_theory.tolist(),
            "pct_decrease": pct_theory.tolist(),
        },
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")
    for fam, rows in family_curves.items():
        for row in rows:
            flag = " (near floor)" if row["near_floor"] else ""
            print(
                f"  {fam:<22} mu={row['mean_fear']:.1f}  "
                f"decrease={row['pct_decrease']:.1f}% "
                f"[{row['pct_decrease_ci_low']:.1f}, {row['pct_decrease_ci_high']:.1f}]{flag}"
            )


if __name__ == "__main__":
    main()
