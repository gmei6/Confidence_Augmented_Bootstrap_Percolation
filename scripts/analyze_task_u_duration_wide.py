"""
Task U (Q5, C-Q5(ii) asymptotic-form refinement): wide-n duration readout.

Reads results/q5_duration_wide_raw.json and computes, per (n, field, mu) cell:
mean T_theta over systemic trials and the ballistic ratio
T_theta / sqrt(n / log n). C-Q5(ii) predicts the ratio is ~constant in n for
the ell = r_n local field (ballistic front) and strictly decreasing in n for
the global field (secondary nucleation short-circuits the front). The mu = 0
control cell is field-free and anchors the ballistic constant.

The verdict fits log(ratio) vs log(n) per (field, mu) series and compares
each slope against the mu = 0 control slope (field type is provably
irrelevant at mu = 0, so the control carries the pure finite-size drift of
the ballistic constant): a slope indistinguishable from the control's is
ballistic; a slope significantly below it is sub-ballistic.
Writes results/processed/task_u_duration_wide_analysis.json.

The actual NEW question (whether the global slope is a stable power law or
flattens vs. Task O's n in {4000..32000} grid) is answered by hand comparing
this analysis's global slope against Task O's -- see the task file's step 3.
"""

import os
import sys
import json
import datetime
from collections import defaultdict

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash

RAW_PATH = "results/q5_duration_wide_raw.json"
OUTPUT_PATH = "results/processed/task_u_duration_wide_analysis.json"

# Regimes are judged on the slope DIFFERENCE vs the mu = 0 control series:
# |t_diff| <= 2 -> ballistic (same drift as the field-free control);
# t_diff < -2  -> sub-ballistic (ratio decays beyond the control drift).
T_CRIT = 2.0


def main():
    with open(os.path.join(base_dir, RAW_PATH)) as f:
        raw = json.load(f)
    meta = raw["metadata"]

    cells = defaultdict(list)
    for rec in raw["results"]:
        cells[(rec["n"], rec["field"], rec["mean_fear"])].append(rec)

    table = []
    for (n, field, mu) in sorted(cells):
        recs = cells[(n, field, mu)]
        ts = np.array([r["t_theta"] for r in recs
                       if r["systemic"] and r["t_theta"] is not None], dtype=float)
        ballistic_scale = float(np.sqrt(n / np.log(n)))
        row = {
            "n": n,
            "field": field,
            "mean_fear": mu,
            "n_trials": len(recs),
            "n_systemic": int(sum(r["systemic"] for r in recs)),
            "p_systemic": float(np.mean([r["systemic"] for r in recs])),
            "ballistic_scale": ballistic_scale,
        }
        if len(ts) > 0:
            row.update({
                "mean_t_theta": float(ts.mean()),
                "sd_t_theta": float(ts.std(ddof=1)) if len(ts) > 1 else 0.0,
                "se_t_theta": float(ts.std(ddof=1) / np.sqrt(len(ts))) if len(ts) > 1 else 0.0,
                "ballistic_ratio": float(ts.mean() / ballistic_scale),
                "ballistic_ratio_se": float(ts.std(ddof=1) / np.sqrt(len(ts)) / ballistic_scale)
                                      if len(ts) > 1 else 0.0,
            })
        else:
            row.update({"mean_t_theta": None, "sd_t_theta": None, "se_t_theta": None,
                        "ballistic_ratio": None, "ballistic_ratio_se": None})
        table.append(row)

    # Per-(field, mu) series: weighted least squares of log(ratio) on log(n).
    series_fits = {}
    by_series = defaultdict(list)
    for row in table:
        if row["ballistic_ratio"] is not None:
            by_series[(row["field"], row["mean_fear"])].append(row)
    for (field, mu), rows in sorted(by_series.items()):
        rows.sort(key=lambda r: r["n"])
        x = np.log([r["n"] for r in rows])
        y = np.log([r["ballistic_ratio"] for r in rows])
        w = np.array([1.0 / max(r["ballistic_ratio_se"] / r["ballistic_ratio"], 1e-6) ** 2
                      for r in rows])
        W = np.sum(w)
        xbar = np.sum(w * x) / W
        ybar = np.sum(w * y) / W
        sxx = np.sum(w * (x - xbar) ** 2)
        slope = float(np.sum(w * (x - xbar) * (y - ybar)) / sxx)
        slope_se = float(np.sqrt(1.0 / sxx))
        series_fits[f"{field}|mu={mu}"] = {
            "field": field,
            "mean_fear": mu,
            "n_points": len(rows),
            "log_ratio_vs_log_n_slope": slope,
            "slope_se": slope_se,
            "ratios_by_n": {str(r["n"]): r["ballistic_ratio"] for r in rows},
        }

    # Judge each field series against the mu = 0 control slope: the control is
    # field-free, so its (small) negative slope is the finite-size drift of
    # the ballistic constant itself, not a field effect.
    ctrl = series_fits["control|mu=0.0"]
    for key, f in series_fits.items():
        d = f["log_ratio_vs_log_n_slope"] - ctrl["log_ratio_vs_log_n_slope"]
        d_se = float(np.sqrt(f["slope_se"] ** 2 + ctrl["slope_se"] ** 2))
        t = d / d_se if d_se > 0 else 0.0
        f["slope_minus_control"] = float(d)
        f["slope_diff_se"] = d_se
        f["t_vs_control"] = float(t)
        f["regime"] = ("control (field-free reference)" if key == "control|mu=0.0"
                       else "ballistic (ratio ~ constant vs control)" if abs(t) <= T_CRIT
                       else "sub-ballistic (ratio decreasing vs control)" if t < -T_CRIT
                       else "super-ballistic (ratio increasing vs control)")

    local_ballistic = all(abs(f["t_vs_control"]) <= T_CRIT
                          for f in series_fits.values() if f["field"] == "local_1")
    global_decreasing = all(f["t_vs_control"] < -T_CRIT
                            for f in series_fits.values() if f["field"] == "global")
    verdict = {
        "clause": "C-Q5(ii) duration dichotomy: T_theta / sqrt(n/log n) ~ constant "
                  "for ell = r_n local field, -> 0 for global field",
        "local_1_ballistic": bool(local_ballistic),
        "global_sub_ballistic": bool(global_decreasing),
        "supported": bool(local_ballistic and global_decreasing),
        "t_crit": T_CRIT,
        "criterion": "log-ratio-vs-log-n slope compared against the mu = 0 "
                     "control slope (paired finite-size drift)",
    }

    out = {
        "metadata": {
            "task": "U (Q5 C-Q5(ii) asymptotic-form refinement: wide-n duration)",
            "source_raw_file": RAW_PATH,
            "source_commit": meta["git_commit"],
            "source_base_seed": meta["base_seed"],
            "n_grid": meta["n_grid"],
            "theta": meta["theta"],
            "trials_per_cell": meta["trials_per_cell"],
            "analysis_runtime_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
        },
        "ballistic_ratio_table": table,
        "series_fits": series_fits,
        "verdict": verdict,
    }

    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")
    print(json.dumps(verdict, indent=2))
    for key, fit in series_fits.items():
        print(f"{key}: slope={fit['log_ratio_vs_log_n_slope']:+.4f} "
              f"(t_vs_control={fit['t_vs_control']:+.1f}) -> {fit['regime']}")


if __name__ == "__main__":
    main()
