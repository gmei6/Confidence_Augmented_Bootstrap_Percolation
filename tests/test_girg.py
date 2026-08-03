"""Tests for the indexed GIRG sampler against the preserved O(n^2) reference.

Bit-exact agreement is impossible and is deliberately not asserted anywhere here.
The reference draws one `rng.random()` per ordered pair in index order; any
sub-quadratic sampler consumes the stream differently, so the same seed cannot
give the same graph. What must agree is the DISTRIBUTION, and that is what these
tests check.

The one exception is `test_complete_graph_coverage`, which is exact rather than
statistical: driving every connection probability to 1 turns the sampler into a
pure enumeration of pairs, so the output must be the complete graph. That single
test is what pins down the partition — a missed pair shows up as a missing edge
and a double-visited pair as a duplicate, and neither can hide behind a random
draw. It is the cheapest and sharpest test in the file.
"""

import math

import numpy as np
import pytest

from twocascade.girg import (
    sample_girg_adjacency,
    sample_powerlaw_weights,
    sample_torus_points,
)

# Written on overnight/2026-08-02-ec9d736a against the BKL bucket-index port,
# whose oracle was named sample_girg_adjacency_reference. The merge kept C1's
# block-vectorized sampler instead (s-024 resolution); its oracle is the same
# pre-port loop under the name sample_girg_adjacency_slow, so the alias keeps
# every oracle comparison below intact.
from twocascade.girg import sample_girg_adjacency_slow as sample_girg_adjacency_reference

ALPHA = 1.0
TAU = 2.5
# Chosen so the graphs come out sparse (<k> around 9-12), which is the regime the
# poster's comparison actually runs in. Dense graphs would hide a sampler that
# mishandles long range, because in a dense graph almost everything connects.
W_MIN = 0.245


def _edge_count(adj):
    return sum(len(a) for a in adj) // 2


def _instance(n, seed):
    rng = np.random.default_rng(seed)
    points = sample_torus_points(n, rng)
    weights = sample_powerlaw_weights(n, TAU, W_MIN, rng)
    return points, weights


def _torus_dist_sq(points, i, j):
    dx = abs(points[i, 0] - points[j, 0])
    dy = abs(points[i, 1] - points[j, 1])
    dx = min(dx, 1.0 - dx)
    dy = min(dy, 1.0 - dy)
    return dx * dx + dy * dy


# --- exact structure ---------------------------------------------------------


@pytest.mark.parametrize("n", [2, 3, 5, 17, 64, 200, 999])
def test_complete_graph_coverage(n):
    """Every pair is visited exactly once — no gaps, no double-counting.

    Weights this large make the connection probability saturate at 1 for every
    pair at every distance, so the sampled graph must be exactly complete. A
    partition that drops a cell pair loses edges; one that visits a cell pair
    twice gives those pairs two independent chances to connect, which appears
    here as a duplicate entry.
    """
    rng = np.random.default_rng(1)
    points = sample_torus_points(n, rng)
    weights = np.full(n, 1e9)
    adj = sample_girg_adjacency(points, weights, ALPHA, rng)

    assert len(adj) == n
    for i, neighbours in enumerate(adj):
        assert len(neighbours) == n - 1, "vertex %d has degree %d, expected %d" % (
            i, len(neighbours), n - 1)
        assert len(set(neighbours)) == len(neighbours), "duplicate edge at vertex %d" % i
        assert i not in neighbours


@pytest.mark.parametrize("n", [0, 1])
def test_degenerate_sizes(n):
    rng = np.random.default_rng(3)
    points = sample_torus_points(n, rng)
    weights = np.full(n, 1.0)
    assert sample_girg_adjacency(points, weights, ALPHA, rng) == [[] for _ in range(n)]


def test_coincident_points_are_skipped_exactly_as_the_reference_skips_them():
    """dist_sq == 0 is a `continue` in the reference, not a probability-1 edge."""
    points = np.array([[0.25, 0.25], [0.25, 0.25], [0.25, 0.25], [0.75, 0.75]])
    weights = np.full(4, 1e9)

    adj = sample_girg_adjacency(points, weights, ALPHA, np.random.default_rng(7))
    ref = sample_girg_adjacency_reference(points, weights, ALPHA, np.random.default_rng(7))

    # The three coincident vertices connect to vertex 3 (distance > 0, p == 1)
    # and to nothing else. Both implementations must agree exactly here, because
    # with p saturated at 1 there is no randomness left to differ over.
    assert sorted(adj[0]) == [3]
    assert sorted(adj[1]) == [3]
    assert sorted(adj[2]) == [3]
    assert sorted(adj[3]) == [0, 1, 2]
    assert [sorted(a) for a in adj] == [sorted(a) for a in ref]


def test_output_is_a_symmetric_simple_graph():
    points, weights = _instance(400, 11)
    adj = sample_girg_adjacency(points, weights, ALPHA, np.random.default_rng(12))

    assert len(adj) == 400
    for i, neighbours in enumerate(adj):
        assert i not in neighbours, "self-loop at %d" % i
        assert len(set(neighbours)) == len(neighbours), "duplicate neighbour at %d" % i
        for j in neighbours:
            assert i in adj[j], "edge %d-%d is not symmetric" % (i, j)


# --- distributional agreement ------------------------------------------------


