"""Cross-language validation: C++ GIRG engine vs Python oracle (cpp-girg-plan G5).

Sibling to tests/test_cpp_validation.py (the gnp §5.4 harness), following its
exact structure and calibration conventions, extended for the cpp-girg-plan's
own parity-scope table (implementation_plan.md). Five checks, each covering a
DIFFERENT failure mode -- none substitutes for another (a sampler with a
truncated long-range tail could pass the aggregate statistics while failing
the distance-binned check; a cascade-logic bug could pass the sampler checks
while failing Prong A):

  1. Exact per-pair probability (deterministic): C++ p_ij == Python p_ij to
     double precision, on shared points/weights.
  2. Sampled-graph statistics (statistical): edge count, degree histogram,
     distance-binned edges -- C++ sampler (both variants) vs the Python oracle
     `sample_girg_adjacency` (C1), under real RNG.
  3. Level-set identity (deterministic, constant-c RNG stub): edge sets at
     fixed thresholds c. Holds EXACTLY at every c for the direct kernel (a
     literal per-pair threshold test, like the oracle itself). For the BKL
     sampler it holds exactly only where every visited cell-pair group
     saturates (p_bar >= 1, the exact-enumeration branch); once p_bar < 1,
     bkl's geometric-skip branch accepts a candidate pair iff
     u.next() < exact_p(i,j)/p_bar, which -- since p_bar < 1 by construction
     of that branch -- is PROVABLY WEAKER than the direct/oracle condition
     u.next() < exact_p(i,j) at the same constant u, for ANY c, including c
     close to 1: a pair with a tiny absolute exact_p can still cross a high c
     if its ratio to its own group's (necessarily larger) upper bound is high
     enough. So bkl is checked against a small BOUNDED symmetric difference
     at high c, not exact equality (see
     test_bkl_level_set_identity_matches_oracle_at_high_threshold below for
     a concrete counterexample pair found while building this test, and
     cpp/tests/test_girg.cpp's identically-scoped, identically-corrected
     C++-only test). This is a twice-corrected scope relative to RISKS.md
     #1's original assumption ("agrees at literally every threshold c"),
     documented rather than silently narrowed: check #2 above covers the
     non-saturating regime statistically, and test_bkl_complete_graph_coverage
     in the C++ suite covers the p_bar>=1 regime exactly and deterministically.
  4. Prong A (deterministic cascade logic, mu=0): final failed set on a
     GIRG-shaped graph, identical node-for-node between languages. Uses the
     existing --dump-failed-set / load_graph_from_file machinery completely
     unchanged -- it is graph-content-agnostic by construction.
  5. Prong B (statistical cascade parity, mu>0): P(systemic) via two-proportion
     z-test, |A*|/n via KS, both compared by p-value (not a fixed distance
     cutoff -- okf/lessons.md's flag against exactly that, already the
     convention test_cpp_validation.py's Prong B uses).

Run after building the C++ engine:
    cd cpp && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make
Tests are skipped (not failed) if the binary is absent.
"""

from __future__ import annotations

import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy import stats

from twocascade.girg import sample_torus_points, sample_powerlaw_weights, sample_girg_adjacency
from twocascade.reference import make_nodes, choose_seed, run_cascade
from twocascade.graphs import sample_degree_dependent_fears

# --------------------------------------------------------------------------- #
# Locations & constants
# --------------------------------------------------------------------------- #

REPO_ROOT = Path(__file__).resolve().parent.parent
CPP_BIN = REPO_ROOT / "cpp" / "build" / "twocascade_run"
DUMP_GEOMETRY_SCRIPT = REPO_ROOT / "scripts" / "dump_girg_reference.py"
DUMP_CASCADE_SCRIPT = REPO_ROOT / "scripts" / "dump_girg_cascade_reference.py"

TAU = 2.5
W_MIN = 0.245
ALPHA_G = 1.2
THETA = 0.5
Z_TEST_MIN_PVALUE = 0.005  # matches test_cpp_validation.py's calibration
SUBPROCESS_TIMEOUT = 600

