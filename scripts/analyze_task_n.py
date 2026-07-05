"""
Task N (Q4) Phase 1 analysis: C-Q4(i) tilt monotonicity on the configuration model.

Loads the three paired gamma slices of the Phase 1 sweep (tau=2.5, n=4000,
base_seed=42, shared graph streams), computes P(systemic) per cell and the
empirical critical seed a_c^emp per mean fear, and evaluates C-Q4(i):
at fixed mu-bar and tau, a_c^emp is strictly decreasing in gamma.

Trials are paired across gamma runs (identical SeedSequence spawn order), so
per-cell differences in the systemic indicator use the paired standard error.

Writes results/processed/task_n_tilt_analysis.json. Figure generation is
separate (scripts/plot_task_n.py) and only reads this artifact.
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
from twocascade.graphs import sample_powerlaw_degrees, sample_degree_dependent_fears

# gamma slice -> (config, raw output) pairing; gamma is read from each config
# rather than hardcoded so the analysis stamp reflects the actual run configs.
#
# Phase 1 (seed grid 260-781, multiples of the G(n,p) Janson a_c) turned out
# entirely supercritical on the tau=2.5 configuration model, so it is recorded
# here only as a supercritical readout; Phase 1b (a in {2..32}, where the pilot
# located the transition) carries the C-Q4(i) evaluation.
PHASE1_CONFIGS = [
    "configs/q4_phase1_gamma_neg1.json",
    "configs/q4_phase1_gamma0.json",
    "configs/q4_phase1.json",
]
PHASE1B_CONFIGS = [
    "configs/q4_phase1b_gammaneg1.json",
    "configs/q4_phase1b_gamma0.json",
    "configs/q4_phase1b_gammapos1.json",
]

OUTPUT_PATH = "results/processed/task_n_tilt_analysis.json"


def load_slices(slice_configs):
    """Load (gamma, config_path, raw_path, raw_data) for each slice, sorted by gamma."""
    slices = []
    for cfg_rel in slice_configs:
        cfg_path = os.path.join(base_dir, cfg_rel)
        with open(cfg_path) as f:
            cfg = json.load(f)
        gamma = cfg["pinned_params"]["fear"]["gamma"]
        raw_rel = cfg["output"]["raw_filepath"]
        raw = load_raw_results(os.path.join(base_dir, raw_rel))
        slices.append({
            "gamma": float(gamma),
            "config": cfg_rel,
            "raw_file": raw_rel,
            "raw": raw,
            "tau": cfg["pinned_params"]["graph"]["tau"],
            "base_seed": cfg["sweep"]["base_seed"],
        })
    slices.sort(key=lambda s: s["gamma"])

    # Pairing sanity: identical sweep axes and base seed across slices.
    ref = slices[0]
    for s in slices[1:]:
        assert s["base_seed"] == ref["base_seed"], "base_seed mismatch breaks pairing"
        assert s["raw"]["sweep_parameters"] == ref["raw"]["sweep_parameters"], \
            "sweep grids differ; slices are not cell-aligned"
    return slices


def indicator_grid(raw, theta):
    """Return {(mean_fear_idx, seed_multiple_idx): np.ndarray of systemic indicators}."""
    grid = {}
    for cell in raw["results"]:
        key = (cell["mean_fear_idx"], cell["seed_multiple_idx"])
        ffs = np.asarray(cell["failed_fractions"])
        grid[key] = (ffs >= theta).astype(float)
    return grid


def paired_comparison(lo, hi, theta):
    """Per-cell paired difference P_hi - P_lo of systemic indicators (hi gamma minus lo)."""
    g_lo = indicator_grid(lo["raw"], theta)
    g_hi = indicator_grid(hi["raw"], theta)
    rows = []
    for key in sorted(g_lo):
        d = g_hi[key] - g_lo[key]
        n_tr = len(d)
        mean = float(np.mean(d))
        se = float(np.std(d, ddof=1) / np.sqrt(n_tr)) if n_tr > 1 else float("nan")
        rows.append({
            "mean_fear_idx": key[0],
            "seed_multiple_idx": key[1],
            "delta_p": mean,
            "paired_se": se,
            "z": mean / se if se and se > 0 else 0.0,
            "n_trials": n_tr,
        })
    return rows


def cap_diagnostics(slices, mean_fear_grid, n, tau, d_min=2, kappa=50,
                    diag_seed_graph=7, diag_seed_fear=11):
    """
    Deterministic ε-cap diagnostic (scoping doc §7 early-warning): on one fixed
    degree sequence, measure cap hits, realized mu-bar, and realized size-biased
    mu-star per (mu, gamma). A realized mu-bar well below nominal means the
    equal-total-fear premise of C-Q4(i) is violated for that cell.
    """
    rng = np.random.default_rng(diag_seed_graph)
    degrees = sample_powerlaw_degrees(n, tau, d_min, rng)
    diag = {"diag_seed_graph": diag_seed_graph, "diag_seed_fear": diag_seed_fear,
            "per_mu_gamma": {}}
    for mu in mean_fear_grid:
        row = {}
        for s in slices:
            g = s["gamma"]
            _, stats = sample_degree_dependent_fears(
                degrees, mu, g, kappa, np.random.default_rng(diag_seed_fear))
            row[str(g)] = {
                "cap_hits": int(stats["cap_hits"]),
                "cap_hit_fraction": stats["cap_hits"] / n,
                "realized_mu_bar": float(stats["realized_mu_bar"]),
                "realized_mu_star": float(stats["realized_mu_star"]),
            }
        diag["per_mu_gamma"][str(float(mu))] = row
    return diag


def phase1_supercritical_readout():
    """Summarize the Phase 1 grid: min P(systemic) over all cells per gamma."""
    slices = load_slices(PHASE1_CONFIGS)
    readout = {}
    for s in slices:
        analyzed = analyze_sweep(s["raw"])
        p_vals = [c["p_systemic"] for c in analyzed["processed_cells"]]
        readout[str(s["gamma"])] = {
            "raw_file": s["raw_file"],
            "n_cells": len(p_vals),
            "min_p_systemic": min(p_vals),
            "seed_grid": s["raw"]["sweep_parameters"]["seed_size_grid"],
        }
    return {
        "finding": "Phase 1 seed grid (Janson a_c multiples for the G(n,p)-matched "
                   "density) is entirely supercritical on the tau=2.5 configuration "
                   "model; the ignition transition sits at a in ~[2, 32], two orders "
                   "below the grid floor, so C-Q4(i) is not resolvable from Phase 1.",
        "per_gamma": readout,
    }


def main():
    slices = load_slices(PHASE1B_CONFIGS)
    meta0 = slices[0]["raw"]["metadata"]
    theta = meta0["theta"]
    sweep_params = slices[0]["raw"]["sweep_parameters"]
    mean_fear_grid = sweep_params["mean_fear_grid"]
    seed_size_grid = sweep_params["seed_size_grid"]
    grid_floor = float(seed_size_grid[0])

    # Empirical thresholds per gamma, with the D-021 clamping filter:
    # a crossing at the grid floor is a clamped lower bound, not a resolved crossing.
    thresholds = {}
    p_systemic = {}
    for s in slices:
        analyzed = analyze_sweep(s["raw"], theta=theta)
        thr = {}
        for mu_str, a_emp in analyzed["empirical_thresholds"].items():
            resolved = a_emp is not None and np.isfinite(a_emp) and a_emp > grid_floor
            thr[mu_str] = {
                "a_emp": None if a_emp is None or not np.isfinite(a_emp) else float(a_emp),
                "resolved": bool(resolved),
                "note": None if resolved else (
                    "no crossing in seed grid" if a_emp is None or not np.isfinite(a_emp)
                    else "clamped at grid floor (lower bound only)"
                ),
            }
        thresholds[str(s["gamma"])] = thr
        p_systemic[str(s["gamma"])] = {
            f"{c['mean_fear']}|{c['seed_multiple']}": c["p_systemic"]
            for c in analyzed["processed_cells"]
        }

    # Paired per-cell comparisons for adjacent gamma pairs (increasing gamma).
    comparisons = {}
    for lo, hi in zip(slices, slices[1:]):
        comparisons[f"{hi['gamma']}_vs_{lo['gamma']}"] = paired_comparison(lo, hi, theta)

    # ε-cap diagnostics: cells where the cap materially compresses the realized
    # mean fear are not equal-total-fear comparisons and cannot refute C-Q4(i).
    cap_diag = cap_diagnostics(slices, mean_fear_grid, meta0["n"], slices[0]["tau"],
                               kappa=meta0["concentration"])
    CAP_TOL = 0.02  # relative shortfall of realized mu-bar vs nominal

    def gamma_is_cap_free(mu, gamma):
        if float(mu) == 0.0:
            return True
        v = cap_diag["per_mu_gamma"][str(float(mu))][str(float(gamma))]
        return abs(v["realized_mu_bar"] - float(mu)) / float(mu) <= CAP_TOL

    def mu_is_cap_free(mu):
        row = cap_diag["per_mu_gamma"][str(float(mu))]
        return all(gamma_is_cap_free(mu, g) for g in row)

    # C-Q4(i) verdict on resolved thresholds: a_c^emp strictly decreasing in gamma,
    # and per-cell paired P(systemic) not decreasing in gamma beyond MC error (|z| > 2).
    # The clause is stated for mu-bar in (0,1), so mu=0 rows (where gamma provably
    # has no effect) are excluded from the verdict, and cap-affected rows are
    # reported separately as artifact-suspect rather than counted as refutations.
    gammas = [s["gamma"] for s in slices]
    threshold_ordering = []
    for mu in mean_fear_grid:
        vals = []
        for g in gammas:
            t = thresholds[str(g)][str(float(mu))]
            vals.append(t["a_emp"] if t["resolved"] else None)
        if all(v is not None for v in vals):
            monotone = all(vals[k] > vals[k + 1] for k in range(len(vals) - 1))
        else:
            monotone = None  # not resolvable at this mu
        threshold_ordering.append({
            "mean_fear": mu,
            "a_emp_by_gamma": dict(zip(map(str, gammas), vals)),
            "strictly_decreasing_in_gamma": monotone,
            "in_clause_scope": float(mu) > 0.0,
            "cap_free": mu_is_cap_free(mu),
        })

    violations = []
    for pair, rows in comparisons.items():
        for row in rows:
            if row["z"] < -2.0:  # higher gamma significantly LESS systemic
                mu = mean_fear_grid[row["mean_fear_idx"]]
                violations.append({"pair": pair, "cap_free": mu_is_cap_free(mu),
                                   **{k: row[k] for k in
                                      ("mean_fear_idx", "seed_multiple_idx", "delta_p", "z")}})

    # Per-adjacent-pair verdicts: a pair tests C-Q4(i) cleanly at mu only when
    # BOTH its gamma slices are cap-free there (equal-total-fear premise intact).
    pair_verdicts = {}
    for lo, hi in zip(slices, slices[1:]):
        g_lo, g_hi = lo["gamma"], hi["gamma"]
        pair = f"{g_hi}_vs_{g_lo}"
        rows = []
        for mu in mean_fear_grid:
            if float(mu) == 0.0:
                continue  # clause scope is mu-bar in (0,1)
            t_lo = thresholds[str(g_lo)][str(float(mu))]
            t_hi = thresholds[str(g_hi)][str(float(mu))]
            if not (t_lo["resolved"] and t_hi["resolved"]):
                continue
            rows.append({
                "mean_fear": mu,
                "cap_free": gamma_is_cap_free(mu, g_lo) and gamma_is_cap_free(mu, g_hi),
                "a_emp_decreasing": t_hi["a_emp"] < t_lo["a_emp"],
            })
        pair_viol = [v for v in violations if v["pair"] == pair]
        clean = [r for r in rows if r["cap_free"]]
        clean_viol = [v for v in pair_viol
                      if gamma_is_cap_free(mean_fear_grid[v["mean_fear_idx"]], g_lo)
                      and gamma_is_cap_free(mean_fear_grid[v["mean_fear_idx"]], g_hi)]
        pair_verdicts[pair] = {
            "cap_free_mu_rows": len(clean),
            "cap_free_rows_a_emp_decreasing": sum(1 for r in clean if r["a_emp_decreasing"]),
            "cap_free_cells_significantly_violating": len(clean_viol),
            "cap_affected_mu_rows": len(rows) - len(clean),
            "cap_affected_cells_significantly_violating": len(pair_viol) - len(clean_viol),
            "pass_cap_free": bool(clean) and all(r["a_emp_decreasing"] for r in clean)
                             and not clean_viol,
            "rows": rows,
        }

    verdict = {
        "clause": "C-Q4(i) tilt monotonicity (mu-bar in (0,1); per adjacent gamma pair)",
        "pair_verdicts": pair_verdicts,
        "note": "Cap-affected rows (realized mu-bar shortfall > 2% for either slice "
                "of the pair) violate the equal-total-fear premise (scoping §7 "
                "early-warning) and are reported as artifact-suspect, not refutations. "
                "At tau=2.5 the gamma=+1 slice is cap-affected at every mu-bar >= 0.1, "
                "so only the (-1, 0) pair tests the clause cleanly on this grid.",
    }

    out = {
        "metadata": {
            "task": "N (Q4 Phase 1b tilt monotonicity, C-Q4(i))",
            "n": meta0["n"],
            "r": meta0["r"],
            "tau": slices[0]["tau"],
            "theta": theta,
            "concentration": meta0["concentration"],
            "trials_per_cell": meta0["trials_per_cell"],
            "base_seed": slices[0]["base_seed"],
            "gammas": gammas,
            "source_configs": [s["config"] for s in slices],
            "source_raw_files": [s["raw_file"] for s in slices],
            "source_commits": {str(s["gamma"]): s["raw"]["metadata"]["git_commit"] for s in slices},
            "analysis_runtime_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "grid_floor": grid_floor,
        },
        "sweep_parameters": sweep_params,
        "empirical_thresholds_by_gamma": thresholds,
        "p_systemic_by_gamma": p_systemic,
        "paired_comparisons": comparisons,
        "threshold_ordering": threshold_ordering,
        "violations": violations,
        "cap_diagnostics": cap_diag,
        "verdict": verdict,
        "phase1_supercritical_readout": phase1_supercritical_readout(),
    }

    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")
    print(json.dumps(verdict, indent=2))
    for row in threshold_ordering:
        print(row["mean_fear"], row["a_emp_by_gamma"], row["strictly_decreasing_in_gamma"])


if __name__ == "__main__":
    main()
