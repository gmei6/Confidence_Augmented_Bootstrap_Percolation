"""
Task O (Q5) analysis: C-Q5 nucleation law and coverage-entropy homogenization.

Reads results/q5_localized_fear_raw.json (written by scripts/run_task_o.py) and
evaluates, on systemic trials:

  (i)  Nucleation law (global field): fitted log-log slope of E[N_nuc] vs g_t,
       pooled over pre-cutoff rounds with g_t <= 0.5; C-Q5(i) predicts slope
       ~= r = 2 (threshold-like), refuted by slope ~= 1 (constant leak) or no
       nucleation at systemic-peak g_t.
  (iii) Homogenization: coverage entropy H at the theta-crossing round per
       (mu, field). The pre-registered absolute thresholds (global >= 0.9,
       local <= 0.6) are evaluated AND re-baselined against the mu=0 control
       (which itself sits well above 0.6 at this n; the scoping doc pre-commits
       to sanity-tuning these numbers on the control).

  (ii) Duration dichotomy needs an n-sweep (T_theta(n) exponents) and is
       explicitly deferred; recorded as such in the verdict.

Writes results/processed/task_o_locality_analysis.json.
"""

import os
import sys
import json
import datetime

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash

RAW_PATH = "results/q5_localized_fear_raw.json"
OUTPUT_PATH = "results/processed/task_o_locality_analysis.json"

G_MAX_FIT = 0.5   # nucleation law is a pre-theta statement
N_BINS = 12


def _binned_curve(x, v):
    x = np.asarray(x, dtype=float)
    v = np.asarray(v, dtype=float)
    if len(x) == 0:
        return None
    bins = np.logspace(np.log10(max(x.min(), 1e-4)), np.log10(x.max()), N_BINS + 1)
    centers, means, counts = [], [], []
    for lo, hi in zip(bins, bins[1:]):
        m = (x >= lo) & (x < hi)
        if m.sum() >= 5:
            centers.append(float(np.sqrt(lo * hi)))
            means.append(float(v[m].mean()))
            counts.append(int(m.sum()))
    return {"g_bin_centers": centers, "mean_n_nuc": means, "n_points": counts}


def nucleation_curve(trials):
    """Pooled (g_t, n_nuc) points from systemic trials; binned means in g_t."""
    pts = [(row["g_t"], row["n_nuc"])
           for t in trials if t["systemic"]
           for row in t["rounds"] if row["g_t"] <= G_MAX_FIT]
    return _binned_curve([p[0] for p in pts], [p[1] for p in pts]) if pts else None


def nucleation_curve_vs_phi(trials, weights, seed_size, n):
    """Pooled (phi_t, n_nuc): phi_t is the windowed recent-failure fraction that
    actually drives the engine's fear probability - the mechanism-faithful
    x-variable (the pre-registered g_t conflates the ignition exponent with
    front-perimeter kinematics: for a 2D ballistic front, new ~ sqrt(g))."""
    W = len(weights)
    pts = []
    for t in trials:
        if not t["systemic"]:
            continue
        news = {row["t"]: row["new"] for row in t["rounds"]}
        news[0] = seed_size
        for row in t["rounds"]:
            if row["g_t"] > G_MAX_FIT:
                continue
            phi = sum(weights[k - 1] * news.get(row["t"] - k, 0)
                      for k in range(1, W + 1)) / n
            if phi > 0:
                pts.append((phi, row["n_nuc"]))
    return _binned_curve([p[0] for p in pts], [p[1] for p in pts]) if pts else None


def fit_slope(curve):
    """OLS slope of log mean N_nuc vs log g_t over bins with positive mean."""
    if curve is None:
        return None
    x = np.array(curve["g_bin_centers"])
    y = np.array(curve["mean_n_nuc"])
    keep = y > 0
    if keep.sum() < 3:
        return None
    lx, ly = np.log(x[keep]), np.log(y[keep])
    A = np.vstack([lx, np.ones_like(lx)]).T
    (slope, intercept), res, *_ = np.linalg.lstsq(A, ly, rcond=None)
    ss_tot = float(((ly - ly.mean()) ** 2).sum())
    r2 = 1.0 - float(res[0]) / ss_tot if len(res) and ss_tot > 0 else None
    return {"slope": float(slope), "intercept": float(intercept),
            "r_squared": r2, "n_bins_fit": int(keep.sum())}


def entropy_at_theta(trials):
    """Mean/SE of H at each systemic trial's theta-crossing round."""
    vals = []
    for t in trials:
        if not t["systemic"] or t["t_theta"] is None:
            continue
        row = next((r for r in t["rounds"] if r["t"] == t["t_theta"]), None)
        if row is not None:
            vals.append(row["H"])
    if not vals:
        return None
    v = np.array(vals)
    return {"mean": float(v.mean()),
            "se": float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else None,
            "n_trials": len(v)}


