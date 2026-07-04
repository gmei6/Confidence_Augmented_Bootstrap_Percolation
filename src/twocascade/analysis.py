"""
Metric analyzer to process raw sweep outcomes.
"""

import json
import numpy as np
from typing import Dict, Any, List, Optional
from twocascade.meanfield import critical_seed_scaling, scaling_ratio

def systemic_prob_at_theta(failed_fractions: np.ndarray, theta: float) -> float:
    """
    Compute the fraction of realizations where the failed fraction is at least theta.
    
    Args:
        failed_fractions: Array of final failed fractions from trials.
        theta: Systemic-event threshold.
    """
    if len(failed_fractions) == 0:
        return 0.0
    return float(np.mean(failed_fractions >= theta))

def load_raw_results(filepath: str) -> Dict[str, Any]:
    """Load raw results JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)

def _interp_crossing(x: np.ndarray, y: np.ndarray, level: float = 0.5) -> Optional[float]:
    """Linearly interpolate where y crosses level. Returns NaN if no crossing."""
    if len(x) == 0 or len(y) == 0:
        return None
        
    # Ensure x and y are sorted by x ascending
    sort_idx = np.argsort(x)
    x_sorted = np.array(x)[sort_idx]
    y_sorted = np.array(y)[sort_idx]
    
    if y_sorted[0] >= level:
        return float(x_sorted[0])
    for i in range(1, len(y_sorted)):
        if y_sorted[i - 1] < level <= y_sorted[i]:
            dy = y_sorted[i] - y_sorted[i - 1]
            if dy == 0:
                return float(x_sorted[i - 1])
            t = (level - y_sorted[i - 1]) / dy
            return float(x_sorted[i - 1] + t * (x_sorted[i] - x_sorted[i - 1]))
    return float('nan')

def analyze_sweep(raw_data: Dict[str, Any], theta: Optional[float] = None) -> Dict[str, Any]:
    """Calculate systemic probabilities, find crossings, and organize bimodality data."""
    meta = raw_data["metadata"]
    if theta is None:
        theta = meta["theta"]
    results = raw_data["results"]
    
    sweep_params = raw_data["sweep_parameters"]
    mean_fear_grid = sweep_params["mean_fear_grid"]
    seed_multiples = sweep_params["seed_multiples"]
    seed_size_grid = sweep_params["seed_size_grid"]
    
    processed_cells = []
    
    curves_by_multiple: Dict[float, List[float]] = {float(m): [0.0] * len(mean_fear_grid) for m in seed_multiples}
    curves_by_mu: Dict[float, List[float]] = {float(mu): [0.0] * len(seed_size_grid) for mu in mean_fear_grid}
    
    import math
    
    for cell in results:
        mu = float(cell["mean_fear"])
        mult = float(cell["seed_multiple"])
        a = int(cell["seed_size"])
        ffs = np.array(cell["failed_fractions"])
        p_sys = systemic_prob_at_theta(ffs, theta)
        
        processed_cells.append({
            "mean_fear": mu,
            "seed_multiple": mult,
            "seed_size": a,
            "p_systemic": p_sys,
            "mean_rounds": float(np.mean(cell["rounds_completed"])),
            "failed_fractions": cell["failed_fractions"]
        })
        
        mu_idx = cell.get("mean_fear_idx")
        if mu_idx is None:
            try:
                mu_idx = next(idx for idx, val in enumerate(mean_fear_grid) if math.isclose(val, mu, abs_tol=1e-9))
            except StopIteration:
                raise ValueError(f"mean_fear {mu} not found in config mean_fear_grid {mean_fear_grid}")
                
        mult_idx = cell.get("seed_multiple_idx")
        if mult_idx is None:
            try:
                mult_idx = next(idx for idx, val in enumerate(seed_multiples) if math.isclose(val, mult, abs_tol=1e-9))
            except StopIteration:
                raise ValueError(f"seed_multiple {mult} not found in config seed_multiples {seed_multiples}")
        
        canonical_mu = float(mean_fear_grid[mu_idx])
        canonical_mult = float(seed_multiples[mult_idx])
        
        curves_by_multiple[canonical_mult][mu_idx] = p_sys
        curves_by_mu[canonical_mu][mult_idx] = p_sys

    # Find crossing mu value for each multiple curve
    crossings_mu = {}
    for mult, p_sys_vals in curves_by_multiple.items():
        crossing_mu = _interp_crossing(np.array(mean_fear_grid), np.array(p_sys_vals), level=0.5)
        crossings_mu[str(mult)] = crossing_mu
        
    # Find empirical critical seed size a_emp for each mu
    empirical_thresholds = {}
    for mu, p_sys_vals in curves_by_mu.items():
        crossing_a = _interp_crossing(np.array(seed_size_grid, dtype=float), np.array(p_sys_vals), level=0.5)
        empirical_thresholds[str(mu)] = crossing_a
        
    return {
        "metadata": meta,
        "processed_cells": processed_cells,
        "crossings_mu": crossings_mu,
        "empirical_thresholds": empirical_thresholds
    }

def evaluate_scaling_adherence(analyzed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate empirical threshold scaling against the theoretical (1-mu)**(r/(r-1)) law.
    
    This evaluates how closely the empirical threshold crossing values a_emp(mu) follow
    the theoretical Janson scaling ratio (1-mu)**(r/(r-1)).
    
    Args:
        analyzed_data: Dictionary returned by analyze_sweep containing:
            - metadata: Dictionary containing simulation parameters (n, p, r, theta).
            - empirical_thresholds: Dict mapping mu strings to crossing seed sizes.
            - processed_cells: List of processed sweep cell results.
            
    Returns:
        Dict containing:
            - results_table: List of dicts for each mu value containing:
                - mu: Float mean fear.
                - a_emp: Float empirical threshold.
                - ratio_emp: Float ratio of threshold at mu to threshold at mu=0, or None if clamped.
                - ratio_theory: Float theoretical scaling ratio.
                - diff: Float difference (ratio_emp - ratio_theory), or None if clamped.
                - predicted_ac: Float theoretical threshold.
                - is_clamped: Boolean flag indicating if empirical threshold is at the seed size floor.
            - max_diff: Float maximum absolute difference for non-clamped rows, or None if none.
            - mean_diff: Float mean absolute difference for non-clamped rows, or None if none.
            - a_emp_0: Float empirical threshold at mu=0.
            
    Raises:
        ValueError: If the mu=0 baseline threshold is missing or corrupted in the grid configuration.
    """
    meta = analyzed_data["metadata"]
    r = meta["r"]
    n = meta["n"]
    p = meta["p"]
    
    emp_thresholds = analyzed_data["empirical_thresholds"]
    
    mu_vals = []
    a_emp_vals = []
    
    min_seed_size = min(cell["seed_size"] for cell in analyzed_data["processed_cells"])
    
    for mu_str, a_emp in emp_thresholds.items():
        if a_emp is not None and not np.isnan(a_emp):
            mu_vals.append(float(mu_str))
            a_emp_vals.append(float(a_emp))
            
    sort_idx = np.argsort(mu_vals)
    mu_sorted = np.array(mu_vals)[sort_idx]
    a_emp_sorted = np.array(a_emp_vals)[sort_idx]
    
    results_table = []
    non_clamped_diffs = []
    
    mu0_idx = None
    a_emp_0 = None
    
    if len(mu_sorted) > 0:
        # Find the index of the mu value closest to 0.0.
        # If no mu=0 entry is present in the grid (or the closest is not close to 0.0),
        # we raise a ValueError to prevent evaluating relative ratios without a valid baseline.
        # If the dataset was completely empty (e.g., all thresholds NaN), the outer guard
        # skips this baseline calculation safely.
        mu0_idx = np.argmin(np.abs(mu_sorted))
        if abs(mu_sorted[mu0_idx]) > 1e-9:
            raise ValueError("CRITICAL: mu=0 baseline is missing or invalid in the selected grid layout.")
        a_emp_0 = a_emp_sorted[mu0_idx]
        
    if a_emp_0 is not None and a_emp_0 > 0:
        for mu, a_emp in zip(mu_sorted, a_emp_sorted):
            ratio_emp = a_emp / a_emp_0
            ratio_theory = scaling_ratio(mu, r)
            diff = ratio_emp - ratio_theory
            
            predicted_ac = critical_seed_scaling(n, p, r, mu)
            # Clamping is evaluated purely against the empirical floor (min_seed_size)
            is_clamped = a_emp <= min_seed_size
            
            if is_clamped:
                results_table.append({
                    "mu": mu,
                    "a_emp": a_emp,
                    "ratio_emp": None,
                    "ratio_theory": ratio_theory,
                    "diff": None,
                    "predicted_ac": predicted_ac,
                    "is_clamped": True
                })
            else:
                results_table.append({
                    "mu": mu,
                    "a_emp": a_emp,
                    "ratio_emp": ratio_emp,
                    "ratio_theory": ratio_theory,
                    "diff": diff,
                    "predicted_ac": predicted_ac,
                    "is_clamped": False
                })
                non_clamped_diffs.append(abs(diff))
                
    if len(non_clamped_diffs) > 0:
        max_diff = np.max(non_clamped_diffs)
        mean_diff = np.mean(non_clamped_diffs)
    else:
        max_diff = None
        mean_diff = None
        
    return {
        "results_table": results_table,
        "max_diff": max_diff,
        "mean_diff": mean_diff,
        "a_emp_0": a_emp_0
    }


