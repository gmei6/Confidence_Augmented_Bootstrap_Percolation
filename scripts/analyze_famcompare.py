"""Analyze the Fear Amplifies cross-family comparison (CM vs GIRG vs ER).

Reads raw sweep outputs (never writes them -- the runner owns results/*_raw.json)
and produces results/processed/famcompare_analysis.json, the single artifact
scripts/plot_famcompare_ratio.py reads to draw the figure.

Families / arms, on the shared n grid {4000, 10000, 20000}:
  - configuration_model : REUSES the existing q4_ignition_tau25_mumap_n{n}_raw.json
                           series (bounded seed a=r=2, mu_bar in [0, 0.1, 0.2, 0.3, 0.4],
                           500 trials/cell). No new compute.
  - girg                : results/famcompare_girg_n{n}_raw.json -- same bounded-seed
                           methodology, per-n w_min calibrated to match the CM family's
                           realised mean degree at that n (task C2/C3b lineage).
  - erdos_renyi_matched : results/famcompare_er_matched_n{n}_raw.json -- ER's OWN seed
                           chosen so P(systemic | mu_bar=0) ~ 0.03, i.e. comparable to
                           where CM/GIRG sit at their bounded seed a=2 (Gary's
                           matched-baseline anchor decision, 2026-08-03). This is the
                           arm that goes in the main ratio panel alongside CM/GIRG.
  - erdos_renyi_bounded : results/famcompare_er_bounded_n{n}_raw.json -- ER at the SAME
                           absolute bounded seed a=r=2 as CM/GIRG. All-zero ignition by
                           construction (ER's a_c is ~250-475 at these n) -- shown as an
                           annotated flat-zero strip, never as a fake ratio.
  - erdos_renyi_a05     : results/famcompare_er_scaled_n{n}_raw.json -- SUPPLEMENTARY,
                           NOT in the main panel. ER at its own a05(mu_bar=0) crossing
                           (baseline ~0.5), so the ratio is arithmetically ceiling-capped
                           at ~2x and cannot show the same dynamic range as the
                           matched-baseline arm. Kept for the appendix/footnote only.

Ratio CI method: parametric bootstrap on the two independent binomial proportions
(10000 resamples), NOT the delta-method log-ratio the prototype used. For each
resample, k1* ~ Binomial(n1, p1_hat) and k0* ~ Binomial(n0, p0_hat) are drawn
independently; the resample is dropped (and the drop rate recorded) on the rare
draw where k0* == 0, since the ratio is undefined there -- a Haldane-Anscombe-style
issue that in practice affects a negligible fraction of draws at these p0_hat/n
(all p0_hat >= 0.014, so P(k0*=0) < 1e-3 in the worst case here). The reported CI is
the empirical 2.5/97.5 percentile of the surviving resampled ratios.

n-availability is checked at run time, not assumed: a family/n cell is included
only if its raw file exists AND has the expected 5 mu_bar cells at 500 trials each.
If GIRG's n=20000 arm has not landed yet, the analysis (and the figure it feeds)
silently runs on whatever n's are complete and records which were skipped and why
in metadata.n_grid_used / metadata.skipped -- this is deliberate (poster-deadline
fallback: n in {4000, 10000} ships without blocking on the multi-hour n=20000 arm).

Usage:
    arch -arm64 python3 scripts/analyze_famcompare.py
"""
import datetime
import json
import os
import subprocess
import sys

import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

N_GRID = [4000, 10000, 20000]
MU_GRID = [0.0, 0.1, 0.2, 0.3, 0.4]
EXPECTED_TRIALS = 500
BOOTSTRAP_DRAWS = 10000
BOOTSTRAP_SEED = 20260803


def git_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def raw_commit(raw):
    return raw.get("metadata", {}).get("git_commit", "unknown")


def load_raw(path):
    full = os.path.join(REPO_ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full) as f:
        return json.load(f)


def cells_from_raw(raw, theta):
    """dict mapping mean_fear (float) -> (n_trials, n_systemic, p_systemic)."""
    out = {}
    for r in raw["results"]:
        ff = r["failed_fractions"]
        n_trials = len(ff)
        n_systemic = sum(1 for x in ff if x >= theta)
        out[round(r["mean_fear"], 6)] = {
            "seed_size": r["seed_size"],
            "n_trials": n_trials,
            "n_systemic": n_systemic,
            "p_systemic": n_systemic / n_trials if n_trials else float("nan"),
        }
    return out


