"""
Integration and edge cases tests for twocascade runner, analysis, and fear boundaries.
"""

import os
import json
import pytest
import numpy as np

from twocascade.runner import run_sweep, serialize_graph_to_json
from twocascade.analysis import analyze_sweep, load_raw_results
from twocascade.reference import sample_individual_fears, choose_seed, sample_gnp_adjacency

def test_sweep_and_analysis_integration(tmp_path):
    """Run a micro-sweep and verify that runner and analysis integrate correctly."""
    config_data = {
      "pinned_params": {
        "n": 50,
        "r": 2,
        "concentration": 50.0, 
        "theta": 0.5,
        "window_len": 1,
        "weights": None,
        "target_high_degree": False
      },
      "scaling": {
        "n_ref": 50,
        "target_mean_degree": 4.0,
        "alpha": 0.7
      },
      "sweep": {
        "mean_fear_grid": [0.0, 0.3],
        "seed_multiples": [0.8, 1.2],
        "trials_per_cell": 3,
        "base_seed": 42
      },
      "output": {
        "raw_filepath": str(tmp_path / "sweep_test_raw.json")
      }
    }
    
    config_path = tmp_path / "test_config.json"
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=2)
        
    # Run the sweep
    run_sweep(str(config_path), num_processes=1)
    
    # Check output exists
    assert os.path.exists(config_data["output"]["raw_filepath"])
    
    # Load and check JSON structure
    raw_results = load_raw_results(config_data["output"]["raw_filepath"])
    assert "metadata" in raw_results
    assert "results" in raw_results
    assert len(raw_results["results"]) == 4 # 2 mus * 2 multiples
    
    # Check index mapping is present
    for cell in raw_results["results"]:
        assert "mean_fear_idx" in cell
        assert "seed_multiple_idx" in cell
        assert len(cell["failed_fractions"]) == 3
        
    # Run analysis
    analysis_results = analyze_sweep(raw_results)
    assert "metadata" in analysis_results
    assert "processed_cells" in analysis_results
    assert len(analysis_results["processed_cells"]) == 4
    
    # Verify linear crossing calculations don't crash
    assert "crossings_mu" in analysis_results
    assert "empirical_thresholds" in analysis_results


def test_fear_channel_boundaries():
    """Verify boundary conditions for sample_individual_fears at mu = 0 and mu = 1."""
    rng = np.random.default_rng(123)
    n = 100
    
    # At mu = 0, all fears must be exactly 0
    fears_zero = sample_individual_fears(n, mean_fear=0.0, concentration=10.0, rng=rng)
    assert all(f == 0.0 for f in fears_zero)
    
    # At mu = 1, all fears must be exactly 1
    fears_one = sample_individual_fears(n, mean_fear=1.0, concentration=10.0, rng=rng)
    assert all(f == 1.0 for f in fears_one)


def test_targeted_seeding():
    """Verify that choose_seed with target_high_degree=True targets nodes with higher degrees."""
    rng = np.random.default_rng(999)
    n = 20
    p = 0.3
    
    # Sample a random graph
    adj = sample_gnp_adjacency(n, p, rng)
    
    # Find the degrees of all nodes
    degrees = [len(neighbors) for neighbors in adj]
    
    # Pick seed of size 3 targeted vs random
    seed_targeted = choose_seed(n, seed_size=3, adjacency=adj, rng=rng, target_high_degree=True)
    seed_random = choose_seed(n, seed_size=3, adjacency=adj, rng=rng, target_high_degree=False)
    
    # Check that degrees of targeted nodes are sorted in descending order
    targeted_degrees = [degrees[idx] for idx in seed_targeted]
    sorted_degrees = sorted(degrees, reverse=True)
    
    # The targeted seeds must be the highest degree nodes
    assert targeted_degrees == sorted_degrees[:3]


def test_graph_serialization(tmp_path):
    """Verify graph serialization outputs valid JSON list of lists."""
    adj = [[1, 2], [0], [0]]
    out_path = str(tmp_path / "graph.json")
    serialize_graph_to_json(adj, out_path)
    
    assert os.path.exists(out_path)
    with open(out_path, "r") as f:
        loaded = json.load(f)
    assert loaded == adj


def test_fear_only_channel_terminates():
    """Verify that under p=0.0 (empty graph/disconnected), the fear-only channel behaves subcritically and halts quickly."""
    from twocascade.reference import make_nodes, run_cascade
    rng = np.random.default_rng(777)
    n = 200
    p = 0.0 # disconnected graph
    
    adj = sample_gnp_adjacency(n, p, rng)
    # E[f] = mu = 0.5 < 1.0 (subcritical)
    fears = sample_individual_fears(n, mean_fear=0.5, concentration=50.0, rng=rng)
    nodes = make_nodes(fears)
    
    # 5 seed failures. Since there are no edges, solvency channel does nothing.
    # The failures can only spread via the fear channel.
    seed_indices = choose_seed(n, seed_size=5, adjacency=adj, rng=rng, target_high_degree=False)
    
    result = run_cascade(adj, nodes, r=2, seed_indices=seed_indices, rng=rng, record_history=True)
    
    # Fear-only per-round offspring is mu * g_t = 0.5 * (a_{t-1}/n).
    # Since it is a subcritical branching process, it must terminate in o(n) steps with final failed fraction << 1.0 w.h.p.
    # For N=200, 5 seeds, it should terminate in a few rounds and fail only a handful of nodes.
    assert result.final_failed_fraction < 0.20, f"Failed too many nodes in fear-only sweep: {result.final_failed_fraction}"
    assert len(result.history) < 10, f"Branching process ran too long: {result.history}"