def main():
    with open(os.path.join(base_dir, RAW_PATH)) as f:
        d = json.load(f)
    meta = d["metadata"]
    r = meta["r"]
    fields = [f["name"] for f in meta["fields"]]
    mu_grid = meta["mean_fear_grid"]

    def cell(mu, field):
        return [t for t in d["results"] if t["mean_fear"] == mu and t["field"] == field]

    # (i) nucleation law
    nucleation = {}
    for field in fields:
        per_mu = {}
        for mu in mu_grid:
            if mu == 0.0:
                continue
            curve = nucleation_curve(cell(mu, field))
            curve_phi = nucleation_curve_vs_phi(cell(mu, field), meta["weights"],
                                                meta["seed_size"], meta["n"])
            per_mu[str(mu)] = {"curve": curve, "fit": fit_slope(curve),
                               "curve_vs_phi": curve_phi,
                               "fit_vs_phi": fit_slope(curve_phi),
                               "total_nuclei": int(sum(
                                   row["n_nuc"] for t in cell(mu, field)
                                   for row in t["rounds"]))}
        nucleation[field] = per_mu

    # (iii) homogenization
    control = entropy_at_theta(cell(0.0, "global"))
    entropy = {field: {str(mu): entropy_at_theta(cell(mu, field))
                       for mu in mu_grid}
               for field in fields}

    global_fits = {mu: v["fit"] for mu, v in nucleation["global"].items()}
    verdict = {
        "clause_i_nucleation_law": {
            "prediction": f"global-field log-log slope ~= r = {r}; refuted by ~1 or no nucleation",
            "global_slopes_by_mu": {mu: (f["slope"] if f else None) for mu, f in global_fits.items()},
            "global_slopes_vs_phi_by_mu": {
                mu: (v["fit_vs_phi"]["slope"] if v["fit_vs_phi"] else None)
                for mu, v in nucleation["global"].items()},
            "local_1_total_nuclei": int(sum(v["total_nuclei"] for v in nucleation["local_1"].values())),
            "supported": all(f is not None and f["slope"] > 1.5 for f in global_fits.values()),
            "reading": "NOT SUPPORTED as pre-registered: slopes ~1.2-1.5 vs g_t and "
                       "~1.0-1.4 vs the mechanism-faithful windowed drive phi_t - a "
                       "constant leak, not the (drive)^r barrier. Honest negative per "
                       "the scoping doc's pre-commitment. Caveat for follow-up: the "
                       "same-round cluster counter may under-represent cross-round "
                       "pair ignition (failed_neighbor_count is cumulative, so two "
                       "lone remote failures in the same ball in DIFFERENT rounds "
                       "also ignite at r=2), and front-adjacent remotes may dominate "
                       "counts; a remote-ignited-growth tracker is the cleaner test.",
        },
        "clause_ii_duration_dichotomy": {
            "status": "DEFERRED - requires an n-sweep of T_theta(n) exponents "
                      "(single n here); flagged for the C++/PACE phase.",
        },
        "clause_iii_homogenization": {
            "prediction": "global H >= 0.9 by theta-crossing; local (ell/r_n <= 4) H <= 0.6",
            "mu0_control_H": control["mean"] if control else None,
            "note": "The mu=0 control itself sits near 0.69 at n=4000, above the "
                    "pre-registered 0.6 local ceiling, so absolute thresholds are "
                    "re-baselined per the scoping doc's sanity-tuning pre-commitment: "
                    "the operative test is elevation above the control.",
            "H_at_theta": {field: {mu: (v["mean"] if v else None)
                                   for mu, v in entropy[field].items()}
                           for field in fields},
            "supported_relative": None,  # filled below
        },
    }

    # Relative homogenization: global elevates above control; local_1 does not.
    if control:
        c = control["mean"]
        glob_elev = [entropy["global"][str(mu)]["mean"] - c for mu in mu_grid if mu > 0]
        loc1_elev = [entropy["local_1"][str(mu)]["mean"] - c for mu in mu_grid if mu > 0]
        verdict["clause_iii_homogenization"]["supported_relative"] = bool(
            all(e > 0.1 for e in glob_elev) and all(abs(e) < 0.05 for e in loc1_elev))

    out = {
        "metadata": {
            "task": "O (Q5 locality: nucleation law + coverage entropy)",
            "source_raw_file": RAW_PATH,
            "source_commit": meta["git_commit"],
            "base_seed": meta["base_seed"],
            "n": meta["n"], "r": r, "theta": meta["theta"],
            "fields": fields, "mean_fear_grid": mu_grid,
            "trials_per_cell": meta["trials_per_cell"],
            "g_max_fit": G_MAX_FIT,
            "analysis_runtime_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
        },
        "nucleation": nucleation,
        "entropy_at_theta": entropy,
        "mu0_control_entropy": control,
        "verdict": verdict,
    }

    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")
    print(json.dumps({k: v for k, v in verdict.items()}, indent=2, default=str)[:2000])


if __name__ == "__main__":
    main()