def estimate_transition_width(
    failed_fractions_by_multiple: Dict[float, List[float]],
    theta: float,
    seed_multiples: List[float],
    bootstrap_reps: int = 500,
    conf_level: float = 0.95,
    seed: int = 12345
) -> Dict[str, Any]:
    """
    Fit P(systemic) vs seed_multiple to a logistic curve, and estimate
    the 10-90% transition width with a bootstrap confidence interval.
    
    Args:
        failed_fractions_by_multiple: Dict mapping seed_multiple (float) to list of failed fractions (list of floats).
        theta: Systemic event threshold (e.g. 0.5).
        seed_multiples: List of seed multiples in the sweep.
        bootstrap_reps: Number of bootstrap resamples.
        conf_level: Confidence level for the interval (default 0.95).
        seed: Random seed for bootstrap reproducibility.
        
    Returns:
        Dict containing:
            "width": Estimated transition width (dimensionless).
            "width_err": Bootstrap standard error of the width.
            "ci": Tuple (lower, upper) representing the bootstrap confidence interval.
            "k": Fit growth rate parameter.
            "x0": Fit midpoint parameter.
            "p_systemic": Dict mapping multiple to empirical P(systemic).
    """
    from scipy.optimize import curve_fit
    
    # Sort multiples to ensure monotonic curve fitting
    multiples = sorted(seed_multiples)
    p_sys_list = []
    binary_outcomes_by_multiple = {}
    
    for m in multiples:
        ffs = np.array(failed_fractions_by_multiple[m])
        outcomes = (ffs >= theta).astype(float)
        binary_outcomes_by_multiple[m] = outcomes
        p_sys_list.append(float(np.mean(outcomes)))
        
    x_data = np.array(multiples)
    y_data = np.array(p_sys_list)
    
    def logistic(x, k, x0):
        # Clip exponent to avoid overflow in exp
        return 1.0 / (1.0 + np.exp(-np.clip(k * (x - x0), -500, 500)))
        
    # Fit the empirical data
    p0 = [10.0, 1.0]  # Initial guess: k=10.0, x0=1.0
    bounds = ([0.0, 0.0], [np.inf, 2.0])  # Force positive slope and midpoint in [0, 2]
    
    try:
        popt, _ = curve_fit(logistic, x_data, y_data, p0=p0, bounds=bounds, maxfev=10000)
        k_fit, x0_fit = popt
        width_fit = (2.0 * np.log(9.0)) / k_fit
    except Exception:
        # Fallback if fit fails
        k_fit, x0_fit = np.nan, np.nan
        width_fit = np.nan
        
    # Bootstrap CI
    rng = np.random.default_rng(seed)
    boot_widths = []
    
    for _ in range(bootstrap_reps):
        y_boot = []
        for m in multiples:
            outcomes = binary_outcomes_by_multiple[m]
            if len(outcomes) > 0:
                boot_outcomes = rng.choice(outcomes, size=len(outcomes), replace=True)
                y_boot.append(float(np.mean(boot_outcomes)))
            else:
                y_boot.append(0.0)
                
        y_boot = np.array(y_boot)
        try:
            popt_b, _ = curve_fit(logistic, x_data, y_boot, p0=p0, bounds=bounds, maxfev=5000)
            k_b = popt_b[0]
            w_b = (2.0 * np.log(9.0)) / k_b
            if not np.isnan(w_b) and not np.isinf(w_b):
                boot_widths.append(w_b)
        except Exception:
            pass
            
    if len(boot_widths) > 0:
        boot_widths = np.array(boot_widths)
        alpha_err = 100.0 * (1.0 - conf_level)
        lo = float(np.percentile(boot_widths, alpha_err / 2.0))
        hi = float(np.percentile(boot_widths, 100.0 - alpha_err / 2.0))
        width_err = float(np.std(boot_widths, ddof=1)) if len(boot_widths) > 1 else 0.0
    else:
        lo, hi = np.nan, np.nan
        width_err = np.nan
        
    return {
        "width": width_fit,
        "width_err": width_err,
        "ci": (lo, hi),
        "k": k_fit,
        "x0": x0_fit,
        "p_systemic": {m: p_sys for m, p_sys in zip(multiples, p_sys_list)}
    }


