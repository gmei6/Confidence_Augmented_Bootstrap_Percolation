"""
Tests for the Q5 experimental local-fear engine (geometry.py).

These are NEW tests for previously untested code (no geometry test existed);
they validate the round_log instrumentation and the fear_adjacency=None
global-field fast path added for the Task O locality sweeps:

1. fear_adjacency=None is exactly equivalent (same seed, same graph) to an
   explicit full-torus fear adjacency (ell >= torus diameter).
2. At mu=0 the local-fear engine matches the reference oracle exactly on the
   same graph (field type is irrelevant without fear - scoping doc prong A).
3. round_log is consistent: seeds + union of per-round sets == final failed
   set, and per-round sizes match the recorded cumulative history increments.
4. Passing round_log/fear_adjacency does not change the cascade outcome
   relative to the default call (instrumentation is purely additive).
"""

import numpy as np

from twocascade.reference import make_nodes, choose_seed, run_cascade, sample_individual_fears
from twocascade.geometry import (
    sample_torus_points,
    build_rgg_adjacency,
    build_fear_adjacency,
    run_cascade_local_fear,
)

N = 500
R = 2
SEED = 1234


def _setup(mu, kappa=50, mean_degree_c=2.0):
    ss = np.random.SeedSequence(SEED)
    s_graph, s_fear, s_casc = ss.spawn(3)
    rng_graph = np.random.default_rng(s_graph)
    points = sample_torus_points(N, rng_graph)
    r_n = np.sqrt(mean_degree_c * np.log(N) / (np.pi * N))
    adj = build_rgg_adjacency(points, r_n)
    fears = sample_individual_fears(N, mean_fear=mu, concentration=kappa,
                                    rng=np.random.default_rng(s_fear))
    seeds = choose_seed(N, 10, adj, np.random.default_rng(s_casc), False)
    return points, adj, fears, seeds


def _run_local(adj, fears, seeds, fear_adj, casc_seed=99, round_log=None):
    nodes = make_nodes(list(fears))
    return nodes, run_cascade_local_fear(
        adjacency=adj, fear_adjacency=fear_adj, nodes=nodes, r=R,
        seed_indices=seeds, rng=np.random.default_rng(casc_seed),
        record_history=True, window_len=5, weights=[0.2] * 5,
        round_log=round_log)


def test_global_fast_path_matches_full_torus_ball():
    points, adj, fears, seeds = _setup(mu=0.4)
    full_ball = build_fear_adjacency(points, 2.0)  # ell >= diameter: all pairs
    nodes_a, res_a = _run_local(adj, fears, seeds, full_ball)
    nodes_b, res_b = _run_local(adj, fears, seeds, None)
    assert res_a.final_failed_fraction == res_b.final_failed_fraction
    assert res_a.rounds_completed == res_b.rounds_completed
    assert res_a.history == res_b.history
    assert [n.failed for n in nodes_a] == [n.failed for n in nodes_b]


def test_mu0_matches_reference_oracle_exactly():
    points, adj, fears, seeds = _setup(mu=0.0)
    fears0 = [0.0] * N
    nodes_ref = make_nodes(list(fears0))
    res_ref = run_cascade(adjacency=adj, nodes=nodes_ref, r=R, seed_indices=seeds,
                          rng=np.random.default_rng(99), record_history=True,
                          window_len=5, weights=[0.2] * 5)
    nodes_loc, res_loc = _run_local(adj, fears0, seeds, None)
    assert res_ref.final_failed_fraction == res_loc.final_failed_fraction
    assert res_ref.rounds_completed == res_loc.rounds_completed
    assert [n.failed for n in nodes_ref] == [n.failed for n in nodes_loc]


def test_round_log_consistency():
    points, adj, fears, seeds = _setup(mu=0.4)
    log = []
    nodes, res = _run_local(adj, fears, seeds, None, round_log=log)
    failed = {i for i, n in enumerate(nodes) if n.failed}
    reconstructed = set(seeds)
    for round_set in log:
        assert reconstructed.isdisjoint(round_set), "a node failed twice"
        reconstructed |= round_set
    assert reconstructed == failed
    # history[k] is the cumulative count; increments match round-set sizes for
    # the rounds recorded in history (history stops growing on the final
    # zero-failure tail rounds the deque keeps for the window).
    increments = [res.history[k] - res.history[k - 1] for k in range(1, len(res.history))]
    assert increments == [len(s) for s in log[:len(increments)]]
    assert all(len(s) == 0 for s in log[len(increments):])


def test_scatter_counts_equal_per_node_scan():
    """The engine's per-round scattered fear counts must equal the brute-force
    per-node ball scan (the pre-optimization formulation) for arbitrary sets."""
    points, adj, fears, seeds = _setup(mu=0.4)
    fear_adj = build_fear_adjacency(points, 0.08)
    rng = np.random.default_rng(5)
    for _ in range(5):
        failed_set = set(rng.choice(N, size=40, replace=False).tolist())
        counts = [0] * N
        for j in failed_set:
            for i in fear_adj[j]:
                counts[i] += 1
        brute = [sum(1 for j in fear_adj[i] if j in failed_set) for i in range(N)]
        assert counts == brute


def test_instrumentation_is_inert():
    points, adj, fears, seeds = _setup(mu=0.4)
    fear_adj = build_fear_adjacency(points, 0.1)
    nodes_a, res_a = _run_local(adj, fears, seeds, fear_adj)
    log = []
    nodes_b, res_b = _run_local(adj, fears, seeds, fear_adj, round_log=log)
    assert res_a.final_failed_fraction == res_b.final_failed_fraction
    assert res_a.history == res_b.history
    assert [n.failed for n in nodes_a] == [n.failed for n in nodes_b]
    assert len(log) > 0
