import pytest
import math
import numpy as np
from collections import deque
from twocascade.reference import (
    Node,
    CascadeResult,
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)

def test_input_validation():
    """Ensure invalid inputs for window_len and weights raise ValueError."""
    rng = np.random.default_rng(42)
    adj = [[1], [0]]
    nodes = [Node(0, 0.5), Node(1, 0.5)]
    seeds = [0]
    
    # window_len < 1
    with pytest.raises(ValueError, match="window_len must be >= 1"):
        run_cascade(adj, nodes, r=2, seed_indices=seeds, rng=rng, record_history=False, window_len=0)
        
    # weights length mismatch
    with pytest.raises(ValueError, match="Length of weights"):
        run_cascade(adj, nodes, r=2, seed_indices=seeds, rng=rng, record_history=False, window_len=3, weights=[0.5, 0.5])
        
    # negative weights
    with pytest.raises(ValueError, match="non-negative"):
        run_cascade(adj, nodes, r=2, seed_indices=seeds, rng=rng, record_history=False, window_len=2, weights=[1.5, -0.5])
        
    # weights do not sum to 1.0
    with pytest.raises(ValueError, match="sum to 1.0"):
        run_cascade(adj, nodes, r=2, seed_indices=seeds, rng=rng, record_history=False, window_len=2, weights=[0.6, 0.6])


def test_equivalence_window_len_1():
    """Verify window_len=1 behaves identically to the default baseline (backward compatibility)."""
    n = 100
    p = 0.1
    r = 2
    
    for seed in range(5):
        # We must use separate isolated RNGs inside run_cascade so they start with identical state
        trial_rng = np.random.default_rng(seed)
        adj = sample_gnp_adjacency(n, p, trial_rng)
        fears = sample_individual_fears(n, mean_fear=0.3, concentration=10.0, rng=trial_rng)
        seeds = choose_seed(n, seed_size=10, adjacency=adj, rng=trial_rng, target_high_degree=False)
        
        # Test default
        nodes_default = make_nodes(fears)
        cascade_rng_1 = np.random.default_rng(seed + 1000)
        result_default = run_cascade(adj, nodes_default, r=r, seed_indices=seeds, rng=cascade_rng_1, record_history=True)
        
        # Test explicit window_len=1
        nodes_explicit = make_nodes(fears)
        cascade_rng_2 = np.random.default_rng(seed + 1000)
        result_explicit = run_cascade(adj, nodes_explicit, r=r, seed_indices=seeds, rng=cascade_rng_2, record_history=True, window_len=1)
        
        assert result_default.final_failed_fraction == result_explicit.final_failed_fraction
        assert result_default.total_failed == result_explicit.total_failed
        assert result_default.rounds_completed == result_explicit.rounds_completed
        assert result_default.history == result_explicit.history


def test_delta_impulse_invariance():
    """Verify that window_len=X with weights=[1.0, 0.0, ...] is identical to window_len=1."""
    n = 100
    p = 0.1
    r = 2
    
    for window_len in [2, 4]:
        weights = [1.0] + [0.0] * (window_len - 1)
        
        for seed in range(5):
            trial_rng = np.random.default_rng(seed)
            adj = sample_gnp_adjacency(n, p, trial_rng)
            fears = sample_individual_fears(n, mean_fear=0.3, concentration=10.0, rng=trial_rng)
            seeds = choose_seed(n, seed_size=10, adjacency=adj, rng=trial_rng, target_high_degree=False)
            
            # Baseline (window_len = 1)
            nodes_base = make_nodes(fears)
            cascade_rng_1 = np.random.default_rng(seed + 1000)
            result_base = run_cascade(
                adj, nodes_base, r=r, seed_indices=seeds, rng=cascade_rng_1, record_history=True,
                window_len=1, weights=[1.0]
            )
            
            # Delta impulse (window_len = X)
            nodes_delta = make_nodes(fears)
            cascade_rng_2 = np.random.default_rng(seed + 1000)
            result_delta = run_cascade(
                adj, nodes_delta, r=r, seed_indices=seeds, rng=cascade_rng_2, record_history=True,
                window_len=window_len, weights=weights
            )
            
            assert result_base.final_failed_fraction == result_delta.final_failed_fraction
            assert result_base.total_failed == result_delta.total_failed
            assert result_base.rounds_completed == result_delta.rounds_completed
            assert result_base.history == result_delta.history