def validate_complete(cells, mu_grid=MU_GRID, expected_trials=EXPECTED_TRIALS):
    for mu in mu_grid:
        c = cells.get(round(mu, 6))
        if c is None or c["n_trials"] != expected_trials:
            return False
    return True


def bootstrap_ratio_ci(k1, n1, k0, n0, rng, draws=BOOTSTRAP_DRAWS):
    """Parametric bootstrap 95% CI on the ratio p1/p0 of two independent binomials.

    Returns (point_ratio, ci_lo, ci_hi, drop_fraction). point_ratio is the plain
    k1/n1 / (k0/n0) estimate (not the bootstrap mean, to keep the point estimate
    simple and standard); the CI comes from the bootstrap distribution.
    """
    p1_hat, p0_hat = k1 / n1, k0 / n0
    point = p1_hat / p0_hat if p0_hat > 0 else float("inf")

    k1_star = rng.binomial(n1, p1_hat, size=draws)
    k0_star = rng.binomial(n0, p0_hat, size=draws)
    valid = k0_star > 0
    drop_fraction = float(1.0 - valid.mean())
    ratios = (k1_star[valid] / n1) / (k0_star[valid] / n0)
    ci_lo, ci_hi = np.percentile(ratios, [2.5, 97.5])
    return point, float(ci_lo), float(ci_hi), drop_fraction


def build_family(name, raw_paths, theta_by_n):
    """raw_paths: dict n -> repo-relative path. Returns (per_n_cells, source_commits, skipped)."""
    per_n = {}
    source_commits = {}
    skipped = {}
    for n, path in raw_paths.items():
        raw = load_raw(path)
        if raw is None:
            skipped[n] = f"raw file not found: {path}"
            continue
        cells = cells_from_raw(raw, theta_by_n[n])
        if not validate_complete(cells):
            skipped[n] = f"incomplete cells in {path}: {cells}"
            continue
        per_n[n] = cells
        source_commits[path] = raw_commit(raw)
    return per_n, source_commits, skipped


