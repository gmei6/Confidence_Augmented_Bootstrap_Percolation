# To run:
# python3 -m pytest tests/test_mu0_bootstrap_threshold.py -v  

"""
Week-1 validation -- mu = 0 reduces to Janson bootstrap percolation on G(n,p).

Goal (tracker section 6, Wk-1; section 2 North Star): confirm the reference
engine's EMPIRICAL seed threshold matches the ANALYTICAL a_c of Janson, Luczak,
Turova & Vallier (2012) (tracker section 4). At mu = 0 every individual fear
f_i = 0, the fear channel never fires, and the dynamics are exactly the
absolute-threshold rule "fail if >= r neighbors have failed." This is the one
milestone that depends on NO open modeling fork (F1/F2/F4 are all fear-channel
choices), which is why it is the right first thing to lock down.

Janson's sharp threshold (r >= 2, density window  1/n << p << n^{-1/r}):
    a < a_c  ->  subcritical:   final failed set is o(n), in fact A* < r/(r-1) * a
    a > a_c  ->  supercritical:  A* = n - o(n)   (near-complete percolation)
with  a_c = (1 - 1/r) * t_c   and   t_c = ((r-1)! / (n p^r))^{1/(r-1)}.

Reproducibility (tracker sections 5.4 / 5.6): the run is deterministic given
(config, seed). The assertions encode the theory with generous finite-n margins,
so the test is meaningful but not flaky.

Run:  pytest tests/test_mu0_bootstrap_threshold.py -v
"""

from __future__ import annotations

import math

import numpy as np

from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)


# --------------------------------------------------------------------------- #
# Analytical benchmark (Janson et al. 2012) -- tracker section 4.
# Closed form on purpose: this test does NOT import your model.py, so it doubles
# as an independent cross-check of that formula.
# --------------------------------------------------------------------------- #
def t_c(n: int, p: float, r: int) -> float:
    """Critical time-scale  t_c = ((r-1)! / (n p^r))^{1/(r-1)}."""
    return (math.factorial(r - 1) / (n * p ** r)) ** (1.0 / (r - 1))


def a_c(n: int, p: float, r: int) -> float:
    """Critical seed size  a_c = (1 - 1/r) * t_c."""
    return (1.0 - 1.0 / r) * t_c(n, p, r)


def phi_subcritical(alpha: float, r: int) -> float:
    """
    Asymptotic subcritical final size in units of t_c (A* ~ phi * t_c), where phi
    solves  r*phi - phi^r = (r-1)*alpha  with  alpha = a / a_c. Closed form r=2.
    """
    if r == 2:
        return 1.0 - math.sqrt(max(0.0, 1.0 - alpha))
    raise NotImplementedError("Closed form given for r=2; solve numerically for r>2.")


# --------------------------------------------------------------------------- #
# >>> ADAPTER: wired to src/twocascade/reference.py. <<<
# --------------------------------------------------------------------------- #
def final_failed_fraction(
    n: int, p: float, r: int, mu: float, a: int, rng: np.random.Generator) -> float:
    """
    Run ONE cascade and return |A*| / n. At mu = 0 the fear channel is off.

    Pipeline mirrors reference.estimate_systemic_probability for a single trial:
    sample G(n,p) -> draw fears -> build nodes -> pick a RANDOM seed of size `a`
    (section 3.1 default; Janson's theorem is for random seeds) -> run one cascade.
    """
    adjacency = sample_gnp_adjacency(n, p, rng)
    # concentration is irrelevant at mu = 0 (sample_individual_fears short-circuits
    # to an all-zero vector), but it is validated as > 0 *before* that branch, so we
    # must pass a positive placeholder. Any value works; the fears come back all-zero.
    fears = sample_individual_fears(n, mean_fear=mu, concentration=1.0, rng=rng)
    nodes = make_nodes(fears)
    seed_indices = choose_seed(
        n, seed_size=a, adjacency=adjacency, rng=rng, target_high_degree=False
    )
    result = run_cascade(
        adjacency, nodes, r=r, seed_indices=seed_indices, rng=rng, record_history=False
    )
    return result.final_failed_fraction


# --------------------------------------------------------------------------- #
# Configuration. r = 2 is the cleanest threshold (closed-form phi). With BETA
# FROZEN (calibrated once at N_REF) and 1/r < ALPHA < 1, p = BETA * N**(-ALPHA)
# sits strictly inside the window  1/n << p << 1/sqrt(n)  as N -> infinity,
# because np = BETA * N**(1-ALPHA) grows. (Pinning BETA to the live N instead
# would cancel ALPHA and collapse this to np = const, the lower edge.)
# At N = 4000:  1/n = 2.5e-4  <  p = 2.5e-3  <  1/sqrt(n) = 1.58e-2   ('<', a finite-N
# spacing of specific numbers -- not '<<', which is the asymptotic statement above).
# One cascade is ~milliseconds (tracker section 5.2), so the suite stays fast.
# Bump N and N_REALIZATIONS to tighten the empirical-threshold bracket.
# --------------------------------------------------------------------------- #
SEED = 20260603
R = 2
N = 4000