def test_boundary_shocks():
    """Verify immediate halts and correct values on empty and complete shock boundaries."""
    rng = np.random.default_rng(300)
    n = 10
    adj = sample_gnp_adjacency(n, p=0.3, rng=rng)
    fears = sample_individual_fears(n, mean_fear=0.5, concentration=5.0, rng=rng)
    
    for window_len in [1, 3]:
        # Empty shock (seed_size = 0)
        nodes_empty = make_nodes(fears)
        res_empty = run_cascade(adj, nodes_empty, r=2, seed_indices=[], rng=rng, record_history=True, window_len=window_len)
        assert res_empty.total_failed == 0
        assert res_empty.rounds_completed == 0
        assert res_empty.history == [0]
        
        # Complete shock (seed_size = n)
        nodes_full = make_nodes(fears)
        res_full = run_cascade(adj, nodes_full, r=2, seed_indices=list(range(n)), rng=rng, record_history=True, window_len=window_len)
        assert res_full.total_failed == n
        assert res_full.rounds_completed == 0
        assert res_full.history == [n]


def test_primes_precision():
    """Ensure uniform weights sum correctly on prime window lengths without floating point issues."""
    rng = np.random.default_rng(400)
    adj = [[1], [0]]
    nodes = [Node(0, 0.5), Node(1, 0.5)]
    seeds = [0]
    
    result = run_cascade(adj, nodes, r=2, seed_indices=seeds, rng=rng, record_history=False, window_len=7, weights=None)
    assert result is not None


def test_multi_window_dynamics():
    """
    Verify that window_len > 1 holds the process active during a quiet round (0 failures),
    and successfully triggers subsequent failures in the window.
    """
    # Deterministic line graph:
    # 0 - 1 - 2 - 3
    # plus helper node 4 for solvency, node 5 isolated
    adj = [
        [1],        # 0 (seed)
        [0, 4, 2],  # 1 (fails by solvency r=2 in Round 1 since 0 and 4 are seeds)
        [1, 3],     # 2 (solvency r=2 prevents solvency failure; fails by fear in Round 3)
        [2],        # 3 (stays solvent)
        [1],        # 4 (seed)
        []          # 5 (isolated)
    ]
    
    # We want Node 2 to fail in Round 3 due to fear.
    # Node 2 has individual_fear = 1.0, Node 3 has 0.0.
    
    # Seed finding for the RNG:
    # Round 1: Node 2 fear prob = 0.1111. Needs RNG draw > 0.1111 to NOT fail.
    # Round 2: Node 2 fear prob = 0.1667. Needs RNG draw > 0.1667 to NOT fail.
    # Round 3: Node 2 fear prob = 0.1667. Needs RNG draw < 0.1667 to fail.
    found_seed = None
    for s in range(5000):
        test_rng = np.random.default_rng(s)
        d1 = test_rng.random()
        d2 = test_rng.random()
        d3 = test_rng.random()
        if d1 > 0.15 and d2 > 0.2 and d3 < 0.15:
            found_seed = s
            break
            
    assert found_seed is not None, "Could not find a valid seed"
    
    test_rng = np.random.default_rng(found_seed)
    nodes = [
        Node(index=0, individual_fear=0.0),
        Node(index=1, individual_fear=0.0),
        Node(index=2, individual_fear=1.0),
        Node(index=3, individual_fear=0.0),
        Node(index=4, individual_fear=0.0),
        Node(index=5, individual_fear=0.0)
    ]
    
    res = run_cascade(adj, nodes, r=2, seed_indices=[0, 4], rng=test_rng, record_history=True, window_len=3)
    
    assert res.total_failed == 4
    assert res.rounds_completed == 5
    assert res.history == [2, 3, 3, 4, 4, 4]
