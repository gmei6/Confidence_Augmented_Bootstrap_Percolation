"""Analyze poster comparison sweep raw results and output Wilson score intervals,
crossings with propagated Wilson uncertainty, D-012 floor checks, and inflation factors.

A CONFIG_SPECS entry's "raw" field may be a single path or a list of paths; a
list is merged cell-by-cell into one curve (used for tail-extension sweeps that
add seed sizes outside an existing grid without re-indexing its RNG streams --
see the poster_er_mu40/mu70 entries)."""

import json
import os
import sys
import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash
from twocascade.model import janson_a_c

CONFIG_SPECS = [
    {"key": "poster_er_mu0", "family": "erdos_renyi", "mu": 0.0, "raw": "results/poster_er_mu0_raw.json"},
    {"key": "poster_er_mu10", "family": "erdos_renyi", "mu": 0.1, "raw": "results/poster_er_mu10_raw.json"},
    {"key": "poster_er_mu20", "family": "erdos_renyi", "mu": 0.2, "raw": "results/poster_er_mu20_raw.json"},
    {"key": "poster_er_mu30", "family": "erdos_renyi", "mu": 0.3, "raw": "results/poster_er_mu30_raw.json"},
    # mu=0.4 and mu=0.7 each merge two raws: the original 11-point grid plus a
    # separate tail-extension sweep (configs/poster_er_mu{40,70}_tails.json).
    # The tails are a SEPARATE config/raw rather than a widened original grid
    # because widening a seed_sizes list in place re-indexes the RNG child-seed
    # stream for every existing cell (project lesson) -- merging post-hoc here
    # keeps the original raw's cells reproducible and untouched.
    {"key": "poster_er_mu40", "family": "erdos_renyi", "mu": 0.4, "raw": ["results/poster_er_mu40_raw.json", "results/poster_er_mu40_tails_raw.json"]},
    {"key": "poster_er_mu50", "family": "erdos_renyi", "mu": 0.5, "raw": "results/poster_er_mu50_raw.json"},
    {"key": "poster_er_mu60", "family": "erdos_renyi", "mu": 0.6, "raw": "results/poster_er_mu60_raw.json"},
    {"key": "poster_er_mu70", "family": "erdos_renyi", "mu": 0.7, "raw": ["results/poster_er_mu70_raw.json", "results/poster_er_mu70_tails_raw.json"]},
    {"key": "poster_cm_mu0", "family": "configuration_model", "mu": 0.0, "raw": "results/poster_cm_mu0_raw.json"},
    {"key": "poster_cm_mu10", "family": "configuration_model", "mu": 0.1, "raw": "results/poster_cm_mu10_raw.json"},
    {"key": "poster_cm_mu20", "family": "configuration_model", "mu": 0.2, "raw": "results/poster_cm_mu20_raw.json"},
    {"key": "poster_cm_mu30", "family": "configuration_model", "mu": 0.3, "raw": "results/poster_cm_mu30_raw.json"},
    {"key": "poster_cm_mu40", "family": "configuration_model", "mu": 0.4, "raw": "results/poster_cm_mu40_raw.json"},
    {"key": "poster_cm_mu50", "family": "configuration_model", "mu": 0.5, "raw": "results/poster_cm_mu50_raw.json"},
    {"key": "poster_cm_mu60", "family": "configuration_model", "mu": 0.6, "raw": "results/poster_cm_mu60_raw.json"},
    {"key": "poster_cm_mu70", "family": "configuration_model", "mu": 0.7, "raw": "results/poster_cm_mu70_raw.json"},
    {"key": "poster_girg_mu0", "family": "girg", "mu": 0.0, "raw": "results/poster_girg_mu0_raw.json"},
    {"key": "poster_girg_mu40", "family": "girg", "mu": 0.4, "raw": "results/poster_girg_mu40_raw.json"},
    {"key": "poster_girg_mu70", "family": "girg", "mu": 0.7, "raw": "results/poster_girg_mu70_raw.json"},
]


