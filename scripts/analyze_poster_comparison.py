"""Analyze poster comparison sweep raw results and output Wilson score intervals."""

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
    {"key": "poster_er_mu40", "family": "erdos_renyi", "mu": 0.4, "raw": "results/poster_er_mu40_raw.json"},
    {"key": "poster_er_mu70", "family": "erdos_renyi", "mu": 0.7, "raw": "results/poster_er_mu70_raw.json"},
    {"key": "poster_cm_mu0", "family": "configuration_model", "mu": 0.0, "raw": "results/poster_cm_mu0_raw.json"},
    {"key": "poster_cm_mu40", "family": "configuration_model", "mu": 0.4, "raw": "results/poster_cm_mu40_raw.json"},
    {"key": "poster_cm_mu70", "family": "configuration_model", "mu": 0.7, "raw": "results/poster_cm_mu70_raw.json"},
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


def main() -> None:
    os.chdir(base_dir)
    proc_dir = os.path.join(base_dir, "results", "processed")
    os.makedirs(proc_dir, exist_ok=True)

    records = []
    source_raws = []
    commits = set()
    janson_ac_map = {}

    for spec in CONFIG_SPECS:
        raw_path = os.path.join(base_dir, spec["raw"])
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Raw file not found at {raw_path}")
        
        source_raws.append(spec["raw"])
        with open(raw_path, "r") as f:
            raw_data = json.load(f)
            
        md = raw_data.get("metadata", {})
        if "git_commit" in md:
            commits.add(md["git_commit"])

        n = md.get("n", 10000)
        p = md.get("p", 0.00045336)
        r = md.get("r", 2)
        ac0 = janson_a_c(n, p, r)
        janson_ac_map[spec["key"]] = ac0

        for cell in raw_data["results"]:
            seed_size = cell["seed_size"]
            a_over_ac = float(seed_size / ac0)
            failed_fracs = np.asarray(cell["failed_fractions"])
            n_trials = len(failed_fracs)
            n_systemic = int(np.sum(failed_fracs >= THETA))
            
            p_hat, ci_lower, ci_upper = wilson_score_interval(n_systemic, n_trials)
            
            records.append({
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
            })

    output_payload = {
        "metadata": {
            "script": "scripts/analyze_poster_comparison.py",
            "git_commit": get_git_commit_hash(),
            "source_raws": source_raws,
            "git_commits_in_raws": sorted(commits),
            "systemic_threshold_theta": THETA,
            "janson_a_c_map": janson_ac_map,
        },
        "records": records,
    }

    out_path = os.path.join(proc_dir, "poster_comparison.json")
    with open(out_path, "w") as f:
        json.dump(output_payload, f, indent=2)

    print(f"Analysis complete. Processed data saved to {out_path}")


if __name__ == "__main__":
    main()
