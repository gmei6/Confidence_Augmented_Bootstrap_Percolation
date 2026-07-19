"""
Task X (Q4, C-Q4(ii)): size-biased collapse test on the CAP-FIXED sampler.

C-Q4(ii) predicts the size-biased mean fear mu_star(gamma) -- not the plain mean
mu_bar -- is the governing quantity for ignition: cells with MATCHED mu_star should
share the same ignition boundary a_c^emp regardless of gamma. Every prior test of
this was gated on the epsilon-cap sampler defect (Task Q); this re-runs it on the
merged water-filling sampler using the three q4_phase2_n10000_gamma*_capfix slices.

Method:
  - Per gamma slice, compute the empirical critical seed a_c^emp(mu_bar) via
    analyze_sweep (P=0.5 crossing), keeping only RESOLVED crossings (a_emp above the
    seed grid floor -- the D-021 clamping filter; clamped values are lower bounds).
  - Per (mu_bar, gamma), get the realized size-biased mean mu_star from the same
    deterministic cap diagnostic analyze_task_n uses (fixed degree sequence + fixed
    fear seed), which now calls the cap-fixed sampler.
  - Collapse metric: compare the spread of a_c^emp across gamma at MATCHED mu_star
    (curves re-expressed vs mu_star, interpolated onto a common mu_star grid) against
    the spread at MATCHED mu_bar (the un-collapsed baseline). If mu_star governs, the
    matched-mu_star spread should be materially smaller than the matched-mu_bar spread.

Read-only on the raws; writes results/processed/q4_size_biased_collapse_analysis.json.
"""

import os
import sys
import json
import datetime
import importlib.util

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash
from twocascade.analysis import analyze_sweep

# Reuse load_slices + cap_diagnostics from analyze_task_n (single source of truth
# for the deterministic mu_star diagnostic and the slice-pairing sanity checks).
spec = importlib.util.spec_from_file_location(
    "analyze_task_n", os.path.join(base_dir, "scripts", "analyze_task_n.py"))
analyze_task_n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze_task_n)

CAPFIX_CONFIGS = [
    "configs/q4_phase2_n10000_gammaneg1_capfix.json",
    "configs/q4_phase2_n10000_gamma0_capfix.json",
    "configs/q4_phase2_n10000_gammapos1_capfix.json",
]
OUTPUT_PATH = "results/processed/q4_size_biased_collapse_analysis.json"
CAP_TOL = 0.02  # relative realized-mu_bar shortfall tolerance (matches analyze_task_n)