THETA = 0.5  # systemic cascade threshold


def wilson_score_interval(k: int, n: int, confidence: float = 0.95) -> tuple[float, float, float]:
    if n == 0:
        return 0.0, 0.0, 0.0
    p_hat = k / n
    z = 1.959963984540054  # 95% confidence
    
    denom = 1.0 + (z**2) / n
    center = (p_hat + (z**2) / (2 * n)) / denom
    margin = (z / denom) * np.sqrt((p_hat * (1.0 - p_hat) / n) + ((z**2) / (4 * n**2)))
    
    ci_lower = max(0.0, float(center - margin))
    ci_upper = min(1.0, float(center + margin))
    return float(p_hat), ci_lower, ci_upper


def interpolate_crossing(x_arr: np.ndarray, y_arr: np.ndarray, target: float = 0.5) -> float:
    for i in range(len(y_arr) - 1):
        if y_arr[i] == target:
            return float(x_arr[i])
        if (y_arr[i] < target <= y_arr[i + 1]) or (y_arr[i] > target >= y_arr[i + 1]):
            dy = y_arr[i + 1] - y_arr[i]
            if dy == 0:
                return float(x_arr[i])
            frac = (target - y_arr[i]) / dy
            return float(x_arr[i] + frac * (x_arr[i + 1] - x_arr[i]))
    if y_arr[0] > target:
        return float(x_arr[0])
    if y_arr[-1] < target:
        return float(x_arr[-1])
    return float("nan")


