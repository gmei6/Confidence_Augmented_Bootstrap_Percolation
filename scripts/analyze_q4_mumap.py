"""
Task V (Q4 C-Q4(iii) refinement): intermediate-mu_bar ignition map.

Every prior Q4 ignition run used only mu_bar in {0.0, 0.4}. This maps the full
mu_bar in {0.0, 0.1, 0.2, 0.3, 0.4} axis across the 5-point n-grid
{4000, 10000, 20000, 40000, 80000} on the tau = 2.5 configuration model at the
bounded seed (a = r = 2), to answer:
  (a) is ignition monotone increasing in mu_bar at each fixed n?
  (b) does the n-decline seen at mu_bar = 0.4 appear at ALL mu_bar > 0, or only
      near 0.4?
  (c) where is the crossover from "flat Theta(1)" to "declining"?

Reads results/q4_ignition_tau25_mumap_n{n}_raw.json via analyze_sweep and writes
results/processed/q4_mumap_analysis.json. Read-only on the raws; never hand-edits
results/. Cross-check: the mu_bar in {0.0, 0.4} columns reproduce the existing
results/q4_ignition_tau25_n{n}_raw.json cells exactly (same base_seed=42, same
per-n seed_multiple), so this script also reports whether those columns match.
"""

import os
import sys
import json
import datetime

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash
from twocascade.analysis import load_raw_results, analyze_sweep

N_GRID = [4000, 10000, 20000, 40000, 80000]
MU_GRID = [0.0, 0.1, 0.2, 0.3, 0.4]
TAU = 2.5
Z = 1.96
OUTPUT_PATH = "results/processed/q4_mumap_analysis.json"


def _wilson(k, trials):
    """Wilson 95% interval (robust at p = 0), matching analyze_q4_ignition.py."""
    ph = k / trials
    den = 1 + Z ** 2 / trials
    mid = (ph + Z ** 2 / (2 * trials)) / den
    hw = Z * np.sqrt(ph * (1 - ph) / trials + Z ** 2 / (4 * trials ** 2)) / den
    return float(mid - hw), float(mid + hw)


