"""
Unit tests for twocascade.analysis metrics and interpolation.
"""

import pytest
import numpy as np
from twocascade.analysis import _interp_crossing, analyze_sweep, evaluate_scaling_adherence, systemic_prob_at_theta

def test_systemic_prob_at_theta():
    """Verify systemic probability calculation under boundaries and edge cases."""
    # Empty array case
    assert systemic_prob_at_theta(np.array([]), 0.5) == 0.0
    
    # Normal cases
    arr = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
    assert np.isclose(systemic_prob_at_theta(arr, 0.5), 3/5)
    assert np.isclose(systemic_prob_at_theta(arr, 0.0), 1.0)
    assert np.isclose(systemic_prob_at_theta(arr, 1.0), 0.0)
    
    # Hard limits
    all_zero = np.zeros(10)
    assert systemic_prob_at_theta(all_zero, 0.0) == 1.0
    assert systemic_prob_at_theta(all_zero, 0.1) == 0.0

def test_analyze_sweep_with_custom_theta():
    """Verify analyze_sweep respects custom theta and uses string keys for outputs."""
    raw_data = {
        "metadata": {
            "n": 100, "p": 0.05, "r": 2, "concentration": 50.0, "theta": 0.5,
            "window_len": 1, "weights": None, "trials_per_cell": 2, "base_seed": 42
        },
        "sweep_parameters": {
            "mean_fear_grid": [0.0, 0.3],
            "seed_multiples": [1.0],
            "seed_size_grid": [4]
        },
        "results": [
            {"mean_fear": 0.0, "seed_multiple": 1.0, "seed_size": 4, "failed_fractions": [0.2, 0.4], "rounds_completed": [1, 1]}
        ]
    }
    # If custom theta = 0.3, failed_fractions [0.2, 0.4] has 1 element >= 0.3 -> p_sys = 0.5
    res = analyze_sweep(raw_data, theta=0.3)
    assert np.isclose(res["processed_cells"][0]["p_systemic"], 0.5)
    
    # Verify key types in empirical_thresholds mapping are strings
    for key in res["empirical_thresholds"].keys():
        assert isinstance(key, str)

def test_interp_crossing():
    """Verify linear interpolation crossing logic."""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    
    y = np.array([0.0, 0.2, 0.8, 1.0])
    crossing = _interp_crossing(x, y, level=0.5)
    assert np.isclose(crossing, 1.5)
    
    y2 = np.array([0.6, 0.7, 0.8, 0.9])
    assert np.isclose(_interp_crossing(x, y2, level=0.5), 0.0)
    
    y3 = np.array([0.0, 0.1, 0.2, 0.3])
    assert np.isnan(_interp_crossing(x, y3, level=0.5))
    
    assert _interp_crossing(np.array([]), np.array([]), level=0.5) is None

def test_interp_crossing_unsorted():
    """Verify that _interp_crossing handles unsorted input grids correctly."""
    # Unsorted input x
    x = np.array([2.0, 0.0, 3.0, 1.0])
    y = np.array([0.8, 0.0, 1.0, 0.2])
    # Sorted order would be x=[0.0, 1.0, 2.0, 3.0], y=[0.0, 0.2, 0.8, 1.0]
    # Level 0.5 crossing should occur at 1.5
    crossing = _interp_crossing(x, y, level=0.5)
    assert np.isclose(crossing, 1.5)

def test_analyze_sweep_index_reconstruction():
    """Verify that analyze_sweep correctly reconstructs missing indices using math.isclose."""
    raw_data = {
        "metadata": {
            "n": 100, "p": 0.05, "r": 2, "concentration": 50.0, "theta": 0.5,
            "window_len": 1, "weights": None, "trials_per_cell": 2, "base_seed": 42
        },
        "sweep_parameters": {
            "mean_fear_grid": [0.0, 0.3, 0.6],
            "seed_multiples": [0.5, 1.0],
            "seed_size_grid": [2, 4]
        },
        "results": [
            {"mean_fear": 0.300000000001, "seed_multiple": 1.0, "seed_size": 4, "failed_fractions": [0.0, 0.6], "rounds_completed": [1, 2]},
            {"mean_fear": 0.0, "seed_multiple": 0.5, "seed_size": 2, "failed_fractions": [0.0, 0.0], "rounds_completed": [1, 1]}
        ]
    }
    
    res = analyze_sweep(raw_data)
    assert len(res["processed_cells"]) == 2
    # Verify that it matched mean_fear 0.300000000001 to canonical grid key "0.3"
    assert "0.3" in res["empirical_thresholds"]
    assert "0.300000000001" not in res["empirical_thresholds"]