N_REF = 4000                                          # size at which mean degree is calibrated
ALPHA = 0.7                                           # 1/r < ALPHA < 1  ->  p interior to the window
TARGET_MEAN_DEGREE = 10.0
BETA  = TARGET_MEAN_DEGREE / N_REF ** (1.0 - ALPHA)   # FROZEN -- calibrated once at N_REF
P = BETA * N ** (-ALPHA)                              # np = BETA * N**(1-ALPHA): grows as N leaves N_REF

N_REALIZATIONS = 200
THETA = 0.5              # systemic-event threshold for locating the crossing


def _fractions(a: int, rng: np.random.Generator, reps: int = N_REALIZATIONS) -> np.ndarray:
    """`reps` independent mu=0 cascades at seed size `a`; returns their |A*|/n."""
    return np.array([final_failed_fraction(N, P, R, 0.0, a, rng) for _ in range(reps)])


def _interp_crossing(x: np.ndarray, y: np.ndarray, level: float):
    """First x where (roughly increasing) y crosses `level`, linearly interpolated."""
    if y[0] >= level:
        return float(x[0])
    for i in range(1, len(y)):
        if y[i - 1] < level <= y[i]:
            t = (level - y[i - 1]) / (y[i] - y[i - 1])
            return float(x[i - 1] + t * (x[i] - x[i - 1]))
    return None


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_mu0_run_is_reproducible():
    """Tracker 5.4: deterministic given (config, seed). Identical seeds -> identical
    outcome (at mu=0 there are no stochastic draws beyond graph + seed selection)."""
    a = max(R, round(a_c(N, P, R)))
    f1 = final_failed_fraction(N, P, R, 0.0, a, np.random.default_rng(SEED))
    f2 = final_failed_fraction(N, P, R, 0.0, a, np.random.default_rng(SEED))
    assert f1 == f2, f"mu=0 not reproducible under a fixed seed: {f1} != {f2}"


def test_deep_subcritical_stays_small():
    """a = 0.5 a_c stays subcritical: final fraction is tiny and obeys the Janson
    bound  A* < r/(r-1) a = 2a  (with finite-n slack)."""
    rng = np.random.default_rng(SEED)
    ac = a_c(N, P, R)
    a = max(R, round(0.5 * ac))
    fr = _fractions(a, rng)

    alpha = a / ac
    expected_count = phi_subcritical(alpha, R) * t_c(N, P, R)   # theory: A* ~ phi * t_c
    q90_count = float(np.percentile(fr, 90)) * N

    assert np.median(fr) < 0.02, (
        f"median subcritical fraction {np.median(fr):.4f} too large "
        f"(theory ~{expected_count / N:.4f})"
    )
    # Janson subcritical bound A* < 2a for r=2; 1.25x slack absorbs finite-n noise.
    assert q90_count < 2.5 * a, f"90th-pctile A* = {q90_count:.1f} violates ~2a bound (a={a})"


def test_deep_supercritical_percolates():
    """a = 2 a_c is well above threshold -> near-complete percolation, A* = n - o(n)."""
    rng = np.random.default_rng(SEED + 2)
    a = max(R, round(2.0 * a_c(N, P, R)))
    fr = _fractions(a, rng)
    assert np.median(fr) > 0.9, f"median supercritical fraction only {np.median(fr):.3f}"


def test_empirical_threshold_matches_a_c():
    """
    Sharper check: locate the seed where P(A*/n >= theta) crosses 0.5 and confirm
    it lands near the analytical a_c. Finite n smears and slightly shifts the
    transition, so the bracket is deliberately generous; tighten N / N_REALIZATIONS
    to narrow it. The (seed, P_systemic) pairs here are also the raw material for
    the Wk-2 bimodality histograms.
    """
    rng = np.random.default_rng(SEED + 1)
    ac = a_c(N, P, R)
    multiples = [0.5, 0.7, 0.85, 1.0, 1.15, 1.3, 1.6, 2.0]
    seeds = [max(R, round(m * ac)) for m in multiples]

    p_systemic = np.array([float(np.mean(_fractions(a, rng) >= THETA)) for a in seeds])

    a_emp = _interp_crossing(np.array(seeds, dtype=float), p_systemic, level=0.5)
    assert a_emp is not None, f"P(systemic) never crossed 0.5 across the sweep: {p_systemic}"

    ratio = a_emp / ac
    assert 0.6 <= ratio <= 1.8, (
        f"empirical threshold {a_emp:.1f} vs analytical a_c {ac:.1f} (ratio {ratio:.2f}); "
        f"P(systemic) over seeds {seeds} = {np.round(p_systemic, 3)}"
    )