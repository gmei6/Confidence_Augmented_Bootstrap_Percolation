"""
Task X (Q4, C-Q4(i)): tilt monotonicity re-analysis on the CAP-FIXED sampler.

Same as scripts/analyze_task_n_phase2.py, but repointed at the three
configs/q4_phase2_n10000_gamma*_capfix.json slices -- the re-run of the paired
gamma design (base_seed=42) on the merged Task Q water-filling sampler (commit
c4ef634). Every prior gamma=0->+1 result was cap-affected (7-28% realized-mu_bar
shortfall); this re-analysis tests whether, with realized_mu_bar now tracking
mu_bar, the gamma>0 cells become cap-free (gamma_is_cap_free True) so the
gamma=0->+1 leg is a VALID equal-total-fear test of C-Q4(i) rather than an
artifact.

The cap_diagnostics call inside analyze_task_n.main() re-samples with the
current (fixed) sampler, so the cap_free flags reflect the fix directly.

Writes results/processed/task_x_tilt_capfix_analysis.json (does NOT overwrite the
S-046/Phase-2 artifacts).
"""

import importlib.util
import json
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

spec = importlib.util.spec_from_file_location(
    "analyze_task_n", os.path.join(base_dir, "scripts", "analyze_task_n.py"))
analyze_task_n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze_task_n)

OUTPUT_PATH = "results/processed/task_x_tilt_capfix_analysis.json"

analyze_task_n.PHASE1B_CONFIGS = [
    "configs/q4_phase2_n10000_gammaneg1_capfix.json",
    "configs/q4_phase2_n10000_gamma0_capfix.json",
    "configs/q4_phase2_n10000_gammapos1_capfix.json",
]
analyze_task_n.OUTPUT_PATH = OUTPUT_PATH
analyze_task_n.phase1_supercritical_readout = lambda: {
    "note": "Phase 1 supercritical readout lives in "
            "results/processed/task_n_tilt_analysis.json (S-046); "
            "not restated in this cap-fixed re-analysis."
}


def main():
    analyze_task_n.main()
    out_path = os.path.join(base_dir, OUTPUT_PATH)
    with open(out_path) as f:
        out = json.load(f)
    out["metadata"]["task"] = ("X (Q4 tilt monotonicity re-test on the cap-fixed "
                               "sampler, C-Q4(i))")
    # analyze_task_n.main() writes a static verdict.note that is accurate for the
    # ORIGINAL cap-affected Task N run (gamma=+1 cap-affected at every mu-bar>=0.1)
    # but STALE here: the Task Q water-filling fix makes realized_mu_bar track mu_bar,
    # so gamma=+1 is now cap-free. Overwrite the note with one derived from THIS run's
    # actual data so the artifact does not contradict its own data.
    #
    # Reviewer finding #1: derive cap-free DIRECTLY from cap_diagnostics (realized_mu_bar
    # tracking mu_bar for every nonzero-mu row of ALL slices), NOT from the pair verdicts'
    # cap_affected_mu_rows counter -- that counter is tallied only over mu rows where both
    # slices RESOLVED a crossing, so a cap-affected-and-unresolved row could leave it 0 and
    # fire the strong "every mu-bar" note on data that doesn't support it.
    CAP_TOL = 0.02  # relative realized-mu_bar shortfall tolerance (matches analyze_task_n)
    per_mu_gamma = out["cap_diagnostics"]["per_mu_gamma"]

    def _row_cap_free(diag, mu):
        return abs(diag["realized_mu_bar"] - mu) / mu <= CAP_TOL

    all_slices_cap_free = all(
        _row_cap_free(diag, float(mu_str))
        for mu_str, by_gamma in per_mu_gamma.items() if float(mu_str) != 0.0
        for diag in by_gamma.values())
    pv = out["verdict"]["pair_verdicts"]
    both_pairs_pass = all(v.get("pass_cap_free", False) for v in pv.values())
    if all_slices_cap_free and both_pairs_pass:
        out["verdict"]["note"] = (
            "Cap-fixed sampler (Task Q water-filling, commit c4ef634): realized "
            "mu-bar tracks mu-bar within tolerance for BOTH gamma pairs at every "
            "mu-bar in (0,1) -- the gamma=0->+1 leg, previously all cap-affected/"
            "artifact-suspect on this grid, is now cap-free. Both adjacent-gamma "
            "pairs test C-Q4(i) cleanly and a_emp is strictly decreasing in gamma "
            "at every cap-free row (0 significant violations).")
    else:
        # Fall through: keep the inherited note but flag it as unverified rather
        # than silently asserting a cap-free claim the data did not support.
        out["verdict"]["note"] = (
            "AUTO-CHECK: not all pairs came out cap-free/passing on this run -- "
            "inherited note left in place below; re-inspect pair_verdicts. || "
            + out["verdict"]["note"])
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    # Critic obs O3: analyze_task_n.main() already print()ed the inherited STALE note
    # to stdout. Emit the corrected, data-derived note last so the final console output
    # a human sees matches the written artifact.
    print("\n[Task X corrected verdict.note]\n" + out["verdict"]["note"])


if __name__ == "__main__":
    main()