def test_edge_count_matches_reference():
    """Mean edge count agrees, to a tolerance derived from the observed spread.

    Both samplers are run on the SAME points and weights for each seed, so the
    only difference between the two sets of counts is the sampling algorithm.
    The tolerance is four standard errors of the difference in means, computed
    from the samples themselves — not a constant picked until the test passed.
    """
    n, seeds = 500, 8
    ref_counts, new_counts = [], []
    for s in range(seeds):
        points, weights = _instance(n, 200 + s)
        ref_counts.append(_edge_count(
            sample_girg_adjacency_reference(points, weights, ALPHA, np.random.default_rng(5000 + s))))
        new_counts.append(_edge_count(
            sample_girg_adjacency(points, weights, ALPHA, np.random.default_rng(9000 + s))))

    ref_counts = np.array(ref_counts, dtype=float)
    new_counts = np.array(new_counts, dtype=float)
    diff = abs(new_counts.mean() - ref_counts.mean())
    se = math.sqrt(ref_counts.var(ddof=1) / seeds + new_counts.var(ddof=1) / seeds)
    tolerance = 4.0 * se

    assert ref_counts.mean() > 0
    assert diff <= tolerance, (
        "mean edge count %.1f vs reference %.1f; difference %.1f exceeds 4 SE = %.1f"
        % (new_counts.mean(), ref_counts.mean(), diff, tolerance))


def test_edge_probability_matches_reference_at_every_distance():
    """The long-range tail, which is the whole reason this port is delicate.

    A sampler that only examines nearby cells can match the total edge count
    while producing no long edges at all, so a count-only test would pass it.
    Here edges are binned by torus distance and compared against the reference
    bin by bin, with the denominator (pairs available in each bin) identical for
    both because they run on the same point set.
    """
    n, seeds = 300, 6
    n_bins = 6
    edges_ref = np.zeros(n_bins)
    edges_new = np.zeros(n_bins)
    pairs = np.zeros(n_bins)

    # Bin on squared torus distance. Max squared distance on the unit torus is
    # 0.5 (both axes at 0.5), and the bins are linear in d rather than d^2 so the
    # far bins hold most of the pairs.
    edges_of_bin = np.linspace(0.0, math.sqrt(0.5), n_bins + 1)

    for s in range(seeds):
        points, weights = _instance(n, 300 + s)
        d = np.array([[math.sqrt(_torus_dist_sq(points, i, j)) for j in range(n)] for i in range(n)])
        iu = np.triu_indices(n, 1)
        pairs += np.histogram(d[iu], bins=edges_of_bin)[0]

        for impl, acc, seed in ((sample_girg_adjacency_reference, edges_ref, 6000 + s),
                                (sample_girg_adjacency, edges_new, 7000 + s)):
            adj = impl(points, weights, ALPHA, np.random.default_rng(seed))
            dists = [d[i, j] for i, nb in enumerate(adj) for j in nb if j > i]
            acc += np.histogram(dists, bins=edges_of_bin)[0]

    assert pairs.min() > 0, "every distance bin must contain pairs to compare"

    far = edges_of_bin[-2]
    assert edges_ref[-1] > 0, "reference produced no edges beyond d=%.2f — bad fixture" % far
    assert edges_new[-1] > 0, (
        "the indexed sampler produced NO edges in the farthest distance bin (d > %.2f) while the "
        "reference produced %d. That is the signature of a truncating spatial index." % (far, edges_ref[-1]))

    for b in range(n_bins):
        if edges_ref[b] + edges_new[b] < 30:
            continue  # too few edges in this bin for the comparison to say anything
        # Poisson-ish: the standard deviation of each count is about its square
        # root, so four sigma on the difference is 4*sqrt(ref + new).
        tol = 4.0 * math.sqrt(edges_ref[b] + edges_new[b])
        assert abs(edges_new[b] - edges_ref[b]) <= tol, (
            "distance bin %d (d in [%.3f, %.3f]): %d edges vs reference %d, difference exceeds "
            "4 sigma = %.1f" % (b, edges_of_bin[b], edges_of_bin[b + 1],
                                edges_new[b], edges_ref[b], tol))


def test_degree_distribution_matches_reference():
    """Heavy-tailed degrees: the max degree is where a bad weight bound shows up.

    Grouping points by weight layer inside each cell exists so that one very
    heavy vertex cannot inflate the acceptance bound for its whole cell. If that
    grouping were dropped the mean would survive and the tail would not.
    """
    n, seeds = 400, 6
    ref_deg, new_deg = [], []
    for s in range(seeds):
        points, weights = _instance(n, 400 + s)
        ref_deg += [len(a) for a in
                    sample_girg_adjacency_reference(points, weights, ALPHA, np.random.default_rng(8000 + s))]
        new_deg += [len(a) for a in
                    sample_girg_adjacency(points, weights, ALPHA, np.random.default_rng(8500 + s))]

    ref_deg = np.array(ref_deg, dtype=float)
    new_deg = np.array(new_deg, dtype=float)

    se = math.sqrt(ref_deg.var(ddof=1) / len(ref_deg) + new_deg.var(ddof=1) / len(new_deg))
    assert abs(new_deg.mean() - ref_deg.mean()) <= 4.0 * se, (
        "mean degree %.3f vs reference %.3f (4 SE = %.3f)"
        % (new_deg.mean(), ref_deg.mean(), 4.0 * se))

    for q in (50, 90, 99):
        r = np.percentile(ref_deg, q)
        v = np.percentile(new_deg, q)
        assert abs(v - r) <= 0.25 * max(r, 1.0), (
            "p%d degree %.1f vs reference %.1f — the tail disagrees" % (q, v, r))
