"""
Metric analyzer to process raw sweep outcomes.
"""

import json
import numpy as np
from typing import Dict, Any, List, Optional
from twocascade.meanfield import critical_seed_scaling, scaling_ratio

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

def analyze_sweep(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate systemic probabilities, find crossings, and organize bimodality data."""
    meta = raw_data["metadata"]
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
        p_sys = float(np.mean(ffs >= theta))
        
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
