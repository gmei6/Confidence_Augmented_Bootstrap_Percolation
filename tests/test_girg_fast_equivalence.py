"""Gate test for the C1 GIRG sampler port. Written before implementation.

This test is not the implementer's to edit. If an assertion looks wrong, stop
and say which one and why instead of changing it.

Requires girg.py to expose, after the port:
  - sample_girg_adjacency       (new, fast, exact)
  - sample_girg_adjacency_slow  (the pre-port O(n^2) loop, kept verbatim)
"""
import numpy as np
import pytest

from twocascade.girg import (
    sample_torus_points,
    sample_powerlaw_weights,
    sample_girg_adjacency,
    sample_girg_adjacency_slow,
)

ALPHA_G = 1.2
TAU = 2.5
W_MIN = 1.0


def _make_inputs(n, seed):
    rng = np.random.default_rng(seed)
    pts = sample_torus_points(n, rng)
    w = sample_powerlaw_weights(n, TAU, W_MIN, rng)
    return pts, w


def _edge_set(adj):
    return {(i, j) for i, nbrs in enumerate(adj) for j in nbrs if i < j}


def _stats(sampler, n, seeds):
    edge_counts, mean_degs, hists = [], [], []
    for s in seeds:
        pts, w = _make_inputs(n, s)
        adj = sampler(pts, w, ALPHA_G, np.random.default_rng(s + 10_000))
        e = _edge_set(adj)
        degs = np.array([len(a) for a in adj])
        edge_counts.append(len(e))
        mean_degs.append(degs.mean())
        hists.append(np.bincount(np.minimum(degs, 20), minlength=21))
    return np.array(edge_counts), np.array(mean_degs), np.sum(hists, axis=0)


def test_determinism_and_invariants():
    n = 500
    pts, w = _make_inputs(n, 7)
    a1 = sample_girg_adjacency(pts, w, ALPHA_G, np.random.default_rng(42))
    a2 = sample_girg_adjacency(pts, w, ALPHA_G, np.random.default_rng(42))
    assert [sorted(x) for x in a1] == [sorted(x) for x in a2], "not deterministic given seed"
    for i, nbrs in enumerate(a1):
        assert i not in nbrs, "self-loop"
        assert len(nbrs) == len(set(nbrs)), "duplicate edge in adjacency list"
        for j in nbrs:
            assert i in a1[j], "asymmetric adjacency"


def test_statistical_equivalence_with_slow_sampler():
    n = 400
    seeds_old = range(100, 130)
    seeds_new = range(200, 230)
    ec_old, md_old, hist_old = _stats(sample_girg_adjacency_slow, n, seeds_old)
    ec_new, md_new, hist_new = _stats(sample_girg_adjacency, n, seeds_new)

    # Edge-count agreement: difference of means within 4 combined standard errors.
    se = np.sqrt(ec_old.var(ddof=1) / len(ec_old) + ec_new.var(ddof=1) / len(ec_new))
    assert abs(ec_old.mean() - ec_new.mean()) < 4.0 * se, (
        f"edge counts diverge: old {ec_old.mean():.1f} vs new {ec_new.mean():.1f}, se {se:.2f}")

    se_d = np.sqrt(md_old.var(ddof=1) / len(md_old) + md_new.var(ddof=1) / len(md_new))
    assert abs(md_old.mean() - md_new.mean()) < 4.0 * se_d, (
        f"mean degree diverges: old {md_old.mean():.3f} vs new {md_new.mean():.3f}")

    # Degree-histogram shape: chi-square on pooled counts (bins with expected >= 5).
    tot_old, tot_new = hist_old.sum(), hist_new.sum()
    mask = (hist_old + hist_new) >= 10
    p_pool = (hist_old + hist_new)[mask] / (tot_old + tot_new)
    exp_old, exp_new = p_pool * tot_old, p_pool * tot_new
    chi2 = float(np.sum((hist_old[mask] - exp_old) ** 2 / exp_old)
                 + np.sum((hist_new[mask] - exp_new) ** 2 / exp_new))
    dof = int(mask.sum()) - 1
    # chi2 threshold ~ dof + 4*sqrt(2*dof): far beyond noise only on real divergence.
    assert chi2 < dof + 4.0 * np.sqrt(2.0 * dof), (
        f"degree histogram diverges: chi2 {chi2:.1f} vs dof {dof}")


class _ConstantRng:
    """Stub generator: random() always returns c, so an edge appears iff p > c.
    Comparing fast-vs-slow edge sets across c compares per-pair probability
    level sets directly — deterministic, and sensitive to cross-block edge loss
    and small multiplicative errors that the statistical test cannot see."""

    def __init__(self, c):
        self.c = c

    def random(self, size=None):
        if size is None:
            return self.c
        return np.full(size, self.c)


def test_multiblock_level_set_identity():
    """n=1300 spans three 512-row blocks (uneven last). Guards the block
    partitioning itself: a sampler that drops or double-counts cross-block
    pairs, or shifts p by a constant factor, fails this exactly."""
    n = 1300
    pts, w = _make_inputs(n, 11)
    for c in (1e-6, 0.3, 0.9):
        e_fast = _edge_set(sample_girg_adjacency(pts, w, ALPHA_G, _ConstantRng(c)))
        e_slow = _edge_set(sample_girg_adjacency_slow(pts, w, ALPHA_G, _ConstantRng(c)))
        assert e_fast == e_slow, (
            f"level-set mismatch at c={c}: "
            f"fast-only {len(e_fast - e_slow)}, slow-only {len(e_slow - e_fast)}")


def test_slow_sampler_is_verbatim_pre_port():
    """The slow sampler must still produce the pre-port distribution: spot-check
    one small graph against a hand-rolled reimplementation of the original loop."""
    n = 60
    pts, w = _make_inputs(n, 3)
    rng = np.random.default_rng(9)
    adj = sample_girg_adjacency_slow(pts, w, ALPHA_G, rng)
    rng2 = np.random.default_rng(9)
    adj2 = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dx = abs(pts[i, 0] - pts[j, 0]); dx = min(dx, 1.0 - dx)
            dy = abs(pts[i, 1] - pts[j, 1]); dy = min(dy, 1.0 - dy)
            d2 = dx * dx + dy * dy
            if d2 == 0:
                continue
            p = min(1.0, (w[i] * w[j] / (n * d2)) ** ALPHA_G)
            if rng2.random() < p:
                adj2[i].append(j)
                adj2[j].append(i)
    assert adj == adj2, "sample_girg_adjacency_slow is not the verbatim pre-port loop"