requires_cpp_binary = pytest.mark.skipif(
    not CPP_BIN.exists(),
    reason=f"C++ engine not built at {CPP_BIN}; build cpp/ in Release mode first",
)


def _subprocess_env() -> dict:
    env = dict(os.environ)
    src = str(REPO_ROOT / "src")
    env["PYTHONPATH"] = src + os.pathsep + env.get("PYTHONPATH", "")
    env["OMP_NUM_THREADS"] = "1"
    return env


def _run_cpp(args: list[str]) -> str:
    result = subprocess.run(
        [str(CPP_BIN)] + args,
        capture_output=True,
        text=True,
        timeout=SUBPROCESS_TIMEOUT,
        env=_subprocess_env(),
    )
    assert result.returncode == 0, (
        f"C++ engine exited with {result.returncode}.\nargs: {args}\nstderr: {result.stderr}"
    )
    return result.stdout


def _dump_geometry(tmp_path: Path, n: int, base_seed: int) -> Path:
    out_dir = tmp_path / "girg_geometry"
    proc = subprocess.run(
        [
            sys.executable, str(DUMP_GEOMETRY_SCRIPT),
            "--n", str(n), "--tau", str(TAU), "--w-min", str(W_MIN),
            "--alpha-g", str(ALPHA_G), "--base-seed", str(base_seed),
            "--out", str(out_dir),
        ],
        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
        env=_subprocess_env(), cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, f"dump_girg_reference.py failed:\n{proc.stderr}"
    return out_dir


def _load_points_weights(out_dir: Path) -> tuple[np.ndarray, np.ndarray]:
    points = np.loadtxt(out_dir / "points.txt")
    weights = np.loadtxt(out_dir / "weights.txt")
    return points, weights


def _edge_set_from_lines(text: str) -> set[tuple[int, int]]:
    edges = set()
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        i, j = map(int, line.split())
        edges.add((i, j))
    return edges


class _ConstantRng:
    """Mirrors tests/test_girg_fast_equivalence.py's stub: random() always
    returns c, so an edge appears iff p > c."""

    def __init__(self, c):
        self.c = c

    def random(self, size=None):
        return self.c if size is None else np.full(size, self.c)


# --------------------------------------------------------------------------- #
# 1. Exact per-pair probability (deterministic)
# --------------------------------------------------------------------------- #


@requires_cpp_binary
def test_exact_probability_matches_python_formula(tmp_path):
    """C++ p_ij must equal an independent Python computation of the SAME
    formula to double-precision tolerance, on shared points/weights. This is
    checkable exactly (no RNG involved) precisely because the model's formula
    is simple enough to duplicate correctly on both sides."""
    n = 150
    out_dir = _dump_geometry(tmp_path, n, base_seed=7)
    points, weights = _load_points_weights(out_dir)

    probs_file = tmp_path / "probs_cpp.txt"
    _run_cpp([
        "--girg-verify", "probabilities",
        "--points-file", str(out_dir / "points.txt"),
        "--weights-file", str(out_dir / "weights.txt"),
        "--alpha-g", str(ALPHA_G),
        "--output", str(probs_file),
    ])

    max_diff = 0.0
    count = 0
    for line in probs_file.read_text().splitlines():
        i, j, p_cpp = line.split()
        i, j, p_cpp = int(i), int(j), float(p_cpp)
        dx = abs(points[i, 0] - points[j, 0]); dx = min(dx, 1.0 - dx)
        dy = abs(points[i, 1] - points[j, 1]); dy = min(dy, 1.0 - dy)
        d2 = dx * dx + dy * dy
        p_py = 0.0 if d2 == 0.0 else min(1.0, (weights[i] * weights[j] / (n * d2)) ** ALPHA_G)
        max_diff = max(max_diff, abs(p_py - p_cpp))
        count += 1

    assert count == n * (n - 1) // 2, f"expected {n*(n-1)//2} pairs, got {count}"
    assert max_diff < 1e-9, f"max |p_py - p_cpp| = {max_diff:.3e} exceeds double-precision tolerance"


# --------------------------------------------------------------------------- #
# 2. Sampled-graph statistics (statistical)
# --------------------------------------------------------------------------- #


@requires_cpp_binary
@pytest.mark.parametrize("variant", ["direct", "bkl"])
def test_sampled_graph_statistics_match_oracle(variant, tmp_path):
    """Edge count, degree histogram, and distance-binned edge counts must
    agree (statistically -- RNG streams differ across languages by design)
    between the C++ sampler and the Python oracle `sample_girg_adjacency`, on
    the SAME points/weights. The distance-binned check specifically catches a
    truncating spatial index -- an aggregate edge-count match alone cannot
    (RISKS.md #2 / implementation_plan.md's parity-table footnote). The
    degree-histogram check catches a bad acceptance bound in the BKL sampler:
    if a group's p_bar were ever LESS than some member pair's exact p, that
    pair's edge probability is silently truncated to p_bar, which costs the
    heaviest vertices their highest-probability edges -- a tail deficit that
    moves the degree distribution while the total edge count can still land
    inside its own tolerance.

    All three checks are calibrated per okf/lessons.md: the degree histogram is
    compared by p-value (per-bin Welch t-test with a Bonferroni correction over
    bins), never by a fixed distance cutoff. The independent replicate unit is
    the GRAPH, not the node: with points/weights held fixed across seeds, node
    degrees within one graph are correlated, so pooling all n*n_seeds degrees
    into one two-sample test would badly understate the variance and make this
    flaky. Per-graph bin counts are genuinely independent across seeds."""
    n = 500
    # 40 replicate graphs, not the 8 this test shipped with. Calibrated by
    # mutation testing during the G5.1 fix round, not guessed: with the BKL
    # acceptance bound deliberately halved (p_bar *= 0.5 -- an invalid,
    # too-small bound, which truncates every pair whose exact p exceeds it), 12
    # replicates left the degree-histogram check silent, while 40 catch it at
    # p = 6e-5 in the heavy-degree tail bin [10, inf) -- the exact bin and
    # failure mode this check exists for. Each replicate is one Python graph
    # plus one cheap C++ subprocess at n=500; 40 of them cost ~2s.
    n_seeds = 40
    out_dir = _dump_geometry(tmp_path, n, base_seed=300)
    points, weights = _load_points_weights(out_dir)

    py_edge_counts, cpp_edge_counts = [], []
    py_deg_samples, cpp_deg_samples = [], []  # one degree array per graph
    n_bins = 6
    edges_of_bin = np.linspace(0.0, math.sqrt(0.5), n_bins + 1)
    d_all = np.array([
        [math.sqrt(min(abs(points[i, 0] - points[j, 0]), 1 - abs(points[i, 0] - points[j, 0])) ** 2
                   + min(abs(points[i, 1] - points[j, 1]), 1 - abs(points[i, 1] - points[j, 1])) ** 2)
         for j in range(n)] for i in range(n)
    ])
    py_dist_hist = np.zeros(n_bins)
    cpp_dist_hist = np.zeros(n_bins)

    for s in range(n_seeds):
        py_rng = np.random.default_rng(9000 + s)
        adj_py = sample_girg_adjacency(points, weights, ALPHA_G, py_rng)
        edges_py = {(i, j) for i, nbrs in enumerate(adj_py) for j in nbrs if i < j}
        py_edge_counts.append(len(edges_py))
        py_deg_samples.append(np.array([len(a) for a in adj_py], dtype=int))
        py_dist_hist += np.histogram([d_all[i, j] for (i, j) in edges_py], bins=edges_of_bin)[0]

        stdout = _run_cpp([
            "--girg-verify", "sample",
            "--points-file", str(out_dir / "points.txt"),
            "--weights-file", str(out_dir / "weights.txt"),
            "--alpha-g", str(ALPHA_G),
            "--girg-variant", variant,
            "--rng-source", "real",
            "--base-seed", str(9500 + s),
        ])
        edges_cpp = _edge_set_from_lines(stdout)
        cpp_edge_counts.append(len(edges_cpp))
        deg = np.zeros(n, dtype=int)
        for (i, j) in edges_cpp:
            deg[i] += 1
            deg[j] += 1
        cpp_deg_samples.append(deg)
        cpp_dist_hist += np.histogram([d_all[i, j] for (i, j) in edges_cpp], bins=edges_of_bin)[0]

    py_edge_counts = np.array(py_edge_counts, dtype=float)
    cpp_edge_counts = np.array(cpp_edge_counts, dtype=float)
    se = math.sqrt(py_edge_counts.var(ddof=1) / n_seeds + cpp_edge_counts.var(ddof=1) / n_seeds)
    diff = abs(py_edge_counts.mean() - cpp_edge_counts.mean())
    assert diff <= 4.0 * se, (
        f"[{variant}] mean edge count {cpp_edge_counts.mean():.1f} vs oracle "
        f"{py_edge_counts.mean():.1f}; diff {diff:.1f} exceeds 4 SE = {4.0*se:.1f}"
    )

    # --- degree histogram -------------------------------------------------- #
    # Bin edges come from the ORACLE's pooled degrees (quantiles, deduped
    # because GIRG degrees are small integers with heavy ties at the low end),
    # so the binning adapts to the fixture instead of hardcoding a distribution
    # shape. The last bin is open-ended: it is the heavy-degree tail, which is
    # the bin a broken acceptance bound damages first.
    py_pooled = np.concatenate(py_deg_samples)
    deg_edges = np.unique(np.quantile(py_pooled, [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]))
    deg_edges = np.append(deg_edges, np.inf)
    assert len(deg_edges) >= 4, (
        f"degenerate degree binning ({deg_edges}) -- bad fixture, not a sampler failure"
    )
    n_deg_bins = len(deg_edges) - 1

    py_deg_hist = np.array([np.histogram(d, bins=deg_edges)[0] for d in py_deg_samples], dtype=float)
    cpp_deg_hist = np.array([np.histogram(d, bins=deg_edges)[0] for d in cpp_deg_samples], dtype=float)

    # Bonferroni over bins keeps the family-wise false-positive rate at the same
    # Z_TEST_MIN_PVALUE the rest of the cross-language suite is calibrated to.
    per_bin_alpha = Z_TEST_MIN_PVALUE / n_deg_bins
    for b in range(n_deg_bins):
        py_col, cpp_col = py_deg_hist[:, b], cpp_deg_hist[:, b]
        if py_col.sum() + cpp_col.sum() < 30:
            continue  # bin too sparse for a mean comparison to say anything
        if py_col.var(ddof=1) == 0.0 and cpp_col.var(ddof=1) == 0.0:
            # Both languages put a deterministic count here; a t-test is
            # undefined, so compare directly.
            assert py_col[0] == cpp_col[0], (
                f"[{variant}] degree bin {b} [{deg_edges[b]:g},{deg_edges[b+1]:g}) is "
                f"deterministic but differs: C++ {cpp_col[0]:.0f} vs oracle {py_col[0]:.0f}"
            )
            continue
        t_res = stats.ttest_ind(py_col, cpp_col, equal_var=False)
        assert t_res.pvalue > per_bin_alpha, (
            f"[{variant}] degree histogram differs beyond Monte Carlo error in bin {b} "
            f"[{deg_edges[b]:g},{deg_edges[b+1]:g}): per-graph mean count "
            f"C++ {cpp_col.mean():.1f} vs oracle {py_col.mean():.1f} "
            f"(t = {t_res.statistic:.3f}, p = {t_res.pvalue:.5f} <= "
            f"{per_bin_alpha:.5f} = {Z_TEST_MIN_PVALUE}/{n_deg_bins} Bonferroni)"
        )

    # Total degree mass is a hard identity, not a statistic: every graph's
    # degrees must sum to 2m for that same graph. A binning that silently
    # dropped nodes would make the p-value checks above vacuous.
    for s in range(n_seeds):
        assert py_deg_samples[s].sum() == 2 * py_edge_counts[s]
        assert cpp_deg_samples[s].sum() == 2 * cpp_edge_counts[s]

    # --- distance-binned edges --------------------------------------------- #
    far = edges_of_bin[-2]
    assert py_dist_hist[-1] > 0, "oracle produced no far-bin edges -- bad fixture"
    assert cpp_dist_hist[-1] > 0, (
        f"[{variant}] C++ sampler produced NO edges beyond d={far:.2f} while the oracle "
        f"produced {py_dist_hist[-1]:.0f} -- signature of a truncating spatial index"
    )
    for b in range(n_bins):
        total = py_dist_hist[b] + cpp_dist_hist[b]
        if total < 30:
            continue
        tol = 4.0 * math.sqrt(total)
        assert abs(cpp_dist_hist[b] - py_dist_hist[b]) <= tol, (
            f"[{variant}] distance bin {b} [{edges_of_bin[b]:.3f},{edges_of_bin[b+1]:.3f}): "
            f"{cpp_dist_hist[b]:.0f} vs oracle {py_dist_hist[b]:.0f}, exceeds 4-sigma tol {tol:.1f}"
        )


# --------------------------------------------------------------------------- #
# 3. Level-set identity (deterministic, constant-c RNG stub)
# --------------------------------------------------------------------------- #


@requires_cpp_binary
@pytest.mark.parametrize("c", [1e-6, 0.3, 0.9])
def test_direct_level_set_identity_matches_oracle_at_every_threshold(c, tmp_path):
    """The direct kernel (Variant A) is a literal per-pair threshold test,
    exactly like the oracle -- so this must hold at EVERY c, not just high
    ones (contrast with the bkl variant test below)."""
    n = 200
    out_dir = _dump_geometry(tmp_path, n, base_seed=11)
    points, weights = _load_points_weights(out_dir)

    adj_py = sample_girg_adjacency(points, weights, ALPHA_G, _ConstantRng(c))
    edges_py = {(i, j) for i, nbrs in enumerate(adj_py) for j in nbrs if i < j}

    stdout = _run_cpp([
        "--girg-verify", "sample",
        "--points-file", str(out_dir / "points.txt"),
        "--weights-file", str(out_dir / "weights.txt"),
        "--alpha-g", str(ALPHA_G),
        "--girg-variant", "direct",
        "--rng-source", "constant",
        "--constant-c", str(c),
    ])
    edges_cpp = _edge_set_from_lines(stdout)

    assert edges_cpp == edges_py, (
        f"c={c}: direct-kernel level-set mismatch; cpp-only {len(edges_cpp - edges_py)}, "
        f"py-only {len(edges_py - edges_cpp)}"
    )


@requires_cpp_binary
@pytest.mark.parametrize("c", [0.9, 0.95, 0.99])
def test_bkl_level_set_identity_matches_oracle_at_high_threshold(c, tmp_path):
    """BKL's geometric-skip branch accepts a candidate pair iff
    u.next() < exact_p(i,j)/p_bar. Since p_bar < 1 by construction of that
    branch, exact_p/p_bar > exact_p for any exact_p > 0 -- so this accept
    condition is PROVABLY WEAKER than the oracle's direct
    u.next() < exact_p(i,j) at the same constant c, for ANY c, including c
    close to 1. Concretely, at n=200/c=0.9 (this fixture, base_seed=11) bkl
    produces one spurious edge (132,173) with exact_p ~ 0.054 whose group's
    p_bar ~ 0.060 pushes the ratio just over 0.9 -- confirmed by hand while
    building this test, not a partition bug. A doubled or dropped cell pair
    (a REAL partition bug) instead produces a large, systematic difference
    (thousands of edges at low c, per G2's investigation), so a small bound
    here still catches that failure mode without asserting a false
    exact-equality guarantee. The p_bar>=1-forced regime, where equality IS
    exact and guaranteed, is covered separately and deterministically by
    cpp/tests/test_girg.cpp's test_bkl_complete_graph_coverage."""
    n = 200
    out_dir = _dump_geometry(tmp_path, n, base_seed=11)
    points, weights = _load_points_weights(out_dir)

    adj_py = sample_girg_adjacency(points, weights, ALPHA_G, _ConstantRng(c))
    edges_py = {(i, j) for i, nbrs in enumerate(adj_py) for j in nbrs if i < j}

    stdout = _run_cpp([
        "--girg-verify", "sample",
        "--points-file", str(out_dir / "points.txt"),
        "--weights-file", str(out_dir / "weights.txt"),
        "--alpha-g", str(ALPHA_G),
        "--girg-variant", "bkl",
        "--rng-source", "constant",
        "--constant-c", str(c),
    ])
    edges_cpp = _edge_set_from_lines(stdout)

    max_symmetric_diff = 3  # small and fixed, not tuned per-c to pass
    symmetric_diff = len(edges_cpp - edges_py) + len(edges_py - edges_cpp)
    assert symmetric_diff <= max_symmetric_diff, (
        f"c={c}: bkl level-set mismatch too large ({symmetric_diff} edges; "
        f"cpp-only {len(edges_cpp - edges_py)}, py-only {len(edges_py - edges_cpp)}) "
        f"-- this exceeds what the ratio-branch boundary effect alone explains "
        f"and may indicate a partition bug"
    )


# --------------------------------------------------------------------------- #
# 4. Prong A -- deterministic cascade logic equivalence at mu = 0
# --------------------------------------------------------------------------- #


PRONG_A_GIRG_CASES = [
    # (n, r, seed_size, base_seed)
    pytest.param(2000, 2, 20, 0, id="n2000-r2"),
    pytest.param(500, 4, 10, 42, id="n500-r4"),
]


@requires_cpp_binary
@pytest.mark.parametrize("n,r,seed_size,base_seed", PRONG_A_GIRG_CASES)
def test_prong_a_girg_failed_sets_identical(n, r, seed_size, base_seed, tmp_path):
    """C++ final failed set on a GIRG-shaped graph must equal the Python
    oracle's, node for node. Uses the existing --dump-failed-set /
    load_graph_from_file machinery completely unchanged -- it never needed to
    know the graph came from GIRG."""
    out_dir = tmp_path / "girg_cascade"
    dump = subprocess.run(
        [
            sys.executable, str(DUMP_CASCADE_SCRIPT),
            "--n", str(n), "--tau", str(TAU), "--w-min", str(W_MIN),
            "--alpha-g", str(ALPHA_G), "--r", str(r),
            "--seed-size", str(seed_size), "--base-seed", str(base_seed),
            "--out", str(out_dir),
        ],
        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
        env=_subprocess_env(), cwd=REPO_ROOT,
    )
    assert dump.returncode == 0, f"dump_girg_cascade_reference.py failed:\n{dump.stderr}"

    stdout = _run_cpp([
        "--graph-file", str(out_dir / "graph.txt"),
        "--seed-file", str(out_dir / "seed.txt"),
        "--dump-failed-set",
        "--mu", "0",
        "--r", str(r),
    ])

    cpp_failed = sorted(int(tok) for tok in stdout.split())
    py_failed = sorted(int(tok) for tok in (out_dir / "failed.txt").read_text().split())

    assert cpp_failed == py_failed, (
        f"Failed sets differ: C++ has {len(cpp_failed)} nodes, Python has {len(py_failed)} nodes.\n"
        f"C++ only: {sorted(set(cpp_failed) - set(py_failed))[:20]}\n"
        f"Python only: {sorted(set(py_failed) - set(cpp_failed))[:20]}"
    )


# --------------------------------------------------------------------------- #
# 5. Prong B -- statistical cascade parity at mu > 0
# --------------------------------------------------------------------------- #

# Calibrated (via a 30-trial pilot run during G5 implementation, not tuned to
# pass the final test) so P(systemic) sits away from 0/1: seed_size=3 at
# n=2000 gave P(final_failed_fraction >= THETA) ~ 0.2-0.4 across mu in
# [0.1, 0.3] with kappa=50 -- an interior regime, not a trivial phase.
PRONG_B_GIRG_PARAMS = dict(n=2000, r=2, mu=0.2, seed_size=3)
N_TRIALS_GIRG = 300
PRONG_B_GIRG_PY_SEED = 24601
PRONG_B_GIRG_CPP_SEED = 24601


def _python_girg_fractions(kappa: float) -> np.ndarray:
    P = {**PRONG_B_GIRG_PARAMS, "kappa": kappa}
    rng = np.random.default_rng(PRONG_B_GIRG_PY_SEED)
    fractions = np.empty(N_TRIALS_GIRG)
    for t in range(N_TRIALS_GIRG):
        points = sample_torus_points(P["n"], rng)
        weights = sample_powerlaw_weights(P["n"], TAU, W_MIN, rng)
        adjacency = sample_girg_adjacency(points, weights, ALPHA_G, rng)
        # gamma=0.0: degree-dependent fear reduces exactly to the global model
        # (this task's scope; see implementation_plan.md).
        fears, _stats = sample_degree_dependent_fears(weights, P["mu"], 0.0, P["kappa"], rng)
        nodes = make_nodes(individual_fears=fears)
        seeds = choose_seed(
            n=P["n"], seed_size=P["seed_size"], adjacency=adjacency, rng=rng,
            target_high_degree=False,
        )
        result = run_cascade(
            adjacency=adjacency, nodes=nodes, r=P["r"], seed_indices=seeds,
            rng=rng, record_history=False,
        )
        fractions[t] = result.final_failed_fraction
    return fractions


def _cpp_girg_fractions(kappa: float) -> np.ndarray:
    P = {**PRONG_B_GIRG_PARAMS, "kappa": kappa}
    stdout = _run_cpp([
        "--graph-type", "girg", "--tau", str(TAU), "--w-min", str(W_MIN), "--alpha-g", str(ALPHA_G),
        "--n", str(P["n"]), "--r", str(P["r"]),
        "--mu", str(P["mu"]), "--kappa", str(kappa),
        "--seed-size", str(P["seed_size"]),
        "--trials", str(N_TRIALS_GIRG),
        "--base-seed", str(PRONG_B_GIRG_CPP_SEED),
    ])
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    assert len(lines) == N_TRIALS_GIRG, f"expected {N_TRIALS_GIRG} lines, got {len(lines)}"
    return np.array([float(ln.split()[0]) for ln in lines])


_girg_fractions_cache = {}


def _get_girg_fractions(kappa: float) -> tuple[np.ndarray, np.ndarray]:
    if kappa not in _girg_fractions_cache:
        if not CPP_BIN.exists():
            pytest.skip(f"C++ engine not built at {CPP_BIN}")
        _girg_fractions_cache[kappa] = (_python_girg_fractions(kappa), _cpp_girg_fractions(kappa))
    return _girg_fractions_cache[kappa]


@requires_cpp_binary
@pytest.mark.parametrize("kappa", [10.0, 50.0])
def test_prong_b_girg_systemic_probability_z_test(kappa):
    py_fracs, cpp_fracs = _get_girg_fractions(kappa)
    x1 = int(np.sum(py_fracs >= THETA))
    x2 = int(np.sum(cpp_fracs >= THETA))
    n1 = n2 = N_TRIALS_GIRG
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)

    if pooled == 0.0 or pooled == 1.0:
        assert p1 == p2
        return

    se = math.sqrt(pooled * (1.0 - pooled) * (1.0 / n1 + 1.0 / n2))
    z = (p1 - p2) / se
    p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z)))
    assert p_value > Z_TEST_MIN_PVALUE, (
        f"P(systemic) differs beyond Monte Carlo error for kappa={kappa}: "
        f"Python {p1:.3f} vs C++ {p2:.3f} (z = {z:.3f}, p = {p_value:.5f})"
    )


@requires_cpp_binary
@pytest.mark.parametrize("kappa", [10.0, 50.0])
def test_prong_b_girg_failed_fraction_ks_distance(kappa):
    py_fracs, cpp_fracs = _get_girg_fractions(kappa)
    ks = stats.ks_2samp(py_fracs, cpp_fracs)
    # p-value form, not a fixed distance cutoff (okf/lessons.md's flag against
    # exactly that miscalibration; matches test_cpp_validation.py's convention).
    assert ks.pvalue > Z_TEST_MIN_PVALUE, (
        f"KS test rejects equivalence for kappa={kappa}: "
        f"distance = {ks.statistic:.4f}, p-value = {ks.pvalue:.5f} <= {Z_TEST_MIN_PVALUE}"
    )
