"""
Task N Phase 2 analysis (Q4, C-Q4(i)): tilt monotonicity at n = 10000.

Thin wrapper over scripts/analyze_task_n.py (S-047 handoff step 3): repoints
its PHASE1B_CONFIGS at the three configs/q4_phase2_n10000_gamma*.json slices
(same paired-seed design, base_seed = 42) and redirects the output so the
S-046 Phase 1b artifact (results/processed/task_n_tilt_analysis.json) is not
overwritten. The Phase 1 supercritical readout is replaced by a pointer note
(it is a Phase 1 finding and already recorded in the Phase 1b artifact).

Writes results/processed/task_n_phase2_n10000_analysis.json.
"""

import importlib.util
import json
import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

spec = importlib.util.spec_from_file_location(
    "analyze_task_n", os.path.join(base_dir, "scripts", "analyze_task_n.py"))
analyze_task_n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze_task_n)

OUTPUT_PATH = "results/processed/task_n_phase2_n10000_analysis.json"

analyze_task_n.PHASE1B_CONFIGS = [
    "configs/q4_phase2_n10000_gammaneg1.json",
    "configs/q4_phase2_n10000_gamma0.json",
    "configs/q4_phase2_n10000_gammapos1.json",
]
analyze_task_n.OUTPUT_PATH = OUTPUT_PATH
analyze_task_n.phase1_supercritical_readout = lambda: {
    "note": "Phase 1 supercritical readout lives in "
            "results/processed/task_n_tilt_analysis.json (S-046); "
            "not restated in this Phase 2 artifact."
}


def main():
    analyze_task_n.main()
    # Relabel the artifact's task stamp: the shared machinery labels itself
    # Phase 1b, but this run analyzes the Phase 2 n = 10000 slices.
    out_path = os.path.join(base_dir, OUTPUT_PATH)
    with open(out_path) as f:
        out = json.load(f)
    out["metadata"]["task"] = "N Phase 2 (Q4 tilt monotonicity at n = 10000, C-Q4(i))"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