def main() -> None:
    os.chdir(base_dir)
    proc_dir = os.path.join(base_dir, "results", "processed")
    os.makedirs(proc_dir, exist_ok=True)

    records = []
    source_raws = []
    commits = set()
    janson_ac_map = {}
    curves_summary = {}

    for spec in CONFIG_SPECS:
        raw_specs = spec["raw"] if isinstance(spec["raw"], list) else [spec["raw"]]

        n = p = r = engine_resolved = None
        all_cells = []
        for raw_rel in raw_specs:
            raw_path = os.path.join(base_dir, raw_rel)
            if not os.path.exists(raw_path):
                raise FileNotFoundError(f"Raw file not found at {raw_path}")

            source_raws.append(raw_rel)
            with open(raw_path, "r") as f:
                raw_data = json.load(f)

            md = raw_data.get("metadata", {})
            if "git_commit" in md:
                commits.add(md["git_commit"])

            this_engine = md.get("engine_resolved", md.get("engine", "unknown"))
            this_n = md.get("n", 10000)
            this_p = md.get("p", 0.00045336)
            this_r = md.get("r", 2)

            if n is None:
                n, p, r, engine_resolved = this_n, this_p, this_r, this_engine
            else:
                # Merging a tail-extension raw into a curve: the pinned params
                # and engine must match the base raw exactly, or this would be
                # silently combining two different experiments into one curve.
                assert (this_n, this_p, this_r) == (n, p, r), (
                    f"{spec['key']}: pinned-param mismatch merging {raw_rel} "
                    f"({this_n}, {this_p}, {this_r}) vs base ({n}, {p}, {r})"
                )
                assert this_engine == engine_resolved, (
                    f"{spec['key']}: engine mismatch merging {raw_rel}: "
                    f"{this_engine} vs {engine_resolved}"
                )
            all_cells.extend(raw_data["results"])

        ac0 = janson_a_c(n, p, r)
        janson_ac_map[spec["key"]] = ac0

        curve_records = []
        realized_mus = []
        for cell in all_cells:
            seed_size = cell["seed_size"]
            a_over_ac = float(seed_size / ac0)
            failed_fracs = np.asarray(cell["failed_fractions"])
            n_trials = len(failed_fracs)
            n_systemic = int(np.sum(failed_fracs >= THETA))
            
            p_hat, ci_lower, ci_upper = wilson_score_interval(n_systemic, n_trials)
            
            if "realized_fear" in cell and cell["realized_fear"] is not None:
                rf = cell["realized_fear"]
                if isinstance(rf, list):
                    realized_mus.extend(rf)
                else:
                    realized_mus.append(rf)

            rec = {
                "config_key": spec["key"],
                "family": spec["family"],
                "mean_fear": spec["mu"],
                "seed_size": seed_size,
                "janson_a_c": ac0,
                "a_over_ac": a_over_ac,
                "n_trials": n_trials,
                "n_systemic": n_systemic,
                "p_systemic": p_hat,
                "wilson_ci_lower": ci_lower,
                "wilson_ci_upper": ci_upper,
            }
            records.append(rec)
            curve_records.append(rec)

        curve_records.sort(key=lambda x: x["seed_size"])
        seed_sizes = np.array([cr["seed_size"] for cr in curve_records], dtype=float)
        p_sys = np.array([cr["p_systemic"] for cr in curve_records], dtype=float)
        ci_low = np.array([cr["wilson_ci_lower"] for cr in curve_records], dtype=float)
        ci_upp = np.array([cr["wilson_ci_upper"] for cr in curve_records], dtype=float)

        interior_mask = (p_sys > 0.05) & (p_sys < 0.95)
        interior_count = int(np.sum(interior_mask))
        reliable = bool(interior_count >= 3)

        a05_point = interpolate_crossing(seed_sizes, p_sys, 0.5)
        a05_low = interpolate_crossing(seed_sizes, ci_upp, 0.5)
        a05_high = interpolate_crossing(seed_sizes, ci_low, 0.5)

        avg_realized_mu = float(np.mean(realized_mus)) if len(realized_mus) > 0 else spec["mu"]

        curves_summary[spec["key"]] = {
            "key": spec["key"],
            "family": spec["family"],
            "mean_fear": spec["mu"],
            "engine_resolved": engine_resolved,
            "realized_mu_bar": avg_realized_mu,
            "janson_a_c": ac0,
            "interior_point_count": interior_count,
            "reliable": reliable,
            "a05_point": a05_point,
            "a05_ci_lower": a05_low,
            "a05_ci_upper": a05_high,
            "a_over_ac_point": a05_point / ac0,
            "a_over_ac_ci_lower": a05_low / ac0,
            "a_over_ac_ci_upper": a05_high / ac0,
        }

    # D-012 scaling prediction table calculation
    # Formula: a_c(mu) = a_c(0) * (1 - mu)^(r / (r - 1)) = a_c(0) * (1 - mu)^2 for r=2
    # Each family is anchored at its own mu=0 arm (mirrors the CM/ER anchor
    # selection); girg only has mu in {0.0, 0.4, 0.7} in this sweep.
    d012_table = []
    family_key_prefix = {"erdos_renyi": "er", "configuration_model": "cm", "girg": "girg"}
    family_mus = {
        "erdos_renyi": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        "configuration_model": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        "girg": [0.0, 0.4, 0.7],
    }
    for fam in ["erdos_renyi", "configuration_model", "girg"]:
        prefix = family_key_prefix[fam]
        anchor_key = f"poster_{prefix}_mu0"
        anchor_crossing = curves_summary[anchor_key]["a05_point"]

        for mu in family_mus[fam]:
            key = f"poster_{prefix}_mu{int(round(mu*100))}"
            cur = curves_summary[key]
            meas = cur["a05_point"]
            meas_low = cur["a05_ci_lower"]
            meas_high = cur["a05_ci_upper"]

            pred = anchor_crossing * ((1.0 - mu) ** 2)
            ratio = meas / pred if pred > 0 else np.nan
            below_floor = bool(pred < 2.0)

            ratio_to_mu0 = meas / anchor_crossing if anchor_crossing > 0 else np.nan
            ratio_to_mu0_low = meas_low / anchor_crossing if anchor_crossing > 0 else np.nan
            ratio_to_mu0_high = meas_high / anchor_crossing if anchor_crossing > 0 else np.nan

            d012_table.append({
                "family": fam,
                "mean_fear": mu,
                "key": key,
                "measured_crossing": meas,
                "measured_ci_lower": meas_low,
                "measured_ci_upper": meas_high,
                "measured_ratio_to_mu0": ratio_to_mu0,
                "measured_ratio_to_mu0_ci_lower": ratio_to_mu0_low,
                "measured_ratio_to_mu0_ci_upper": ratio_to_mu0_high,
                "measured_a_over_ac": cur["a_over_ac_point"],
                "measured_a_over_ac_ci_lower": cur["a_over_ac_ci_lower"],
                "measured_a_over_ac_ci_upper": cur["a_over_ac_ci_upper"],
                "predicted_crossing": pred,
                "ratio": ratio,
                "below_floor": below_floor,
                "interior_count": cur["interior_point_count"],
            })


    # Finite size inflation factor for ER mu=0
    er_mu0_cur = curves_summary["poster_er_mu0"]
    ac0_er = er_mu0_cur["janson_a_c"]
    inflation_point = er_mu0_cur["a05_point"] / ac0_er
    inflation_low = er_mu0_cur["a05_ci_lower"] / ac0_er
    inflation_high = er_mu0_cur["a05_ci_upper"] / ac0_er

    output_payload = {
        "metadata": {
            "script": "scripts/analyze_poster_comparison.py",
            "git_commit": get_git_commit_hash(),
            "source_raws": source_raws,
            "git_commits_in_raws": sorted(commits),
            "systemic_threshold_theta": THETA,
            "janson_a_c_map": janson_ac_map,
        },
        "curves_summary": curves_summary,
        "d012_table": d012_table,
        "inflation_factor_er_mu0": {
            "point": inflation_point,
            "ci_lower": inflation_low,
            "ci_upper": inflation_high,
            "janson_a_c": ac0_er,
        },
        "records": records,
    }

    out_path = os.path.join(proc_dir, "poster_comparison.json")
    with open(out_path, "w") as f:
        json.dump(output_payload, f, indent=2)

    print(f"Analysis complete. Processed data saved to {out_path}")
    print("\n--- SUMMARY TABLE ---")
    print(f"{'Key':<16} {'Engine':<8} {'mu_real':<8} {'Interior':<8} {'a_0.5 (Point)':<14} {'a_0.5 (95% CI)':<20} {'a/a_c (Point)':<14} {'a/a_c (95% CI)':<20}")
    for k, v in curves_summary.items():
        print(f"{k:<16} {v['engine_resolved']:<8} {v['realized_mu_bar']:<8.3f} {v['interior_point_count']:<8} {v['a05_point']:<14.2f} [{v['a05_ci_lower']:.2f}, {v['a05_ci_upper']:.2f}] {'':<3} {v['a_over_ac_point']:<14.4f} [{v['a_over_ac_ci_lower']:.4f}, {v['a_over_ac_ci_upper']:.4f}]")

    print("\n--- D-012 COMPARISON TABLE ---")
    print(f"{'Family':<22} {'mu':<5} {'Measured (CI)':<26} {'Predicted':<12} {'Ratio':<8} {'Below Floor (<r=2)?':<20}")
    for row in d012_table:
        ci_str = f"{row['measured_crossing']:.2f} [{row['measured_ci_lower']:.2f}, {row['measured_ci_upper']:.2f}]"
        print(f"{row['family']:<22} {row['mean_fear']:<5.1f} {ci_str:<26} {row['predicted_crossing']:<12.2f} {row['ratio']:<8.3f} {str(row['below_floor']):<20}")

    print(f"\nER mu=0 Inflation Factor over Janson a_c ({ac0_er:.2f}): {inflation_point:.3f} [{inflation_low:.3f}, {inflation_high:.3f}]")


if __name__ == "__main__":
    main()

