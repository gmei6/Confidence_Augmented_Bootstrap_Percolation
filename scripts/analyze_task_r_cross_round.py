"""
Task R (Q5) cross-round analysis.

PRIMARY VERDICT (S-057 reframing, Gary's Option A): the strict-r_n-clique metric
is STRUCTURALLY BLIND to cross-round co-location, so this operationalization cannot
test C-Q5(i) at all -- it is not resolved by the real-vs-null z-test. A node is
certified "remote" in round t only if it is > r_n from EVERY previously-failed node
(run_task_r_cross_round.py:262-266). Therefore any later-round remote node is > r_n
from every earlier remote node, so no real cross-round pair is ever within r_n and
NO cross-round strict-r_n-clique can form -- round_gap == 0 for every real nucleus
by construction (proof, confirmed empirically). This is a TAUTOLOGY OF THE
MEASUREMENT, NOT a statement that cross-round ignition is physically absent: Task O's
lower-bound caveat (physical failed_neighbor_count accumulation across rounds; two
lone remote failures in the same ball in different rounds still ignite at r=2 --
okf/lessons.md) is a mechanism this metric cannot see. That caveat therefore stays
OPEN; the valid test is a supra-r_n cross-K (Option B), deferred.

RETIRED (confounded): the real-vs-null z-score and its pre-registered decision
rule. The null (run_task_r_cross_round.py:311-320) draws per-round from the
eligible pool WITHOUT the cross-round r_n-exclusion the real process enforces, so
the null admits cross-round cliques the real process forbids -- inflating null
counts 2.5-4.6x and driving z strongly negative for a purely STRUCTURAL reason,
not spatial physics. The z-test is retained below only as a provenance diagnostic
and must NOT be read as a test of cross-round correlation. (A genuine positive
test would require a supra-r_n cross-type pair-correlation / Ripley cross-K, i.e.
a different measurement -- deferred, Option B.)

Reads results/q5_task_r_cross_round_raw.json. Read-only on the raw JSON (never
recomputes the simulation); writes only to results/processed/.
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

        # STRUCTURAL cross-round diagnostic (the primary reading): a nucleus is
        # genuinely cross-round iff its members span >1 round, i.e. round_gap > 0.
        # By the certification rule this must be 0; we compute it from the raw
        # rather than assert it, so the artifact carries the evidence.
        gaps = [m["round_gap"] for r in cell_trials for m in r["real_nuclei_meta"]]
        cross_round_nuclei = sum(1 for g in gaps if g > 0)

        cell_reports[str(mu)] = {
            "n_trials": len(cell_trials),
            "real_total_cross_round_n_nuc": real_total,
            "per_round_nuclei_total": per_round_total,
            "additional_nuclei_vs_per_round": real_total - per_round_total,
            "per_trial_real_counts": [r["real_cross_round_n_nuc"] for r in cell_trials],
            "structural_cross_round_nuclei": cross_round_nuclei,
            "total_nuclei": len(gaps),
            "max_round_gap": max(gaps) if gaps else 0,
            "confounded_ztest_diagnostic": checkpoint_report,
            "confounded_ztest_passes_at_max_k": passes,
        }

    total_cross_round = sum(c["structural_cross_round_nuclei"] for c in cell_reports.values())
    total_nuclei = sum(c["total_nuclei"] for c in cell_reports.values())
    fraction_passing = cells_passing_threshold / len(cells) if cells else 0.0

    out = {
        "primary_verdict": {
            "clause": "C-Q5(i) cross-round remote nucleation (strict-r_n-clique operationalization)",
            "verdict": "STRICT_CLIQUE_METRIC_STRUCTURALLY_BLIND_TO_CROSS_ROUND",
            "structural_cross_round_nuclei_total": total_cross_round,
            "total_nuclei": total_nuclei,
            "basis": (
                "A round-t' remote node is > r_n from every earlier-failed node "
                "(certification rule, run_task_r_cross_round.py:262-266), so no real "
                "cross-round pair is within r_n and no cross-round strict-r_n-clique "
                "can form. Proof; confirmed by round_gap == 0 for all "
                f"{total_nuclei} real nuclei."),
            "interpretation": (
                "This is a TAUTOLOGY OF THE MEASUREMENT, not a statement about the "
                "physics: nodes are selected for being > r_n from all prior failures, "
                "then asked whether they are within r_n of a prior failure -- they never "
                "are. So the strict-r_n-clique metric is structurally INCAPABLE of "
                "detecting cross-round co-location; it does not establish that cross-round "
                "ignition is physically absent."),
            "task_o_caveat_status": (
                "OPEN, not closed. Task O's cross-round lower-bound caveat concerns "
                "physical failed_neighbor_count accumulation -- two lone remote failures "
                "in the same ball in DIFFERENT rounds still ignite at r=2 (okf/lessons.md) "
                "-- a mechanism this metric is blind to. This operationalization therefore "
                "cannot close that caveat; a supra-r_n cross-type pair-correlation / Ripley "
                "cross-K (Option B) is the valid test and remains the only way to answer "
                "C-Q5(i)'s cross-round question."),
        },
        "cells": cell_reports,
        "retired_confounded_ztest": {
            "status": "RETIRED -- confounded; NOT a valid test of cross-round correlation",
            "confound": (
                "The null (run_task_r_cross_round.py:311-320) draws per-round from the "
                "eligible pool without the cross-round r_n-exclusion the real process "
                "enforces, so it admits cross-round cliques the real process forbids "
                "(null 2.5-4.6x real). The strongly-negative z is a structural artifact, "
                "not spatial physics."),
            "z_threshold": DECISION_Z_THRESHOLD,
            "cell_fraction_threshold": DECISION_CELL_FRACTION,
            "cells_passing": cells_passing_threshold,
            "total_cells": len(cells),
            "fraction_passing": fraction_passing,
            "legacy_decision_label": (
                "PURSUE_FULLER_SWEEP" if fraction_passing >= DECISION_CELL_FRACTION
                else "DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS"),
            "deferred_valid_test": (
                "A genuine positive test needs a supra-r_n cross-type pair-correlation / "
                "Ripley cross-K between early- and late-round remote nuclei (Option B)."),
        },
        "source_raw": os.path.relpath(RAW_PATH, base_dir),
        "source_git_commit": raw["metadata"]["git_commit"],
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")
    print(f"PRIMARY VERDICT: {out['primary_verdict']['verdict']} "
          f"({total_cross_round}/{total_nuclei} nuclei cross-round -> metric cannot see "
          f"cross-round co-location; C-Q5(i) untested by this operationalization, "
          f"Task O caveat OPEN)")
    print(f"Retired z-test (confounded) legacy label: "
          f"{out['retired_confounded_ztest']['legacy_decision_label']}")


if __name__ == "__main__":
    analyze()
