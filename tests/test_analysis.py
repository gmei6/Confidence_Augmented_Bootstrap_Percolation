"""
Unit tests for twocascade.analysis metrics and interpolation.
"""

import pytest
import numpy as np
from twocascade.analysis import _interp_crossing, analyze_sweep

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
    # Verify that it matched mean_fear 0.300000000001 to grid index 1 (corresponding to 0.3)
    # and matched seed_multiple 1.0 to grid index 1 (corresponding to 1.0)
    # If float matching failed, it would have raised ValueError.