def fit_finite_size_exponent(
    n_list: List[int],
    widths_list: List[float],
    width_errs_list: Optional[List[float]] = None
) -> Dict[str, Any]:
    """
    Fit log(width) = -1/nu * log(n) + C to estimate the transition-width exponent nu.
    
    Args:
        n_list: List of system sizes (int).
        widths_list: List of estimated widths (float).
        width_errs_list: Optional list of width errors (float) to use as weights.
        
    Returns:
        Dict containing:
            "nu": Estimated exponent (float).
            "nu_err": Propagated standard error of nu (float).
            "slope": Slope of the log-log fit (-1/nu) (float).
            "slope_err": Standard error of the slope (float).
            "intercept": Intercept of the log-log fit (C) (float).
            "r_squared": R^2 coefficient of determination of the fit (float).
    """
    from scipy.optimize import curve_fit
    
    x = np.log(np.array(n_list, dtype=float))
    y = np.log(np.array(widths_list, dtype=float))
    
    # Simple linear fit: y = slope * x + intercept
    def linear_model(x_val, slope, intercept):
        return slope * x_val + intercept
        
    # Standard linear regression to get initial values and weights
    if width_errs_list is not None:
        # Propagate width_err to log(width) error: d(log(w)) = dw / w
        w_arr = np.array(widths_list, dtype=float)
        we_arr = np.array(width_errs_list, dtype=float)
        # Avoid division by zero
        we_arr = np.where(we_arr <= 0.0, 1e-8, we_arr)
        y_err = we_arr / w_arr
    else:
        y_err = None
        
    popt, pcov = curve_fit(
        linear_model, x, y,
        p0=[-0.5, 0.0],
        sigma=y_err,
        absolute_sigma=(y_err is not None)
    )
    
    slope, intercept = popt
    slope_err = np.sqrt(pcov[0, 0])
    
    # Calculate R-squared
    y_pred = linear_model(x, slope, intercept)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0.0 else 1.0
    
    # Calculate nu = -1.0 / slope
    if slope != 0.0:
        nu = -1.0 / slope
        # Error propagation: delta_nu = nu^2 * delta_slope
        nu_err = (nu ** 2) * slope_err
    else:
        nu = np.nan
        nu_err = np.nan
        
    return {
        "nu": float(nu),
        "nu_err": float(nu_err),
        "slope": float(slope),
        "slope_err": float(slope_err),
        "intercept": float(intercept),
        "r_squared": float(r_squared)
    }


