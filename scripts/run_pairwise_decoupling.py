#!/usr/bin/env python3
"""
Pairwise Decoupling Analysis (t=3) — Standalone Script with Provenance
======================================================================

Runs the same Tier 1 (variance ratio) and Tier 2 (pairwise covariance)
analyses as tests/test_pairwise_decoupling.py at round t=3, but saves
structured JSON output with provenance metadata (config + seed + git commit hash).

Output goes to stdout and optionally to a JSON file via --output.
Does NOT write to results/raw/ or results/figures/ (per §3.2 of
LESSONS_LEARNED).

Usage:
    python scripts/run_pairwise_decoupling.py
    python scripts/run_pairwise_decoupling.py --output decoupling.json
    python scripts/run_pairwise_decoupling.py --m-trials 500   # quick run
"""

import argparse
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np

from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)
from twocascade.model import calculate_beta, calculate_p_n, janson_a_c


# ──────────────────────────────────────────────────────────────────────
# Provenance
# ──────────────────────────────────────────────────────────────────────
def _git_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=os.path.join(os.path.dirname(__file__), ".."),
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "unknown"


# ──────────────────────────────────────────────────────────────────────
# Core helpers
# ──────────────────────────────────────────────────────────────────────
def _combined_a_c(n, p, r, mu):
    return janson_a_c(n, p, r) * (1.0 - mu) ** (r / (r - 1))


def _variance_ratio(s_t, seed_size, n):
    n_eff = n - seed_size
    pi_hat = float(np.mean(s_t - seed_size)) / n_eff
    if pi_hat <= 0.0 or pi_hat >= 1.0:
        return None, None, None, None
    var_s = float(np.var(s_t, ddof=1))
    binom = n_eff * pi_hat * (1.0 - pi_hat)
    return var_s / binom, n_eff * pi_hat, var_s, pi_hat


def _bootstrap_ci(s_t, seed_size, n, n_boot, rng):
    m = len(s_t)
    rs = []
    for _ in range(n_boot):
        idx = rng.choice(m, size=m, replace=True)
        r_b, *_ = _variance_ratio(s_t[idx], seed_size, n)
        if r_b is not None:
            rs.append(r_b)
    if len(rs) < n_boot // 2:
        return None, None
    arr = np.array(rs)
    return float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))


def _run_trials_t3(n, p, mu, seed_size, m, kappa, r, t_target, rng):
    out = np.empty(m, dtype=int)
    for i in range(m):
        adj = sample_gnp_adjacency(n, p, rng)
        fears = sample_individual_fears(n, mu, kappa, rng)
        nodes = make_nodes(fears)
        seed = choose_seed(n, seed_size, adj, rng, target_high_degree=False)
        res = run_cascade(adj, nodes, r, seed, rng, record_history=True)
        out[i] = res.history[min(t_target, len(res.history) - 1)]
    return out


def _distant_pairs(adjacency, seed_set, k, rng):
    n = len(adjacency)
    non_seed = [i for i in range(n) if i not in seed_set]
    nbr = {i: set(adjacency[i]) for i in non_seed}
    pairs, seen = [], set()
    for _ in range(k * 200):
        if len(pairs) >= k:
            break
        ab = rng.choice(len(non_seed), size=2, replace=False)
        i, j = non_seed[ab[0]], non_seed[ab[1]]
        key = (min(i, j), max(i, j))
        if key not in seen and not (nbr[i] & nbr[j]):
            pairs.append(key)
            seen.add(key)
    return pairs


