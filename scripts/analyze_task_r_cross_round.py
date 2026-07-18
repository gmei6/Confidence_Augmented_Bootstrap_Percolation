"""
Task R (Q5) cross-round pilot analysis: real-vs-null excess statistic and the
pre-registered decision rule.

Reads results/q5_task_r_cross_round_raw.json (scripts/run_task_r_cross_round.py)
and, per mean-fear cell and per K checkpoint in {1, 10, 30}:
  - real_total: sum of real_cross_round_n_nuc across trials in the cell
  - the K null cell-level totals (summing each replicate index across trials)
  - z-score of real_total against the null distribution's mean/SD (K=1 excluded
    from the statistical test -- no SD is estimable from a single draw)
  - per-trial excess (real - mean-null), to flag whether a cell's verdict is
    driven by a small number of outlier trials
  - per_round_nuclei_total (existing metric) vs real_cross_round_n_nuc, for the
    raw "how much lower-bound undercounting" comparison

Applies the pre-registered decision rule (Task R Final Brief, S-05x): z > 2 in
>= 2/3 of pilot cells -> recommend a fuller n=8000+ sweep; otherwise, attribute
the cross-round signal to depletion coincidence and the existing honest-negative
(constant-leak) reading stands as final.

Read-only on the raw JSON (never recomputes the simulation); writes only to
results/processed/.
"""

import os
import json

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_PATH = os.path.join(base_dir, "results/q5_task_r_cross_round_raw.json")
OUTPUT_PATH = os.path.join(base_dir, "results/processed/task_r_cross_round_analysis.json")

DECISION_Z_THRESHOLD = 2.0
DECISION_CELL_FRACTION = 2.0 / 3.0


def analyze():
    with open(RAW_PATH) as f:
        raw = json.load(f)

    results = raw["results"]
    cells = sorted(set(r["mean_fear"] for r in results))
    checkpoints = raw["metadata"]["null_replicate_checkpoints"]

    cell_reports = {}
    cells_passing_threshold = 0
    for mu in cells:
        cell_trials = [r for r in results if r["mean_fear"] == mu]
        real_total = sum(r["real_cross_round_n_nuc"] for r in cell_trials)
        per_round_total = sum(r["per_round_nuclei_total"] for r in cell_trials)

        checkpoint_report = {}
        for k in checkpoints:
            per_trial_null_lists = [r["null_totals_by_checkpoint"][str(k)] for r in cell_trials]
            if not all(len(lst) == k for lst in per_trial_null_lists):
                checkpoint_report[k] = {"error": "incomplete null replicates at this checkpoint"}
                continue
            null_cell_totals = [sum(lst[rep] for lst in per_trial_null_lists) for rep in range(k)]
            mean_null = float(np.mean(null_cell_totals))
            sd_null = float(np.std(null_cell_totals, ddof=1)) if k > 1 else float("nan")

            entry = {
                "mean_null_total": mean_null,
                "sd_null_total": sd_null,
                "real_total": real_total,
                "excess": real_total - mean_null,
            }
            if k >= 2 and sd_null > 0:
                entry["z_score"] = (real_total - mean_null) / sd_null
            else:
                entry["z_score"] = None
                entry["note"] = "K too small or SD=0 -- cost-characterization only, not a statistical test"
            checkpoint_report[k] = entry

        max_k = max(checkpoints)
        final_z = checkpoint_report[max_k].get("z_score")
        passes = final_z is not None and final_z > DECISION_Z_THRESHOLD
        if passes:
            cells_passing_threshold += 1

        cell_reports[str(mu)] = {
            "n_trials": len(cell_trials),
            "real_total_cross_round_n_nuc": real_total,
            "per_round_nuclei_total": per_round_total,
            "additional_nuclei_vs_per_round": real_total - per_round_total,
            "per_trial_real_counts": [r["real_cross_round_n_nuc"] for r in cell_trials],
            "checkpoints": checkpoint_report,
            "passes_decision_threshold_at_max_k": passes,
        }

    fraction_passing = cells_passing_threshold / len(cells) if cells else 0.0
    decision = (
        "PURSUE_FULLER_SWEEP" if fraction_passing >= DECISION_CELL_FRACTION
        else "DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS"
    )

    out = {
        "cells": cell_reports,
        "decision_rule": {
            "z_threshold": DECISION_Z_THRESHOLD,
            "cell_fraction_threshold": DECISION_CELL_FRACTION,
            "cells_passing": cells_passing_threshold,
            "total_cells": len(cells),
            "fraction_passing": fraction_passing,
            "decision": decision,
        },
        "source_raw": os.path.relpath(RAW_PATH, base_dir),
        "source_git_commit": raw["metadata"]["git_commit"],
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Decision: {decision} ({cells_passing_threshold}/{len(cells)} cells passed z>{DECISION_Z_THRESHOLD})")


if __name__ == "__main__":
    analyze()
