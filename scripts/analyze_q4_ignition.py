"""
Q4 ignition-gate analysis (C-Q4(iii)): bounded-seed (a = r = 2) ignition on
tau = 2.5 vs tau = 3.5 configuration models across n in {4000, 10000, 20000}.

C-Q4(iii) predicts: at tau = 2.5 (heavy tail) a bounded seed ignites systemic
cascades with probability Theta(1) (or growing in n); at tau = 3.5 (light
tail) bounded seeds must NOT ignite (P(systemic) -> 0 with n).

Reads the six results/q4_ignition_*_raw.json files via analyze_sweep and
writes results/processed/q4_ignition_analysis.json.
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

N_GRID = [4000, 10000, 20000]
TAUS = {"tau25": 2.5, "tau35": 3.5}
OUTPUT_PATH = "results/processed/q4_ignition_analysis.json"


def main():
    cells = []
    source_commits = {}
    for tag, tau in TAUS.items():
        for n in N_GRID:
            raw_rel = f"results/q4_ignition_{tag}_n{n}_raw.json"
            raw = load_raw_results(os.path.join(base_dir, raw_rel))
            source_commits[raw_rel] = raw["metadata"]["git_commit"]
            trials = raw["metadata"]["trials_per_cell"]
            for c in analyze_sweep(raw)["processed_cells"]:
                k = int(round(c["p_systemic"] * trials))
                # Wilson 95% interval: robust at p = 0 (tau = 3.5 cells).
                z = 1.96
                ph = k / trials
                den = 1 + z ** 2 / trials
                mid = (ph + z ** 2 / (2 * trials)) / den
                hw = z * np.sqrt(ph * (1 - ph) / trials + z ** 2 / (4 * trials ** 2)) / den
                cells.append({
                    "tau": tau,
                    "n": n,
                    "mean_fear": c["mean_fear"],
                    "seed_size": c["seed_size"],
                    "n_trials": trials,
                    "n_systemic": k,
                    "p_systemic": c["p_systemic"],
                    "wilson_95": [float(mid - hw), float(mid + hw)],
                    "raw_file": raw_rel,
                })

    # Gate check per (tau, mu) series across n.
    series = {}
    for tau in (2.5, 3.5):
        for mu in sorted({c["mean_fear"] for c in cells}):
            rows = sorted([c for c in cells if c["tau"] == tau and c["mean_fear"] == mu],
                          key=lambda c: c["n"])
            ps = [r["p_systemic"] for r in rows]
            series[f"tau={tau}|mu={mu}"] = {
                "tau": tau,
                "mean_fear": mu,
                "p_by_n": {str(r["n"]): r["p_systemic"] for r in rows},
                "total_systemic": sum(r["n_systemic"] for r in rows),
                "direction": ("all-zero" if all(p == 0 for p in ps)
                              else "increasing" if ps == sorted(ps) and ps[0] < ps[-1]
                              else "decreasing" if ps == sorted(ps, reverse=True) and ps[0] > ps[-1]
                              else "non-monotone"),
            }

    tau35_gate = all(s["total_systemic"] == 0 for s in series.values() if s["tau"] == 3.5)
    tau25_ignites = all(s["total_systemic"] > 0 for s in series.values() if s["tau"] == 2.5)
    verdict = {
        "clause": "C-Q4(iii) tail gating: bounded seed (a = r = 2) ignites at "
                  "tau = 2.5, must not ignite at tau = 3.5",
        "tau35_never_ignites": bool(tau35_gate),
        "tau25_ignites_at_bounded_seed": bool(tau25_ignites),
        "gate_holds": bool(tau35_gate and tau25_ignites),
        "note": "The tau = 2.5 vs 3.5 dichotomy is the gate; the n-direction of "
                "the tau = 2.5 branch is reported per series (Theta(1) requires "
                "non-vanishing P as n grows and is only bounded, not proven, by "
                "three n points).",
    }

    out = {
        "metadata": {
            "task": "Q4 ignition gates (C-Q4(iii) bounded-seed tail gating)",
            "n_grid": N_GRID,
            "taus": list(TAUS.values()),
            "source_commits": source_commits,
            "analysis_runtime_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
        },
        "cells": cells,
        "series": series,
        "verdict": verdict,
    }

    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")
    print(json.dumps(verdict, indent=2))
    for key, s in series.items():
        print(f"{key}: {s['p_by_n']} -> {s['direction']}")


if __name__ == "__main__":
    main()