def _safe(v):
    """Make a value JSON-serializable."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    return v


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description="Pairwise decoupling analysis with provenance.")
    ap.add_argument("--output", type=str, default=None,
                    help="Save JSON results to this path")
    ap.add_argument("--m-trials", type=int, default=2000,
                    help="Monte Carlo trials per cell (default 2000)")
    ap.add_argument("--seed", type=int, default=42,
                    help="Base RNG seed (default 42)")
    args = ap.parse_args()

    # ── Config ──
    r = 2
    alpha = 0.7
    tmd = 8.0
    n_ref = 1000
    kappa = 50.0
    theta = 0.5
    m = args.m_trials
    n_vals = [1000, 2000, 4000, 8000]
    mu_vals = [0.0, 0.3, 0.5]
    mu_t2 = [0.3, 0.5]
    n_boot = 1000
    n_graphs = 5
    k_pairs = 30
    t_target = 3

    beta = calculate_beta(tmd, n_ref, alpha)
    ss = np.random.SeedSequence(args.seed)
    rng_a, rng_b, rng_2 = [np.random.default_rng(s) for s in ss.spawn(3)]

    provenance = dict(git_hash=_git_hash(),
                      timestamp=datetime.now(timezone.utc).isoformat(),
                      base_seed=args.seed, m_trials=m,
                      n_values=n_vals, mu_values=mu_vals,
                      r=r, alpha=alpha, target_mean_degree=tmd,
                      n_ref=n_ref, kappa=kappa, theta_systemic=theta,
                      t_target=t_target)
    out = dict(provenance=provenance,
               tier1_subcritical=[], tier1_near_critical=[],
               tier2_pairwise=[])

    # ── Tier 1a ──
    print(f"\n=== TIER 1a: Variance Ratio  ·  0.8 × a_c  [subcritical, t={t_target}] ===")
    for n in n_vals:
        p = calculate_p_n(beta, n, alpha)
        for mu in mu_vals:
            ac = _combined_a_c(n, p, r, mu)
            a = max(r, math.ceil(0.8 * ac))
            s_t = _run_trials_t3(n, p, mu, a, m, kappa, r, t_target, rng_a)
            R, lam, var_s, pi = _variance_ratio(s_t, a, n)
            lo, hi = _bootstrap_ci(s_t, a, n, n_boot, rng_a)
            row = dict(n=n, mu=mu, a=a, R=_safe(R), lam=_safe(lam),
                       var=_safe(var_s), pi_hat=_safe(pi),
                       ci_lo=_safe(lo), ci_hi=_safe(hi), m_eff=len(s_t))
            out["tier1_subcritical"].append(row)
            if R is not None:
                print(f"  n={n:>5}  μ={mu:.1f}  a={a:>4}  π̂={pi:.5f}  "
                      f"λ={lam:>7.1f}  R={R:.3f}  "
                      f"CI=[{lo:.3f},{hi:.3f}]")
            else:
                print(f"  n={n:>5}  μ={mu:.1f}  a={a:>4}  — degenerate —")

    # ── Tier 1b ──
    print(f"\n=== TIER 1b: Variance Ratio  ·  1.1 × a_c  [near-critical, t={t_target}] ===")
    for n in n_vals:
        p = calculate_p_n(beta, n, alpha)
        for mu in mu_vals:
            ac = _combined_a_c(n, p, r, mu)
            a = max(r, math.ceil(1.1 * ac))
            s_t = _run_trials_t3(n, p, mu, a, m, kappa, r, t_target, rng_b)
            R, lam, var_s, pi = _variance_ratio(s_t, a, n)
            lo, hi = _bootstrap_ci(s_t, a, n, n_boot, rng_b)
            row = dict(n=n, mu=mu, a=a, R=_safe(R), lam=_safe(lam),
                       var=_safe(var_s), pi_hat=_safe(pi),
                       ci_lo=_safe(lo), ci_hi=_safe(hi), m_eff=len(s_t))
            out["tier1_near_critical"].append(row)
            if R is not None:
                print(f"  n={n:>5}  μ={mu:.1f}  a={a:>4}  π̂={pi:.5f}  "
                      f"λ={lam:>7.1f}  R={R:.3f}  "
                      f"CI=[{lo:.3f},{hi:.3f}]")
            else:
                print(f"  n={n:>5}  μ={mu:.1f}  a={a:>4}  — degenerate —")

    # ── Tier 2 ──
    print(f"\n=== TIER 2: Pairwise ΔCov  ·  {n_graphs} graphs × "
          f"{k_pairs} pairs  [diagnostic, t={t_target}] ===")
    se = 1.0 / math.sqrt(m)
    print(f"  SE ≈ {se:.4f} — cannot resolve O(1/n)")
    
    max_cov_all_cells = 0.0
    max_graph_blowup_all_cells = 0.0
    
    for n in n_vals:
        p = calculate_p_n(beta, n, alpha)
        for mu in mu_t2:
            ac = _combined_a_c(n, p, r, mu)
            seed_size = max(r, math.ceil(0.8 * ac))
            all_covs = []
            graph_blowups = []
            for _ in range(n_graphs):
                adj = sample_gnp_adjacency(n, p, rng_2)
                si = choose_seed(n, seed_size, adj, rng_2,
                                 target_high_degree=False)
                sset = set(si)
                pairs = _distant_pairs(adj, sset, k_pairs, rng_2)
                if len(pairs) < 5:
                    continue
                watched = set()
                for ii, jj in pairs:
                    watched.add(ii)
                    watched.add(jj)
                ind = {v: np.empty(m) for v in watched}
                blowup_count = 0
                for t in range(m):
                    fears = sample_individual_fears(n, mu, kappa, rng_2)
                    nodes = make_nodes(fears)
                    res = run_cascade(adj, nodes, r, list(si), rng_2,
                                record_history=False, track_nodes=watched)
                    
                    # Extract 1{Y_v <= 3} indicator
                    for v in watched:
                        failed_by_t3 = (v in res.tracked_failure_rounds) and (res.tracked_failure_rounds[v] <= t_target)
                        ind[v][t] = float(failed_by_t3)
                    
                    if res.total_failed >= (theta * n):
                        blowup_count += 1
                
                blowup_rate = blowup_count / m
                graph_blowups.append(blowup_rate)

                for ii, jj in pairs:
                    xi = ind[ii]
                    xj = ind[jj]
                    cov = float(np.mean(xi * xj)
                                - np.mean(xi) * np.mean(xj))
                    all_covs.append(abs(cov))

            mean_blowup = float(np.mean(graph_blowups)) if graph_blowups else 0.0
            max_cell_graph_blowup = float(np.max(graph_blowups)) if graph_blowups else 0.0
            max_graph_blowup_all_cells = max(max_graph_blowup_all_cells, max_cell_graph_blowup)
            cell_max_cov = float(np.max(all_covs)) if all_covs else 0.0
            max_cov_all_cells = max(max_cov_all_cells, cell_max_cov)
            
            row = dict(n=n, mu=mu, n_pairs=len(all_covs),
                       mean_abs_cov=_safe(np.mean(all_covs)
                                         if all_covs else None),
                       max_abs_cov=_safe(np.max(all_covs)
                                        if all_covs else None),
                       mean_blowup=mean_blowup)
            out["tier2_pairwise"].append(row)
            if all_covs:
                print(f"  n={n:>5}  μ={mu:.1f}  pairs={len(all_covs):>4}"
                      f"  mean|Cov|={np.mean(all_covs):.6f}"
                      f"  max|Cov|={np.max(all_covs):.6f}"
                      f"  mean_blow={mean_blowup:.3f}")
            else:
                print(f"  n={n:>5}  μ={mu:.1f}  — no valid pairs —  mean_blow={mean_blowup:.3f}")

    # ── Script-level Sanity Warning (printed, not gated) ──
    print("\n=== SANITY CHECK WARNINGS ===")
    has_warning = False
    for n in n_vals:
        row = next((r for r in out["tier1_subcritical"] if r["n"] == n and r["mu"] == 0.0), None)
        if row and row["R"] is not None:
            R = row["R"]
            if not (1.0 < R < 6.0):
                has_warning = True
                print(f"  [WARNING] Tier 1: μ=0 sanity check failed at n={n}: R={R:.3f} "
                      f"(expected R ∈ [1.0, 6.0] at t=3 as an empirically-calibrated regression guard).")
    
    if max_cov_all_cells > 0.05:
        has_warning = True
        print(f"  [WARNING] Tier 2: Macroscopic subcritical pairwise correlation detected (max |Cov| = {max_cov_all_cells:.6f} > 0.05).")
    
    if max_graph_blowup_all_cells > 0.50:
        has_warning = True
        print(f"  [WARNING] Tier 2: Extreme single-graph blowup rate detected (max graph blowup = {max_graph_blowup_all_cells * 100:.1f}% > 50.0%).")
        
    if not has_warning:
        print("  All sanity checks passed (R ∈ [1.0, 6.0] and max |Cov| ≤ 0.05, max graph blowup ≤ 50.0%).")

    # ── Save ──
    if args.output:
        with open(args.output, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nResults saved to {args.output}")

    print("\nDone.")


if __name__ == "__main__":
    main()
