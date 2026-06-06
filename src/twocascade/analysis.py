"""
Metric analyzer to process raw sweep outcomes.
"""

import json
import numpy as np
from typing import Dict, Any, List, Optional

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