def analyze_fear_field_concentration(
    raw_by_n: Dict[int, Dict[str, Any]],
    rounds: Optional[List[int]] = None,
    min_trials: int = 2
) -> Dict[str, Any]:
    """
    Measure how the across-trial variance of the fear-field trajectory decays as
    the system size n grows (Task E, empirical concentration characterization).

    Conventions (window_len = 1): the raw histories are cumulative failed counts
    with history[0] = seed size, so the generation size of active round k >= 1 is
    a_k = history[k] - history[k-1], and g_k = a_k / n is the fear field that
    round k's failures exert on round k+1. Since g_0 = a_0 / n is deterministic
    given the config, rounds (1, 2, 3) are the first three stochastic fear-field
    values.

    For each cell (mean_fear, seed_multiple), each round k, and each n: across
    the trials whose cascade reached round k (rounds_completed >= k), compute the
    empirical mean E[g_k], variance Var(g_k), and relative variance
    Var(g_k) / E[g_k]^2, then fit log(rel var) = -gamma * log(n) + c across n to
    estimate the concentration decay rate gamma.

    Args:
        raw_by_n: Mapping from system size n to the loaded raw sweep JSON. Each
            raw dict must carry per-cell "histories" (list of per-trial cumulative
            histories) alongside "rounds_completed"; all sizes must share the same
            sweep grid.
        rounds: Active rounds k to analyze. Defaults to [1, 2, 3].
        min_trials: Minimum trials reaching round k for the cell stats to count
            (needs >= 2 for a sample variance).

    Returns:
        Dict with "rounds", "n_values", and "cells"; each cell carries
        "mean_fear", "seed_multiple", and "per_round" entries holding aligned
        lists over n ("mean_g", "var_g", "rel_var", "trials_included"; None where
        fewer than min_trials trials reached round k) plus the log-log "fit"
        ({"gamma", "gamma_err", "intercept", "r_squared", "n_points"}, or None if
        fewer than 2 sizes yield a valid relative variance).
    """
    if rounds is None:
        rounds = [1, 2, 3]
    if min_trials < 2:
        raise ValueError("min_trials must be >= 2 to compute a sample variance")
    if not raw_by_n:
        raise ValueError("raw_by_n must contain at least one system size")

    n_values = sorted(raw_by_n.keys())

    # Index cells by grid coordinates (never float keys) and check grid alignment.
    cells_by_n = {}
    for n in n_values:
        cells_by_n[n] = {
            (cell["mean_fear_idx"], cell["seed_multiple_idx"]): cell
            for cell in raw_by_n[n]["results"]
        }
    grid_keys = sorted(cells_by_n[n_values[0]].keys())
    for n in n_values[1:]:
        if sorted(cells_by_n[n].keys()) != grid_keys:
            raise ValueError(f"Sweep grid for n={n} does not match n={n_values[0]}")
        for key in grid_keys:
            ref, cur = cells_by_n[n_values[0]][key], cells_by_n[n][key]
            if (ref["mean_fear"], ref["seed_multiple"]) != (cur["mean_fear"], cur["seed_multiple"]):
                raise ValueError(f"Cell {key} parameters differ between n={n_values[0]} and n={n}")

    out_cells = []
    for key in grid_keys:
        ref_cell = cells_by_n[n_values[0]][key]
        per_round = []
        for k in rounds:
            mean_g, var_g, rel_var, trials_included = [], [], [], []
            for n in n_values:
                cell = cells_by_n[n][key]
                g_vals = [
                    (hist[k] - hist[k - 1]) / n
                    for hist, rc in zip(cell["histories"], cell["rounds_completed"])
                    if rc >= k
                ]
                trials_included.append(len(g_vals))
                if len(g_vals) >= min_trials:
                    g_arr = np.asarray(g_vals, dtype=float)
                    m = float(np.mean(g_arr))
                    v = float(np.var(g_arr, ddof=1))
                    mean_g.append(m)
                    var_g.append(v)
                    rel_var.append(v / m**2 if m > 0.0 else None)
                else:
                    mean_g.append(None)
                    var_g.append(None)
                    rel_var.append(None)

            valid = [(n, rv) for n, rv in zip(n_values, rel_var) if rv is not None and rv > 0.0]
            if len(valid) >= 2:
                x = np.log(np.array([n for n, _ in valid], dtype=float))
                y = np.log(np.array([rv for _, rv in valid], dtype=float))
                slope, intercept = np.polyfit(x, y, 1)
                y_pred = slope * x + intercept
                ss_res = float(np.sum((y - y_pred) ** 2))
                ss_tot = float(np.sum((y - np.mean(y)) ** 2))
                # OLS slope standard error; undefined without residual dof.
                if len(valid) > 2:
                    sxx = float(np.sum((x - np.mean(x)) ** 2))
                    gamma_err = float(np.sqrt((ss_res / (len(valid) - 2)) / sxx))
                else:
                    gamma_err = None
                fit = {
                    "gamma": float(-slope),
                    "gamma_err": gamma_err,
                    "intercept": float(intercept),
                    "r_squared": 1.0 - ss_res / ss_tot if ss_tot > 0.0 else 1.0,
                    "n_points": len(valid)
                }
            else:
                fit = None

            per_round.append({
                "round": k,
                "mean_g": mean_g,
                "var_g": var_g,
                "rel_var": rel_var,
                "trials_included": trials_included,
                "fit": fit
            })

        out_cells.append({
            "mean_fear": ref_cell["mean_fear"],
            "seed_multiple": ref_cell["seed_multiple"],
            "per_round": per_round
        })

    return {
        "rounds": list(rounds),
        "n_values": [int(n) for n in n_values],
        "cells": out_cells
def evaluate_binomial_dispersion(
    failures_at_t: List[int],
    seed_size: int,
    n: int,
    bootstrap_reps: int = 2000,
    conf_level: float = 0.95,
    seed: int = 20260704
) -> Dict[str, Any]:
    """
    Test the cumulative failure count S(t) at a fixed round against the i.i.d.
    binomial benchmark S(t) - a ~ Bin(n - a, pi(t)).

    Computes the empirical mean fraction pi(t) = E[S(t) - a] / (n - a), the
    empirical variance Var(S(t)), and the overdispersion ratio
    D_t = Var(S(t)) / [(n - a) * pi(t) * (1 - pi(t))], with a percentile
    bootstrap confidence interval for D_t (trials resampled with replacement).

    Args:
        failures_at_t: Per-trial cumulative failure counts S(t) at the fixed
            round t, INCLUDING the a seed nodes.
        seed_size: Initial seed size a.
        n: System size.
        bootstrap_reps: Number of bootstrap resamples for the CI.
        conf_level: Confidence level for the bootstrap interval (default 0.95).
        seed: Random seed for bootstrap reproducibility.

    Returns:
        Dict containing:
            "pi_t": Empirical mean failed fraction of the susceptible pool.
            "var_empirical": Empirical variance of S(t) (ddof=1).
            "var_binomial": Binomial benchmark variance (n-a)*pi*(1-pi).
            "dispersion_ratio": D_t, or NaN if the benchmark variance is zero
                (pi(t) degenerate at 0 or 1).
            "ci": Tuple (lower, upper) percentile bootstrap CI for D_t
                (NaN, NaN if degenerate).
            "n_trials": Number of trials used.

    Raises:
        ValueError: If seed_size >= n, or fewer than 2 trials are supplied.
    """
    if seed_size >= n:
        raise ValueError(f"seed_size ({seed_size}) must be smaller than n ({n})")
    s = np.asarray(failures_at_t, dtype=float)
    if len(s) < 2:
        raise ValueError("Need at least 2 trials to estimate a variance")

    m = n - seed_size  # susceptible pool size

    def _dispersion(vals: np.ndarray) -> float:
        pi = float(np.mean(vals - seed_size)) / m
        var_binom = m * pi * (1.0 - pi)
        if var_binom <= 0.0:
            return float("nan")
        return float(np.var(vals, ddof=1)) / var_binom

    pi_t = float(np.mean(s - seed_size)) / m
    var_empirical = float(np.var(s, ddof=1))
    var_binomial = m * pi_t * (1.0 - pi_t)
    dispersion_ratio = _dispersion(s)

    if np.isnan(dispersion_ratio):
        return {
            "pi_t": pi_t,
            "var_empirical": var_empirical,
            "var_binomial": var_binomial,
            "dispersion_ratio": float("nan"),
            "ci": (float("nan"), float("nan")),
            "n_trials": len(s)
        }

    rng = np.random.default_rng(seed)
    boot_ratios = []
    for _ in range(bootstrap_reps):
        resample = rng.choice(s, size=len(s), replace=True)
        d_b = _dispersion(resample)
        if np.isfinite(d_b):
            boot_ratios.append(d_b)

    if len(boot_ratios) > 0:
        boot_ratios = np.array(boot_ratios)
        alpha_err = 100.0 * (1.0 - conf_level)
        lo = float(np.percentile(boot_ratios, alpha_err / 2.0))
        hi = float(np.percentile(boot_ratios, 100.0 - alpha_err / 2.0))
    else:
        lo, hi = float("nan"), float("nan")

    return {
        "pi_t": pi_t,
        "var_empirical": var_empirical,
        "var_binomial": var_binomial,
        "dispersion_ratio": dispersion_ratio,
        "ci": (lo, hi),
        "n_trials": len(s)
    }