def main():
    os.chdir(REPO_ROOT)
    rng = np.random.default_rng(BOOTSTRAP_SEED)

    theta_by_n = {n: 0.5 for n in N_GRID}  # pinned_params.theta is 0.5 in every config used here

    cm_paths = {n: f"results/q4_ignition_tau25_mumap_n{n}_raw.json" for n in N_GRID}
    girg_paths = {n: f"results/famcompare_girg_n{n}_raw.json" for n in N_GRID}
    er_matched_paths = {n: f"results/famcompare_er_matched_n{n}_raw.json" for n in N_GRID}
    er_bounded_paths = {n: f"results/famcompare_er_bounded_n{n}_raw.json" for n in N_GRID}
    er_a05_paths = {n: f"results/famcompare_er_scaled_n{n}_raw.json" for n in N_GRID}

    cm_cells, cm_commits, cm_skip = build_family("configuration_model", cm_paths, theta_by_n)
    girg_cells, girg_commits, girg_skip = build_family("girg", girg_paths, theta_by_n)
    er_m_cells, er_m_commits, er_m_skip = build_family("erdos_renyi_matched", er_matched_paths, theta_by_n)
    er_b_cells, er_b_commits, er_b_skip = build_family("erdos_renyi_bounded", er_bounded_paths, theta_by_n)
    er_a05_cells, er_a05_commits, er_a05_skip = build_family("erdos_renyi_a05", er_a05_paths, theta_by_n)

    # n's usable in the MAIN ratio panel: need CM, GIRG, and ER-matched all complete at that n.
    n_grid_used = [n for n in N_GRID if n in cm_cells and n in girg_cells and n in er_m_cells]
    n_grid_skipped = {
        n: {
            "configuration_model": cm_skip.get(n),
            "girg": girg_skip.get(n),
            "erdos_renyi_matched": er_m_skip.get(n),
        }
        for n in N_GRID if n not in n_grid_used
    }

    def ratio_series(cells_by_n):
        out = {}
        for n in n_grid_used:
            cells = cells_by_n[n]
            base = cells[0.0]
            row = {}
            for mu in MU_GRID:
                if mu == 0.0:
                    continue
                c = cells[round(mu, 6)]
                point, lo, hi, drop = bootstrap_ratio_ci(
                    c["n_systemic"], c["n_trials"], base["n_systemic"], base["n_trials"], rng
                )
                row[f"{mu:g}"] = {
                    "ratio": point, "ci_lo": lo, "ci_hi": hi,
                    "bootstrap_drop_fraction": drop,
                    "numerator": {"n_systemic": c["n_systemic"], "n_trials": c["n_trials"], "p": c["p_systemic"]},
                    "denominator": {"n_systemic": base["n_systemic"], "n_trials": base["n_trials"], "p": base["p_systemic"]},
                    "ceiling_censored": c["p_systemic"] >= 0.999,
                }
            out[n] = {"baseline_p": base["p_systemic"], "baseline_seed": base["seed_size"], "by_mu": row}
        return out

    cm_ratios = ratio_series(cm_cells)
    girg_ratios = ratio_series(girg_cells)
    er_m_ratios = ratio_series(er_m_cells)

    # ER bounded (a=r=2): flat-zero strip, all n's where it's available (independent of n_grid_used).
    er_bounded_summary = {}
    for n, cells in er_b_cells.items():
        er_bounded_summary[n] = {mu: cells[round(mu, 6)]["p_systemic"] for mu in MU_GRID}

    # ER a05-anchored: supplementary only, same ratio treatment, own n-availability.
    n_grid_a05 = [n for n in N_GRID if n in er_a05_cells]
    er_a05_ratios = ratio_series({n: er_a05_cells[n] for n in n_grid_a05}) if n_grid_a05 else {}
    # ratio_series() closes over n_grid_used for the main arms; redo directly for a05 with its own n list.
    def ratio_series_for(cells_by_n, n_list):
        out = {}
        for n in n_list:
            cells = cells_by_n[n]
            base = cells[0.0]
            row = {}
            for mu in MU_GRID:
                if mu == 0.0:
                    continue
                c = cells[round(mu, 6)]
                point, lo, hi, drop = bootstrap_ratio_ci(
                    c["n_systemic"], c["n_trials"], base["n_systemic"], base["n_trials"], rng
                )
                row[f"{mu:g}"] = {
                    "ratio": point, "ci_lo": lo, "ci_hi": hi,
                    "bootstrap_drop_fraction": drop,
                    "ceiling_censored": c["p_systemic"] >= 0.999,
                }
            out[n] = {"baseline_p": base["p_systemic"], "baseline_seed": base["seed_size"], "by_mu": row}
        return out
    er_a05_ratios = ratio_series_for(er_a05_cells, n_grid_a05)

    all_source_commits = {}
    for d in (cm_commits, girg_commits, er_m_commits, er_b_commits, er_a05_commits):
        all_source_commits.update(d)

    payload = {
        "metadata": {
            "script": "scripts/analyze_famcompare.py",
            "git_commit": git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "n_grid_full": N_GRID,
            "n_grid_used_main_panel": n_grid_used,
            "n_grid_skipped_main_panel": n_grid_skipped,
            "n_grid_used_a05_supplementary": n_grid_a05,
            "mu_grid": MU_GRID,
            "theta": 0.5,
            "ratio_ci_method": (
                "parametric bootstrap, 10000 resamples: k1*~Binomial(n1,p1_hat), "
                "k0*~Binomial(n0,p0_hat) drawn independently, ratio=(k1*/n1)/(k0*/n0); "
                "resamples with k0*==0 dropped (drop_fraction recorded per cell); "
                "95% CI = empirical 2.5/97.5 percentile of surviving resampled ratios"
            ),
            "bootstrap_seed": BOOTSTRAP_SEED,
            "source_commits": all_source_commits,
        },
        "main_panel": {
            "configuration_model": cm_ratios,
            "girg": girg_ratios,
            "erdos_renyi_matched": er_m_ratios,
        },
        "erdos_renyi_bounded_flat_zero": er_bounded_summary,
        "supplementary_erdos_renyi_a05_anchored": {
            "note": (
                "ER evaluated at its own a05(mu_bar=0) crossing (baseline ~0.5), NOT the "
                "matched-baseline anchor. Ratio is arithmetically ceiling-capped near 2x "
                "since baseline p~0.5 and p cannot exceed 1. Not part of the main panel."
            ),
            "ratios": er_a05_ratios,
        },
        "raw_cells": {
            "configuration_model": cm_cells,
            "girg": girg_cells,
            "erdos_renyi_matched": er_m_cells,
            "erdos_renyi_bounded": er_b_cells,
            "erdos_renyi_a05_anchored": er_a05_cells,
        },
    }

    out_path = os.path.join(REPO_ROOT, "results/processed/famcompare_analysis.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"n_grid used in main panel: {n_grid_used}")
    if n_grid_skipped:
        print(f"n_grid skipped (incomplete raws): {n_grid_skipped}")
    print(f"n_grid used for ER a05 supplementary: {n_grid_a05}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