def test_evaluate_scaling_adherence_missing_baseline():
    """Verify that evaluate_scaling_adherence raises ValueError when mu=0 baseline is missing or invalid."""
    # Scenario 1: mu=0 baseline is missing entirely
    analyzed_data_missing = {
        "metadata": {"r": 2, "n": 1000, "p": 0.01, "theta": 0.5},
        "empirical_thresholds": {
            "0.1": 8.0,
            "0.2": 6.0
        },
        "processed_cells": [{"seed_size": 3}]
    }
    with pytest.raises(ValueError, match="CRITICAL: mu=0 baseline is missing or invalid"):
        evaluate_scaling_adherence(analyzed_data_missing)

    # Scenario 2: mu=0 baseline is invalid (closest is 0.05, which is > 1e-9)
    analyzed_data_invalid = {
        "metadata": {"r": 2, "n": 1000, "p": 0.01, "theta": 0.5},
        "empirical_thresholds": {
            "0.05": 9.0,
            "0.1": 8.0
        },
        "processed_cells": [{"seed_size": 3}]
    }
    with pytest.raises(ValueError, match="CRITICAL: mu=0 baseline is missing or invalid"):
        evaluate_scaling_adherence(analyzed_data_invalid)

def test_evaluate_scaling_adherence_clamping_mask():
    """Verify that rows satisfying a_emp <= min_seed_size are masked."""
    # N=1000, p=0.01, r=2 -> a_c(0) = 5.0.
    # We set min_seed_size = 3.
    analyzed_data = {
        "metadata": {"r": 2, "n": 1000, "p": 0.01, "theta": 0.5},
        "empirical_thresholds": {
            "0.0": 10.0,   # Valid (a_emp = 10 > 3)
            "0.2": 6.0,    # Valid (a_emp = 6 > 3)
            "0.4": 2.0,    # Clamped (a_emp = 2 <= 3)
            "0.5": 4.0     # Valid (a_emp = 4 > 3, no longer masked by predicted_ac = 1.25 < 3)
        },
        "processed_cells": [
            {"seed_size": 3},
            {"seed_size": 5}
        ]
    }
    res = evaluate_scaling_adherence(analyzed_data)
    results = {row["mu"]: row for row in res["results_table"]}
    
    assert not results[0.0]["is_clamped"]
    assert results[0.0]["ratio_emp"] is not None
    assert results[0.0]["diff"] is not None
    
    assert not results[0.2]["is_clamped"]
    assert results[0.2]["ratio_emp"] is not None
    assert results[0.2]["diff"] is not None

    assert results[0.4]["is_clamped"]
    assert results[0.4]["ratio_emp"] is None
    assert results[0.4]["diff"] is None

    assert not results[0.5]["is_clamped"]
    assert results[0.5]["ratio_emp"] is not None
    assert results[0.5]["diff"] is not None

def test_evaluate_scaling_adherence_stats_exclusion():
    """Verify that summary statistics run exclusively across valid, unconstrained data points, and return None if empty."""
    # Case 1: Some valid, some clamped
    analyzed_data_mixed = {
        "metadata": {"r": 2, "n": 1000, "p": 0.01, "theta": 0.5},
        "empirical_thresholds": {
            "0.0": 10.0,  # Valid (ratio_emp = 1.0, ratio_theory = 1.0, diff = 0.0)
            "0.2": 8.0,   # Valid (ratio_emp = 0.8, ratio_theory = 0.64, diff = 0.16)
            "0.5": 2.0    # Clamped
        },
        "processed_cells": [{"seed_size": 3}]
    }
    res_mixed = evaluate_scaling_adherence(analyzed_data_mixed)
    # Diffs for valid rows are [0.0, 0.16]. Max(|diff|) = 0.16, Mean(|diff|) = 0.08.
    assert np.isclose(res_mixed["max_diff"], 0.16)
    assert np.isclose(res_mixed["mean_diff"], 0.08)

    # Case 2: All clamped
    # If min_seed_size = 12, then both mu=0 and mu=0.2 are clamped because their a_emp <= 12.
    analyzed_data_all_clamped = {
        "metadata": {"r": 2, "n": 1000, "p": 0.01, "theta": 0.5},
        "empirical_thresholds": {
            "0.0": 10.0,
            "0.2": 8.0
        },
        "processed_cells": [{"seed_size": 12}]
    }
    res_all_clamped = evaluate_scaling_adherence(analyzed_data_all_clamped)
    assert res_all_clamped["max_diff"] is None
    assert res_all_clamped["mean_diff"] is None