def main():
    slices = analyze_task_n.load_slices(CAPFIX_CONFIGS)
    meta0 = slices[0]["raw"]["metadata"]
    theta = meta0["theta"]
    n = meta0["n"]
    tau = slices[0]["tau"]
    kappa = meta0["concentration"]
    sweep_params = slices[0]["raw"]["sweep_parameters"]
    mean_fear_grid = sweep_params["mean_fear_grid"]
    seed_size_grid = sweep_params["seed_size_grid"]
    grid_floor = float(seed_size_grid[0])
    gammas = [s["gamma"] for s in slices]

    # Deterministic mu_star / realized_mu_bar per (mu_bar, gamma) -- cap-fixed sampler.
    cap_diag = analyze_task_n.cap_diagnostics(slices, mean_fear_grid, n, tau, kappa=kappa)

    # a_c^emp(mu_bar) per gamma, resolved-crossings only.
    per_gamma = {}
    for s in slices:
        analyzed = analyze_sweep(s["raw"], theta=theta)
        thr = {}
        for mu_str, a_emp in analyzed["empirical_thresholds"].items():
            resolved = a_emp is not None and np.isfinite(a_emp) and a_emp > grid_floor
            thr[float(mu_str)] = float(a_emp) if resolved else None
        per_gamma[s["gamma"]] = thr

    # Build (mu_bar, mu_star, a_c^emp, realized_mu_bar, cap_free) points per gamma.
    points = {g: [] for g in gammas}
    for g in gammas:
        for mu in mean_fear_grid:
            if float(mu) == 0.0:
                continue  # clause scope is mu-bar in (0,1); gamma has no effect at mu=0
            diag = cap_diag["per_mu_gamma"][str(float(mu))][str(float(g))]
            a_emp = per_gamma[g].get(float(mu))
            cap_free = abs(diag["realized_mu_bar"] - float(mu)) / float(mu) <= CAP_TOL
            points[g].append({
                "mu_bar": float(mu),
                "mu_star": diag["realized_mu_star"],
                "realized_mu_bar": diag["realized_mu_bar"],
                "cap_free": bool(cap_free),
                "a_c_emp": a_emp,
                "resolved": a_emp is not None,
            })

    def spread_at_matched(xkey):
        """Mean across the common x-range of (max-min a_c^emp across gamma) after
        interpolating each gamma's a_c^emp(x) onto a shared grid. xkey in
        {'mu_bar','mu_star'}. Uses only resolved points."""
        curves = {}
        for g in gammas:
            xs, ys = [], []
            for p in points[g]:
                if p["resolved"]:
                    xs.append(p[xkey]); ys.append(p["a_c_emp"])
            if len(xs) >= 2:
                order = np.argsort(xs)
                curves[g] = (np.array(xs)[order], np.array(ys)[order])
        if len(curves) < 2:
            return None, None, curves
        lo = max(c[0].min() for c in curves.values())
        hi = min(c[0].max() for c in curves.values())
        if not (hi > lo):
            return None, None, curves  # no overlapping x-range across gamma
        xgrid = np.linspace(lo, hi, 25)
        stacked = np.array([np.interp(xgrid, c[0], c[1]) for c in curves.values()])
        spread = stacked.max(axis=0) - stacked.min(axis=0)
        return float(spread.mean()), float(spread.max()), curves

    mu_bar_spread_mean, mu_bar_spread_max, _ = spread_at_matched("mu_bar")
    mu_star_spread_mean, mu_star_spread_max, _ = spread_at_matched("mu_star")

    collapse = None
    if mu_bar_spread_mean is not None and mu_star_spread_mean is not None:
        ratio = mu_star_spread_mean / mu_bar_spread_mean if mu_bar_spread_mean > 0 else None
        # Reviewer finding #3: ratio is None means the mu_bar spread is degenerate (0), so
        # we cannot measure whether mu_star IMPROVES collapse -- that is "undetermined",
        # not a refutation. Only ratio >= 1 is a genuine "not supported".
        collapse_supported = None if ratio is None else bool(ratio < 1.0)
        collapse = {
            "matched_mu_bar_spread_mean": mu_bar_spread_mean,
            "matched_mu_bar_spread_max": mu_bar_spread_max,
            "matched_mu_star_spread_mean": mu_star_spread_mean,
            "matched_mu_star_spread_max": mu_star_spread_max,
            "spread_ratio_mustar_over_mubar": ratio,
            "collapse_supported": collapse_supported,
            "collapse_undetermined_reason": (
                None if ratio is not None else
                "matched-mu_bar spread is 0 (degenerate); cannot assess mu_star improvement"),
            "interpretation": (
                "C-Q4(ii) predicts a_c^emp collapses at matched mu_star -> "
                "spread_ratio < 1 means re-expressing vs mu_star tightens the "
                "gamma spread (supports mu_star as governing quantity); ratio >= 1 "
                "means mu_star does not collapse the boundary better than mu_bar."),
        }

    # Validation (Task Q fix): realized_mu_bar tracks mu_bar within CAP_TOL for gamma>0
    # cells that previously showed 7-28% shortfall -- checking realized_mu_bar, NOT
    # cap_hits (the verified invariant, per okf/next-actions.md item 5).
    mu_bar_tracking = {}
    for g in gammas:
        rows = []
        for p in points[g]:
            rows.append({"mu_bar": p["mu_bar"], "realized_mu_bar": p["realized_mu_bar"],
                         "rel_shortfall": abs(p["realized_mu_bar"] - p["mu_bar"]) / p["mu_bar"],
                         "cap_free": p["cap_free"]})
        mu_bar_tracking[str(g)] = {
            "cells": rows,
            "all_cap_free": all(r["cap_free"] for r in rows),
            "max_rel_shortfall": max(r["rel_shortfall"] for r in rows) if rows else 0.0,
        }

    out = {
        "metadata": {
            "task": "X (Q4 C-Q4(ii) size-biased collapse re-test on cap-fixed sampler)",
            "capfix_configs": CAPFIX_CONFIGS,
            "n": n, "tau": tau, "gammas": gammas, "cap_tol": CAP_TOL,
            "source_commits": {s["raw_file"]: s["raw"]["metadata"]["git_commit"] for s in slices},
            "analysis_runtime_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
        },
        "points_by_gamma": {str(g): points[g] for g in gammas},
        "collapse": collapse,
        "realized_mu_bar_tracking": mu_bar_tracking,
    }

    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")
    if collapse:
        print(f"matched-mu_bar spread mean = {collapse['matched_mu_bar_spread_mean']:.3f}, "
              f"matched-mu_star spread mean = {collapse['matched_mu_star_spread_mean']:.3f}, "
              f"ratio = {collapse['spread_ratio_mustar_over_mubar']}")
        print(f"collapse_supported: {collapse['collapse_supported']}")
    else:
        print("collapse metric: insufficient resolved/overlapping thresholds "
              "(reported per-gamma points for inspection)")
    for g in gammas:
        t = mu_bar_tracking[str(g)]
        print(f"gamma={g}: all_cap_free={t['all_cap_free']}, "
              f"max_rel_shortfall={t['max_rel_shortfall']:.4f}")


if __name__ == "__main__":
    main()