def main():
    cells = []
    source_commits = {}
    # p_grid[mu][n] -> p_systemic; k_grid[mu][n] -> n_systemic (for the cross-check).
    p_grid = {mu: {} for mu in MU_GRID}
    for n in N_GRID:
        raw_rel = f"results/q4_ignition_tau25_mumap_n{n}_raw.json"
        raw = load_raw_results(os.path.join(base_dir, raw_rel))
        source_commits[raw_rel] = raw["metadata"]["git_commit"]
        trials = raw["metadata"]["trials_per_cell"]
        for c in analyze_sweep(raw)["processed_cells"]:
            k = int(round(c["p_systemic"] * trials))
            lo, hi = _wilson(k, trials)
            mu = c["mean_fear"]
            cells.append({
                "tau": TAU,
                "n": n,
                "mean_fear": mu,
                "seed_size": c["seed_size"],
                "n_trials": trials,
                "n_systemic": k,
                "p_systemic": c["p_systemic"],
                "wilson_95": [lo, hi],
                "raw_file": raw_rel,
            })
            # round the float key to the grid to avoid float-key drift (lessons.md)
            mu_key = min(MU_GRID, key=lambda g: abs(g - mu))
            p_grid[mu_key][n] = c["p_systemic"]

    # Per-mu_bar series: n-trend direction (reusing analyze_q4_ignition's logic).
    series = {}
    for mu in MU_GRID:
        rows = sorted(p_grid[mu].items())  # (n, p) sorted by n
        ps = [p for _, p in rows]
        series[f"mu={mu}"] = {
            "mean_fear": mu,
            "p_by_n": {str(n): p for n, p in rows},
            "direction": ("all-zero" if all(p == 0 for p in ps)
                          else "increasing" if ps == sorted(ps) and ps[0] < ps[-1]
                          else "decreasing" if ps == sorted(ps, reverse=True) and ps[0] > ps[-1]
                          else "non-monotone"),
        }

    # (a) monotone-increasing-in-mu at each fixed n?
    mono_in_mu = {}
    for n in N_GRID:
        col = [p_grid[mu][n] for mu in MU_GRID]
        mono_in_mu[str(n)] = {
            "p_by_mu": {str(mu): p_grid[mu][n] for mu in MU_GRID},
            "monotone_increasing": col == sorted(col),
        }

    # Cross-check vs the existing (non-mumap) raws. NOTE on the RNG mechanism:
    # run_sweep (src/twocascade/runner.py:280-326) spawns child seeds in a flat
    # sequence assigned cell-by-cell in (mean_fear, seed_multiple) grid order.
    # mu=0.0 is the FIRST mean_fear value in both the old [0.0,0.4] grid and the
    # new [0.0,0.1,0.2,0.3,0.4] grid, so it gets the same child seeds and must
    # reproduce EXACTLY -- that is the real wiring check (correct base_seed,
    # config, seed_multiples). mu=0.4 moved from grid position 2 to position 5,
    # so it draws a DIFFERENT (independent) RNG stream; it therefore should NOT
    # match to the trial, and instead is an independent REPLICATION that should
    # agree within Monte Carlo error. (The task file's claim that both columns
    # reproduce exactly was based on a misread of this sequential spawning.)
    cross_check = {}
    for n in N_GRID:
        ref_rel = f"results/q4_ignition_tau25_n{n}_raw.json"
        ref = load_raw_results(os.path.join(base_dir, ref_rel))
        trials = ref["metadata"]["trials_per_cell"]
        ref_p = {round(c["mean_fear"], 4): c["p_systemic"]
                 for c in analyze_sweep(ref)["processed_cells"]}
        # mu=0.0: must reproduce exactly.
        new0, old0 = p_grid[0.0][n], ref_p.get(0.0)
        # mu=0.4: independent stream -> agreement within MC error (combined SE).
        new4, old4 = p_grid[0.4][n], ref_p.get(round(0.4, 4))
        se_comb = np.sqrt(max(new4 * (1 - new4), 1e-9) / trials
                          + max(old4 * (1 - old4), 1e-9) / trials)
        z4 = abs(new4 - old4) / se_comb if se_comb > 0 else 0.0
        cross_check[str(n)] = {
            "0.0": {"new": new0, "existing": old0,
                    "exact_match": old0 is not None and new0 == old0},
            "0.4": {"new": new4, "existing": old4,
                    "abs_diff": float(abs(new4 - old4)),
                    "combined_se": float(se_comb),
                    "z": float(z4),
                    "agrees_within_mc_error": bool(z4 <= 3.0)},
        }
    mu0_exact = all(cc["0.0"]["exact_match"] for cc in cross_check.values())
    mu4_within_mc = all(cc["0.4"]["agrees_within_mc_error"] for cc in cross_check.values())

    out = {
        "metadata": {
            "task": "V — Q4 intermediate-mu_bar ignition map (C-Q4(iii) refinement)",
            "tau": TAU,
            "n_grid": N_GRID,
            "mu_grid": MU_GRID,
            "source_commits": source_commits,
            "analysis_runtime_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
        },
        "cells": cells,
        "p_grid": {str(mu): {str(n): p_grid[mu][n] for n in N_GRID} for mu in MU_GRID},
        "series_by_mu": series,
        "monotone_in_mu_by_n": mono_in_mu,
        "cross_check_vs_existing_raws": cross_check,
        "cross_check_mu0_exact": bool(mu0_exact),
        "cross_check_mu04_within_mc_error": bool(mu4_within_mc),
    }

    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")
    print(f"cross_check mu=0.0 EXACT reproduction (wiring): {mu0_exact}")
    print(f"cross_check mu=0.4 independent-stream agreement within MC error: {mu4_within_mc} "
          f"(max z={max(cc['0.4']['z'] for cc in cross_check.values()):.2f})")
    print("P(systemic) grid [mu_bar x n]:")
    header = "  mu\\n  " + "".join(f"{n:>10d}" for n in N_GRID)
    print(header)
    for mu in MU_GRID:
        row = "".join(f"{p_grid[mu][n]:>10.3f}" for n in N_GRID)
        print(f"  {mu:<5} {row}   -> {series[f'mu={mu}']['direction']}")


if __name__ == "__main__":
    main()
