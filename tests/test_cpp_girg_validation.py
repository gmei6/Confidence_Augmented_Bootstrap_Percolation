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

import json
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


def _dump_geometry(tmp_path: Path, n: int, base_seed: int,
                   w_min: float = W_MIN, subdir: str = "girg_geometry") -> Path:
    out_dir = tmp_path / subdir
    proc = subprocess.run(
        [
            sys.executable, str(DUMP_GEOMETRY_SCRIPT),
            "--n", str(n), "--tau", str(TAU), "--w-min", str(w_min),
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


def _edge_lines(text: str) -> list[tuple[int, int]]:
    """Every emitted (i, j) line, WITH duplicates preserved.

    The engine prints one line per adjacency entry with j > i, so a cell-pair
    class that gets visited (and sampled) twice emits the same pair twice.
    Collapsing to a set -- which _edge_set_from_lines below does, and which
    every check in this file used to do unconditionally -- destroys exactly
    that evidence: under a constant-c source, a doubled visit reaches the same
    accept/reject verdict as the first, so the edge SET is bit-identical to
    baseline and the duplicate line is the only surviving trace of the bug.
    Measured on the n=200 fixture at c=0.9 with the cell_lex_less guard
    deleted: 141 emitted lines against 136 unique edges (G5.2, MINOR-8).
    """
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        i, j = map(int, line.split())
        lines.append((i, j))
    return lines


def _edge_set_from_lines(text: str) -> set[tuple[int, int]]:
    return set(_edge_lines(text))


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
    building this test, not a partition bug.

    SCOPE CORRECTED BY MEASUREMENT (G5.2, reviewer round 2 MINOR-8). G5 also
    claimed that a doubled or dropped cell pair "instead produces a large,
    systematic difference (thousands of edges at low c), so a small bound here
    still catches that failure mode". That was never measured and is false.
    Mutating sample_girg_adjacency_bkl in an isolated copy and re-running THIS
    fixture (symmetric difference at c = 0.9 / 0.95 / 0.99, bound = 3):

        baseline                             1 / 0 / 0
        drop the level-2 non-touching class  1 / 0 / 0   <- invisible
        drop the level-3 non-touching class  4 / 3 / 3   <- passes at 2 of 3
        delete the cell_lex_less guard       1 / 0 / 0   <- invisible
          (i.e. every unordered cell pair visited and sampled twice)

    n=200 has L=3, so level 3 is its deepest non-touching level. Both blind
    spots are structural, not fixture luck: doubling is IDEMPOTENT at the edge-
    set level under a constant source (the second visit re-runs the same
    accept/reject with the same u), and the level-2 class holds only the
    longest-range pairs, whose exact_p is far below any c tested here.

    The bound is kept as a cheap tripwire on the ratio-branch boundary effect
    -- which is what it actually measures -- and is no longer claimed to catch
    partition bugs. Those are caught by, in order of directness:
    cpp/tests/test_girg.cpp's test_bkl_complete_graph_coverage (the p_bar>=1
    regime forces exact enumeration; it fails on all three mutations, at its
    adj[i].size() == n-1 assertion); the production-n moment test at the bottom
    of this file (statistical, no constant source, so neither blind spot
    applies -- measured under these same mutations: doubling gives z = +91.1 on
    the edge count, dropping level 3 gives z = -37.5 in the [0.236,0.354)
    distance bin, both p = 0 against its Bonferroni alpha of 6.7e-5); and the
    duplicate-emission assertion added below, which turns the previously
    invisible doubling mutation into a hard failure here (141 emitted lines vs
    136 unique edges at c=0.9 under that mutation)."""
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
    emitted = _edge_lines(stdout)
    edges_cpp = set(emitted)
    # No pair emitted twice: a doubled cell-pair class is invisible in the
    # symmetric difference below (idempotent under a constant source) but not
    # here. This is the discrimination the bound of 3 does not provide.
    assert len(emitted) == len(edges_cpp), (
        f"c={c}: the bkl sampler emitted {len(emitted)} adjacency lines for "
        f"{len(edges_cpp)} distinct edges -- a cell pair is being visited (and "
        f"sampled) more than once, i.e. a partition bug"
    )

    max_symmetric_diff = 3  # tripwire on the ratio-branch boundary, see docstring
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

# DELIBERATELY DIFFERENT VALUES (reviewer round 3, MINOR-8). These two seeds
# used to both be 24601, which reads as an attempt to line the two languages'
# RNG streams up -- exactly the thing §5.4 disclaims (numpy's Generator and
# C++'s mt19937_64 do not produce the same stream from the same integer, and
# nothing in this file depends on their doing so). Prong B is a two-sample
# statistical comparison, so the seeds are independent labels for two
# independent Monte Carlo runs; making them differ removes the false
# implication and, incidentally, makes the comparison slightly stronger by
# ruling out any shared-seed coincidence.
PRONG_B_GIRG_PY_SEED = 24601
PRONG_B_GIRG_CPP_SEED = 31337

# Fear-memory window cells (reviewer round 3, MAJOR-2). Prong B ran only at the
# DEFAULT window (window_len=1, i.e. no memory) while every production GIRG
# config -- configs/poster_girg_mu0.json / _mu40 / _mu70 -- runs window_len=5
# with weights [0.2]*5. The windowed path in reference.run_cascade is a
# different code path on BOTH sides (a deque of per-round failure counts, a
# weighted sum over the last window_len rounds, and a window_len-round
# all-quiet stopping rule), so a divergence there would have been invisible to
# the entire cross-language suite while affecting every poster GIRG number.
#
# The (5, [0.2]*5) cell is calibrated the same way the original cell was: an
# 80-trial Python pilot at pilot seed 314159 (NOT the test's 24601, so the
# choice is not tuned to the final comparison) gave P(systemic) = 0.325 at
# kappa=10 and 0.350 at kappa=50 -- both interior, so no other parameter needed
# to move. kappa=50 is the one carried into the suite because it is also the
# `concentration` the production configs use.
WINDOW5_WEIGHTS = (0.2, 0.2, 0.2, 0.2, 0.2)
PRONG_B_GIRG_CELLS = [
    pytest.param(10.0, 1, None, id="kappa10-window1"),
    pytest.param(50.0, 1, None, id="kappa50-window1"),
    pytest.param(50.0, 5, WINDOW5_WEIGHTS, id="kappa50-window5"),
]


def _python_girg_fractions(kappa: float, window_len: int, weights) -> np.ndarray:
    P = {**PRONG_B_GIRG_PARAMS, "kappa": kappa}
    rng = np.random.default_rng(PRONG_B_GIRG_PY_SEED)
    fractions = np.empty(N_TRIALS_GIRG)
    for t in range(N_TRIALS_GIRG):
        points = sample_torus_points(P["n"], rng)
        girg_weights = sample_powerlaw_weights(P["n"], TAU, W_MIN, rng)
        adjacency = sample_girg_adjacency(points, girg_weights, ALPHA_G, rng)
        # gamma=0.0: degree-dependent fear reduces exactly to the global model
        # (this task's scope; see implementation_plan.md).
        fears, _stats = sample_degree_dependent_fears(girg_weights, P["mu"], 0.0, P["kappa"], rng)
        nodes = make_nodes(individual_fears=fears)
        seeds = choose_seed(
            n=P["n"], seed_size=P["seed_size"], adjacency=adjacency, rng=rng,
            target_high_degree=False,
        )
        result = run_cascade(
            adjacency=adjacency, nodes=nodes, r=P["r"], seed_indices=seeds,
            rng=rng, record_history=False,
            window_len=window_len,
            weights=None if weights is None else list(weights),
        )
        fractions[t] = result.final_failed_fraction
    return fractions


def _cpp_girg_fractions(kappa: float, window_len: int, weights) -> np.ndarray:
    P = {**PRONG_B_GIRG_PARAMS, "kappa": kappa}
    args = [
        "--graph-type", "girg", "--tau", str(TAU), "--w-min", str(W_MIN), "--alpha-g", str(ALPHA_G),
        "--n", str(P["n"]), "--r", str(P["r"]),
        "--mu", str(P["mu"]), "--kappa", str(kappa),
        "--seed-size", str(P["seed_size"]),
        "--trials", str(N_TRIALS_GIRG),
        "--base-seed", str(PRONG_B_GIRG_CPP_SEED),
        "--window-len", str(window_len),
    ]
    if weights is not None:
        args += ["--weights", ",".join(repr(float(w)) for w in weights)]
    stdout = _run_cpp(args)
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    assert len(lines) == N_TRIALS_GIRG, f"expected {N_TRIALS_GIRG} lines, got {len(lines)}"
    return np.array([float(ln.split()[0]) for ln in lines])


_girg_fractions_cache = {}


def _get_girg_fractions(kappa: float, window_len: int, weights) -> tuple[np.ndarray, np.ndarray]:
    key = (kappa, window_len, weights)
    if key not in _girg_fractions_cache:
        if not CPP_BIN.exists():
            pytest.skip(f"C++ engine not built at {CPP_BIN}")
        _girg_fractions_cache[key] = (
            _python_girg_fractions(kappa, window_len, weights),
            _cpp_girg_fractions(kappa, window_len, weights),
        )
    return _girg_fractions_cache[key]


@requires_cpp_binary
@pytest.mark.parametrize("kappa,window_len,weights", PRONG_B_GIRG_CELLS)
def test_prong_b_girg_systemic_probability_z_test(kappa, window_len, weights):
    py_fracs, cpp_fracs = _get_girg_fractions(kappa, window_len, weights)
    x1 = int(np.sum(py_fracs >= THETA))
    x2 = int(np.sum(cpp_fracs >= THETA))
    n1 = n2 = N_TRIALS_GIRG
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)

    # Non-vacuity, checked BEFORE the degenerate short-circuit below: a cell
    # whose P(systemic) sat at 0 or 1 on both sides would pass this test while
    # comparing nothing at all. The cells are pilot-calibrated to be interior
    # (see PRONG_B_GIRG_CELLS); this asserts the calibration still holds rather
    # than trusting the comment that records it.
    assert 0.02 < p1 < 0.98, (
        f"degenerate Prong B cell (kappa={kappa}, window_len={window_len}): the "
        f"Python side's P(systemic) = {p1:.3f} is at the boundary, so this "
        f"comparison has almost no power -- recalibrate the cell"
    )

    if pooled == 0.0 or pooled == 1.0:
        assert p1 == p2
        return

    se = math.sqrt(pooled * (1.0 - pooled) * (1.0 / n1 + 1.0 / n2))
    z = (p1 - p2) / se
    p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z)))
    assert p_value > Z_TEST_MIN_PVALUE, (
        f"P(systemic) differs beyond Monte Carlo error for kappa={kappa}, "
        f"window_len={window_len}, weights={weights}: "
        f"Python {p1:.3f} vs C++ {p2:.3f} (z = {z:.3f}, p = {p_value:.5f})"
    )


@requires_cpp_binary
@pytest.mark.parametrize("kappa,window_len,weights", PRONG_B_GIRG_CELLS)
def test_prong_b_girg_failed_fraction_ks_distance(kappa, window_len, weights):
    py_fracs, cpp_fracs = _get_girg_fractions(kappa, window_len, weights)
    ks = stats.ks_2samp(py_fracs, cpp_fracs)
    # p-value form, not a fixed distance cutoff (okf/lessons.md's flag against
    # exactly that miscalibration; matches test_cpp_validation.py's convention).
    assert ks.pvalue > Z_TEST_MIN_PVALUE, (
        f"KS test rejects equivalence for kappa={kappa}, window_len={window_len}, "
        f"weights={weights}: "
        f"distance = {ks.statistic:.4f}, p-value = {ks.pvalue:.5f} <= {Z_TEST_MIN_PVALUE}"
    )


# --------------------------------------------------------------------------- #
# 6. Production-n cross-language parity (n = 10000, and n = 40000)
# --------------------------------------------------------------------------- #

# WHY THIS EXISTS (reviewer round 2, MAJOR-1). Every check above tops out at
# n = 2000 (and the sampler-level ones at n = 500), but the BKL sampler's level
# schedule is n-DEPENDENT: girg_bkl_level_count gives L = 5 at n = 2000, L = 6
# at n = 10000, L = 7 at n = 40000. The validated regime therefore never
# exercised the recursion depth production actually runs at, and a defect that
# only appears at a deeper level -- a level-6 cell-pair class double-visited or
# dropped, a candidate set that degenerates at fine grids -- would have been
# invisible to the entire suite. This test closes that gap at the production
# tuple used by configs/poster_girg_*.json (n = 10000, tau = 2.5,
# w_min = 0.186377, alpha_g = 1.2).
#
# EXTENDED IN G5.3 (reviewer round 3, MAJOR-1): n = 10000 is only L = 6, so the
# same argument still applied one level up. There are now TWO tests below --
# three replicates at n = 10000 (L = 6) and one at n = 40000 (L = 7, the largest
# n this project has swept), sharing one size-generic driver. L = 8 (any
# n in (65536, 262144], e.g. n = 80000) remains UNVALIDATED; the per-level
# coverage table lives in cpp/include/twocascade/girg.hpp, next to the schedule
# it describes.
#
# HOW, given that the obvious approaches do not scale. Comparing sampled graphs
# across languages needs a reference for "how many edges SHOULD there be", and
# at n = 10000 the small-n approach -- materialize the n x n distance matrix,
# take many replicate graphs, compare sample means -- is doubly wrong: 1e8
# doubles is 800 MB of dense n x n structure (the constitution's §I rule and
# reviewer MINOR-9), and heavy-tailed weights (tau = 2.5) make replicate-to-
# replicate edge-count scatter so large that a handful of replicates has almost
# no power.
#
# So the reference is not another sample, it is the EXACT first two moments of
# the sampled statistic under the model, conditional on the shared points and
# weights. Each pair is an independent Bernoulli(p_ij), so for any pair-indexed
# statistic S = sum_{i<j} c_ij X_ij:
#     E[S] = sum c_ij p_ij,     Var[S] = sum c_ij^2 p_ij (1 - p_ij),
# both computable in ONE blockwise O(n^2)-time, O(block*n)-memory pass in numpy
# (the same block trick twocascade.girg.sample_girg_adjacency itself uses), with
# the p_ij coming from the PYTHON side of the language boundary. Then z =
# (S_observed - E[S]) / sqrt(Var[S]) is an absolute, per-replicate, cross-
# language check with no fitted constant anywhere: 3 replicates suffice because
# the comparison is against exact moments rather than against another noisy
# sample. Three statistics are checked, each covering a different failure mode:
#   - total edge count             (gross over/under-sampling)
#   - 6 torus-distance bins        (a truncating spatial index: the far bins go
#                                   to zero while the near bins absorb the mass)
#   - degree mass on the heaviest  (a too-small BKL acceptance bound p_bar,
#     5% of vertices                which silently truncates exactly the
#                                   highest-p pairs, i.e. the heavy tail)
# Realized statistics are computed per-EDGE (m ~ 2.6e4 at this tuple), never
# per-pair, so nothing dense at n x n is built on the observed side either.
#
# Acceptance is by p-value with a Bonferroni correction over every z the test
# produces, matching Z_TEST_MIN_PVALUE and okf/lessons.md's standing objection
# to bare fixed-distance cutoffs.

PRODUCTION_N = 10000
PRODUCTION_W_MIN = 0.186377  # configs/poster_girg_*.json, calibrated in C2
PRODUCTION_BASE_SEEDS = [4100, 4101, 4102]
# Largest n this project has actually swept, and the only size in either suite
# that reaches BKL level 7 (reviewer round 3, MAJOR-1). One replicate; see
# test_largest_swept_n_moment_parity below for the cost accounting.
LARGEST_SWEPT_N = 40000
LARGEST_SWEPT_BASE_SEEDS = [4103]
MOMENT_BLOCK = 256           # 256 x 10000 doubles = 20 MB per temporary
N_DIST_BINS = 6
HEAVY_WEIGHT_QUANTILE = 0.95
MIN_EXPECTED_FOR_NORMAL = 30.0  # skip bins too sparse for a normal approximation


def _girg_exact_moments(points, weights, alpha_g, heavy_mask, dist_edges,
                        block=MOMENT_BLOCK):
    """Exact E and Var of three pair-indexed statistics under the GIRG model,
    conditional on (points, weights). Blockwise: peak memory is O(block * n),
    never O(n^2) -- constitution §I, reviewer MINOR-9.

    The p_ij formula here is written out from the model definition rather than
    imported, so this is an independent Python-side statement of the law that
    the C++ sampler is being measured against."""
    n = len(points)
    x, y = points[:, 0], points[:, 1]
    n_bins = len(dist_edges) - 1
    e_total = v_total = 0.0
    e_bin = np.zeros(n_bins)
    v_bin = np.zeros(n_bins)
    e_heavy = v_heavy = 0.0
    hw = heavy_mask.astype(float)

    for start in range(0, n, block):
        end = min(start + block, n)
        rows = np.arange(start, end)
        cols = np.arange(start, n)  # only j >= start can satisfy j > i here
        dx = np.abs(x[rows, None] - x[None, cols]); dx = np.minimum(dx, 1.0 - dx)
        dy = np.abs(y[rows, None] - y[None, cols]); dy = np.minimum(dy, 1.0 - dy)
        d2 = dx * dx + dy * dy
        zero = (d2 == 0.0)
        d2_safe = np.where(zero, 1.0, d2)
        p = np.minimum(1.0, (weights[rows, None] * weights[None, cols]
                             / (n * d2_safe)) ** alpha_g)
        # Coincident points are skipped (p = 0), matching the oracle's `continue`.
        p = np.where((cols[None, :] > rows[:, None]) & ~zero, p, 0.0)
        q = p * (1.0 - p)

        e_total += float(p.sum())
        v_total += float(q.sum())

        idx = np.clip(np.digitize(np.sqrt(d2), dist_edges) - 1, 0, n_bins - 1).ravel()
        e_bin += np.bincount(idx, weights=p.ravel(), minlength=n_bins)
        v_bin += np.bincount(idx, weights=q.ravel(), minlength=n_bins)

        # c_ij = |{i,j} n heavy| in {0,1,2}: sum of heavy vertices' degrees.
        c = hw[rows, None] + hw[None, cols]
        e_heavy += float((c * p).sum())
        v_heavy += float((c * c * q).sum())

    return {
        "total": (e_total, v_total),
        "bins": (e_bin, v_bin),
        "heavy": (e_heavy, v_heavy),
    }


def _girg_edge_statistics(edges, points, heavy_mask, dist_edges, n):
    """Realized values of the same three statistics, computed per-EDGE (O(m))."""
    if not edges:
        return 0, np.zeros(len(dist_edges) - 1), 0
    ei = np.fromiter((i for i, _ in edges), dtype=int, count=len(edges))
    ej = np.fromiter((j for _, j in edges), dtype=int, count=len(edges))
    dx = np.abs(points[ei, 0] - points[ej, 0]); dx = np.minimum(dx, 1.0 - dx)
    dy = np.abs(points[ei, 1] - points[ej, 1]); dy = np.minimum(dy, 1.0 - dy)
    d = np.sqrt(dx * dx + dy * dy)
    bin_counts = np.histogram(d, bins=dist_edges)[0].astype(float)
    deg = np.bincount(np.concatenate([ei, ej]), minlength=n)
    return len(edges), bin_counts, int(deg[heavy_mask].sum())


def _moment_parity_records(tmp_path, n, base_seeds, subdir_prefix, rep_offset=0):
    """Run the exact-moment parity comparison at size n and return every z it
    produces as (label, z, detail) triples.

    Split out of the test body (G5.3) so the SAME machinery covers more than one
    n without duplicating it -- the check is size-generic, only its cost is not.
    Seeds follow the original scheme, offset by rep_offset so a second call
    cannot collide with the first: geometry from base_seeds, C++ from
    77000 + 10*rep + variant, the Python oracle from 88000 + rep."""
    dist_edges = np.linspace(0.0, math.sqrt(0.5), N_DIST_BINS + 1)
    records = []

    for local_rep, base_seed in enumerate(base_seeds):
        rep = local_rep + rep_offset
        out_dir = _dump_geometry(tmp_path, n, base_seed=base_seed,
                                 w_min=PRODUCTION_W_MIN, subdir=f"{subdir_prefix}{local_rep}")
        points, weights = _load_points_weights(out_dir)
        assert points.shape == (n, 2)

        heavy_mask = weights >= np.quantile(weights, HEAVY_WEIGHT_QUANTILE)
        assert heavy_mask.sum() > 0
        moments = _girg_exact_moments(points, weights, ALPHA_G, heavy_mask, dist_edges)

        e_total, v_total = moments["total"]
        e_bin, v_bin = moments["bins"]
        e_heavy, v_heavy = moments["heavy"]
        assert v_total > 0.0 and e_total > 0.0

        observed = {}
        for variant in ("direct", "bkl"):
            stdout = _run_cpp([
                "--girg-verify", "sample",
                "--points-file", str(out_dir / "points.txt"),
                "--weights-file", str(out_dir / "weights.txt"),
                "--alpha-g", str(ALPHA_G),
                "--girg-variant", variant,
                "--rng-source", "real",
                "--base-seed", str(77000 + 10 * rep + (0 if variant == "direct" else 1)),
            ])
            observed[f"cpp-{variant}"] = sorted(_edge_set_from_lines(stdout))

        adj_py = sample_girg_adjacency(points, weights, ALPHA_G,
                                       np.random.default_rng(88000 + rep))
        observed["python-oracle"] = sorted(
            (i, j) for i, nbrs in enumerate(adj_py) for j in nbrs if i < j)

        for label, edges in observed.items():
            m, bin_counts, heavy_mass = _girg_edge_statistics(
                edges, points, heavy_mask, dist_edges, n)
            records.append((f"rep{rep}/{label}/edge-count", (m - e_total) / math.sqrt(v_total),
                            f"m={m} vs E={e_total:.1f}+-{math.sqrt(v_total):.1f}"))
            records.append((f"rep{rep}/{label}/heavy-degree-mass",
                            (heavy_mass - e_heavy) / math.sqrt(v_heavy),
                            f"mass={heavy_mass} vs E={e_heavy:.1f}+-{math.sqrt(v_heavy):.1f}"))
            for b in range(N_DIST_BINS):
                if e_bin[b] < MIN_EXPECTED_FOR_NORMAL or v_bin[b] <= 0.0:
                    continue  # too sparse for a normal approximation to mean anything
                records.append((
                    f"rep{rep}/{label}/dist-bin{b}"
                    f"[{dist_edges[b]:.3f},{dist_edges[b+1]:.3f})",
                    (bin_counts[b] - e_bin[b]) / math.sqrt(v_bin[b]),
                    f"count={bin_counts[b]:.0f} vs E={e_bin[b]:.1f}+-{math.sqrt(v_bin[b]):.1f}"))

            # A truncating spatial index is the one failure this suite must never
            # miss, and at production n the outermost bin can be sparse enough to
            # be skipped above -- so assert its non-emptiness as a hard fact too.
            assert bin_counts[-1] > 0, (
                f"rep{rep}/{label}: no edges at all in the outermost distance bin "
                f"[{dist_edges[-2]:.3f},{dist_edges[-1]:.3f}) while the model expects "
                f"{e_bin[-1]:.1f} -- signature of a truncating spatial index"
            )

        # Cross-variant: direct vs bkl on the SAME points/weights. Independent
        # RNG streams, so the difference of two Poisson-binomial counts has
        # variance 2 * v_total under the null that both sample the same measure.
        m_direct = len(observed["cpp-direct"])
        m_bkl = len(observed["cpp-bkl"])
        records.append((f"rep{rep}/direct-vs-bkl/edge-count",
                        (m_bkl - m_direct) / math.sqrt(2.0 * v_total),
                        f"bkl={m_bkl} direct={m_direct}"))

    return records


def _assert_moment_records(records, what):
    """Bonferroni over every z produced, so the family-wise false-positive rate
    is the same Z_TEST_MIN_PVALUE the rest of this suite is calibrated to."""
    assert records, f"{what}: no z-scores produced at all"
    n_tests = len(records)
    per_test_alpha = Z_TEST_MIN_PVALUE / n_tests
    worst = max(records, key=lambda rec: abs(rec[1]))
    worst_p = 2.0 * stats.norm.sf(abs(worst[1]))
    assert worst_p > per_test_alpha, (
        f"{what} failed at {worst[0]}: z = {worst[1]:+.3f}, "
        f"p = {worst_p:.3e} <= {per_test_alpha:.3e} "
        f"(= {Z_TEST_MIN_PVALUE}/{n_tests} Bonferroni over {n_tests} z-scores); {worst[2]}"
    )


@requires_cpp_binary
def test_production_n_cross_language_parity_against_exact_moments(tmp_path):
    """C++ (both variants) and the Python oracle, at the PRODUCTION tuple and
    production n, each measured against exact model moments on shared geometry.

    The Python oracle is included not as the thing under test but as a CONTROL:
    it is the sampler every other check in this file trusts, so if its z-scores
    were also out of range the moment computation would be what is wrong, not
    the C++ engine. Keeping it in the same Bonferroni family makes that
    explicit rather than assumed.

    Direct and BKL are additionally compared to each other on the same
    points/weights (independent RNG streams, so the comparison is statistical):
    that is the cross-VARIANT half of the parity claim, and it is the check
    that would catch a defect confined to the deeper level schedule that only
    n >= 10000 reaches.

    DISCRIMINATION (measured, not assumed). Mutating sample_girg_adjacency_bkl
    in an isolated copy of the tree and re-running THIS test at n = 10000, which
    produces 75 z-scores and therefore a Bonferroni alpha of 6.667e-5:
      - baseline, unmutated: worst |z| = 2.03 (p = 0.043), 0 of 75 z-scores
        past alpha -- i.e. the margin below is real headroom, not a test that
        barely passes                                                [G5.3]
      - visit every unordered cell pair twice: z = +91.1 on the edge count
        (m = 36539 vs E = 25130 +- 125)                              [G5.2]
      - drop the level-3 non-touching class: z = -37.5 in the [0.236,0.354)
        distance bin (238 edges vs E = 1627 +- 37)                   [G5.2]
      - drop the level-2 non-touching class (MUT-A at level 2, the one class
        G5.2 never measured against this test): CAUGHT decisively. Worst
        z = -20.89 in the [0.471,0.589) distance bin (79 edges vs
        E = 524.9 +- 21.3), p = 7.1e-97; 19 of the 75 z-scores exceed alpha,
        including the plain edge count (z = -9.90, m = 23889 vs
        E = 25129.6 +- 125.3) and the heavy-degree mass (z = -11.43). Every
        failing z is a cpp-bkl one: the Python-oracle and cpp-direct records in
        the same family stay inside +-2, which is what makes the diagnosis
        "the BKL sampler lost its longest-range class" rather than "the moment
        computation is wrong"                                        [G5.3]
    That last case is the one the constant-c level-set tests are structurally
    blind to (the level-2 class carries only the longest-range pairs, whose
    exact_p never crosses a high threshold c, so its removal changes no edge at
    c in {0.9, 0.95, 0.99}). Both this test and, deterministically,
    cpp/tests/test_girg.cpp's test_bkl_complete_graph_coverage catch it; the
    signature here is specifically a deficit concentrated in the OUTER distance
    bins, which is what identifies it as a lost long-range class."""
    records = _moment_parity_records(
        tmp_path, PRODUCTION_N, PRODUCTION_BASE_SEEDS, subdir_prefix="prod_")
    _assert_moment_records(records, f"production-n (n={PRODUCTION_N}) parity")


@requires_cpp_binary
@pytest.mark.slow
def test_largest_swept_n_moment_parity_reaches_bkl_level_7(tmp_path):
    """The same exact-moment parity check, one replicate, at n = 40000 -- the
    largest n this project has swept and the ONLY size in either suite that
    reaches BKL level 7 (reviewer round 3, MAJOR-1).

    WHY IT IS SEPARATE rather than a fourth entry in PRODUCTION_BASE_SEEDS:
    cost. Measured on this machine, one n = 40000 replicate is ~83 s wall
    (geometry dump 0.7 s, exact moments 43 s, C++ bkl 0.24 s, C++ direct 15 s,
    Python oracle 24 s) against ~17 s for all three n = 10000 replicates
    together, and its peak RSS is ~2.5 GB (the Python oracle's own blockwise
    temporaries; the moment pass itself peaks at ~1.6 GB with MOMENT_BLOCK=256,
    which measurement confirmed is both faster and 3.7x lighter than 1024). A
    separate test keeps that cost deselectable via `-m "not slow"`, keeps its
    Bonferroni family separate and honest, and keeps a failure at n = 40000
    distinguishable from one at n = 10000 in the report.

    ONE replicate, not three: the comparison is against EXACT model moments, so
    a single replicate already yields ~20 independent z-scores; replicates buy
    breadth over geometry realizations, not power, and the geometry-to-geometry
    variation is already sampled three times at n = 10000.

    DISCRIMINATION AT THIS n (measured, G5.3). With the level-2 non-touching
    class dropped in an isolated mutated build, this test's 25 z-scores give a
    Bonferroni alpha of 2.0e-4 and it FAILS at worst z = -27.14 in the
    [0.471,0.589) distance bin (184 edges vs E = 1055.7 +- 32.1), p = 3.1e-162,
    with 7 of 25 z past alpha -- and every one of them a cpp-bkl record, while
    cpp-direct and python-oracle stay inside +-1.2 on the same geometry. So the
    single replicate is not a token: it discriminates on its own.

    STILL NOT COVERED: level 8, i.e. n in (65536, 262144] -- notably the
    n = 80000 an even larger sweep would use. See the coverage table in
    cpp/include/twocascade/girg.hpp."""
    records = _moment_parity_records(
        tmp_path, LARGEST_SWEPT_N, LARGEST_SWEPT_BASE_SEEDS,
        subdir_prefix="largest_", rep_offset=len(PRODUCTION_BASE_SEEDS))
    _assert_moment_records(records, f"largest-swept-n (n={LARGEST_SWEPT_N}) parity")


# --------------------------------------------------------------------------- #
# 7. C++'s OWN point/weight generators vs Python's sampling law
# --------------------------------------------------------------------------- #

# WHY THIS EXISTS (reviewer round 2, MAJOR-2). Sections 1-6 all feed the C++
# engine points and weights DUMPED BY PYTHON (that is what makes them
# deterministic), so not one of them says anything about C++'s own
# sample_torus_points / sample_powerlaw_weights (cpp/src/girg.cpp:11-30). Those
# are not test scaffolding: the graph_type=="girg" branch of main.cpp's trial
# loop calls them for EVERY production trial. A transposed exponent
# (u**(tau-1) rather than u**(-1/(tau-1))), a w_min added rather than
# multiplied, or points drawn on the wrong support would leave every check
# above green while every production GIRG run sampled the wrong model.
#
# The C++ draws are exported by the `--girg-verify draws` mode added for this
# purpose, which reproduces the production trial loop's rng construction
# exactly (make_seeded_rng(base_seed, 0) -> points -> weights, one generator,
# that order). Three independent claims are asserted:
#   (a) weights follow the SAME LAW as Python's sample_powerlaw_weights --
#       both against the analytic CDF the law implies and, two-sample, against
#       Python's actual draws (that second one is the literal cross-language
#       comparison the reviewer asked for; it needs no analytic derivation to
#       be trusted, and it would catch a discrepancy in a law we had
#       mis-derived identically in both places... which the first check, being
#       derivation-based, would not);
#   (b) points are uniform on [0,1)^2 -- per-axis and, via a grid chi-square,
#       jointly (a sampler that drew y = x would pass both per-axis KS tests);
#   (c) end-to-end, the geometry these two functions produce feeds the BKL
#       sampler to the CALIBRATED mean degree, i.e. the C++ engine reproduces
#       the number the poster's matched-degree arm is built on.
#
# Acceptance is by p-value with a Bonferroni correction over each test's own
# family (never a bare fixed distance -- okf/lessons.md), and each test also
# carries a DISCRIMINATION check showing the same statistic at the same
# threshold rejects a deliberately wrong law. Without that, "KS did not
# reject" is unfalsifiable: a KS test on a statistic that cannot move is
# always green.

GEOM_LAW_N = 100_000          # draws per generator check
GEOM_LAW_CPP_SEED = 909
GEOM_LAW_PY_SEED = 20260804
GRID_SIDE = 32                # 32x32 cells -> ~98 expected points per cell
WRONG_TAU = 2.55              # 2% exponent error, for the discrimination checks
MEAN_DEGREE_REPLICATES = 20   # matches the calibration run's replicate count
MEAN_DEGREE_DIRECT_REPLICATES = 5
CALIBRATION_JSON = REPO_ROOT / "results" / "processed" / "girg_degree_calibration.json"


def _cpp_draws(n: int, tau: float, w_min: float, base_seed: int):
    """Points and weights as generated BY C++ (production rng construction)."""
    stdout = _run_cpp([
        "--girg-verify", "draws",
        "--n", str(n), "--tau", str(tau), "--w-min", str(w_min),
        "--base-seed", str(base_seed),
    ])
    rows = np.fromstring(stdout, sep=" ").reshape(-1, 3)
    assert rows.shape[0] == n, f"expected {n} draw rows, got {rows.shape[0]}"
    return rows[:, :2], rows[:, 2]


@requires_cpp_binary
def test_cpp_weight_generator_matches_pythons_powerlaw_law():
    """C++ sample_powerlaw_weights vs (i) the analytic law and (ii) Python's draws.

    The law: w = w_min * u**(-1/(tau-1)) with u ~ U(0,1) gives
    P(W > w) = P(u < (w/w_min)**-(tau-1)) = (w_min/w)**(tau-1), i.e. a Pareto
    with shape tau-1 and scale w_min. scipy's pareto(b, loc=0, scale) has
    exactly that survival function, so the one-sample KS below is against the
    law itself, with no fitted parameter anywhere.
    """
    _, w_cpp = _cpp_draws(GEOM_LAW_N, TAU, W_MIN, GEOM_LAW_CPP_SEED)
    w_py = sample_powerlaw_weights(GEOM_LAW_N, TAU, W_MIN,
                                   np.random.default_rng(GEOM_LAW_PY_SEED))

    # Support: the law's minimum is exactly w_min (u=1 -> w=w_min). A draw
    # below it means the exponent's SIGN is wrong, which a KS test on the bulk
    # can be surprisingly slow to notice.
    assert w_cpp.min() >= W_MIN, f"C++ weight below w_min: {w_cpp.min()!r} < {W_MIN}"

    ks_law = stats.kstest(w_cpp, "pareto", args=(TAU - 1.0, 0.0, W_MIN))
    ks_cross = stats.ks_2samp(w_cpp, w_py)
    alpha = Z_TEST_MIN_PVALUE / 2  # Bonferroni over the two claims
    assert ks_law.pvalue > alpha, (
        f"C++ weights reject the analytic Pareto(shape={TAU - 1}, scale={W_MIN}) law: "
        f"D = {ks_law.statistic:.5f}, p = {ks_law.pvalue:.3e} <= {alpha:.3e}"
    )
    assert ks_cross.pvalue > alpha, (
        f"C++ and Python weight draws reject a common law: "
        f"D = {ks_cross.statistic:.5f}, p = {ks_cross.pvalue:.3e} <= {alpha:.3e}"
    )

    # DISCRIMINATION: the same test, same threshold, same sample size, against
    # draws from a law only 2% off in the exponent -- must reject, both ways.
    w_wrong = sample_powerlaw_weights(GEOM_LAW_N, WRONG_TAU, W_MIN,
                                      np.random.default_rng(GEOM_LAW_PY_SEED + 1))
    ks_wrong_law = stats.kstest(w_wrong, "pareto", args=(TAU - 1.0, 0.0, W_MIN))
    ks_wrong_cross = stats.ks_2samp(w_wrong, w_cpp)
    assert ks_wrong_law.pvalue < alpha and ks_wrong_cross.pvalue < alpha, (
        f"discrimination failed: tau={WRONG_TAU} draws were NOT rejected as "
        f"tau={TAU} (law p = {ks_wrong_law.pvalue:.3e}, cross p = "
        f"{ks_wrong_cross.pvalue:.3e}), so these KS checks prove nothing"
    )


@requires_cpp_binary
def test_cpp_point_generator_is_uniform_on_the_torus():
    """C++ sample_torus_points vs U([0,1))^2: support, per-axis, and joint."""
    points, _ = _cpp_draws(GEOM_LAW_N, TAU, W_MIN, GEOM_LAW_CPP_SEED + 1)
    x, y = points[:, 0], points[:, 1]

    # Half-open support, as the torus wrap-around assumes.
    assert x.min() >= 0.0 and x.max() < 1.0, f"x outside [0,1): [{x.min()}, {x.max()}]"
    assert y.min() >= 0.0 and y.max() < 1.0, f"y outside [0,1): [{y.min()}, {y.max()}]"

    ks_x = stats.kstest(x, "uniform")
    ks_y = stats.kstest(y, "uniform")
    # Joint uniformity: per-axis KS is blind to dependence (y = x passes both),
    # and the whole point of the geometry is the JOINT position, so bin the
    # unit square and chi-square the cell counts.
    counts, _, _ = np.histogram2d(x, y, bins=[np.linspace(0, 1, GRID_SIDE + 1),
                                              np.linspace(0, 1, GRID_SIDE + 1)])
    chi2 = stats.chisquare(counts.ravel())

    alpha = Z_TEST_MIN_PVALUE / 3  # Bonferroni over the three claims
    assert ks_x.pvalue > alpha and ks_y.pvalue > alpha, (
        f"C++ torus points reject per-axis uniformity: "
        f"x p = {ks_x.pvalue:.3e}, y p = {ks_y.pvalue:.3e} (alpha = {alpha:.3e})"
    )
    assert chi2.pvalue > alpha, (
        f"C++ torus points reject joint uniformity on a {GRID_SIDE}x{GRID_SIDE} grid: "
        f"chi2 = {chi2.statistic:.1f}, p = {chi2.pvalue:.3e} <= {alpha:.3e}"
    )

    # DISCRIMINATION: the grid chi-square must reject a sampler that is
    # per-axis uniform but jointly degenerate (y = x), which is exactly the
    # failure the two KS tests above cannot see.
    diag_counts, _, _ = np.histogram2d(x, x, bins=[np.linspace(0, 1, GRID_SIDE + 1),
                                                   np.linspace(0, 1, GRID_SIDE + 1)])
    assert stats.chisquare(diag_counts.ravel()).pvalue < alpha, (
        "discrimination failed: the grid chi-square did not reject y = x, so it "
        "is not testing joint uniformity at all"
    )


@requires_cpp_binary
def test_cpp_generated_geometry_reproduces_calibrated_mean_degree():
    """End-to-end: C++-generated points+weights, sampled by the C++ engine, hit
    the mean degree Python's calibration achieved at the SAME tuple.

    Provenance: results/processed/girg_degree_calibration.json (C2,
    scripts/calibrate_girg_degree.py, base_seed 20260802, 20 replicates) is
    where w_min = 0.186377 comes from in the first place, and it records the
    achieved <k> and its standard ERROR over those 20 replicates. The
    per-replicate SD is se * sqrt(20) -- that is the tolerance scale used here,
    read from the artifact rather than typed in, so this test tracks the
    calibration instead of drifting from it.

    This is the only check in the file that exercises the production path
    end to end: generators + sampler, no Python-supplied geometry anywhere.
    """
    calib = json.loads(CALIBRATION_JSON.read_text())["girg"]
    n = calib["n"]
    tau, alpha_g, w_min = calib["tau"], calib["alpha_g"], calib["w_min"]
    target = calib["achieved_mean_degree"]
    per_replicate_sd = calib["achieved_se"] * math.sqrt(20)  # 20 replicates, per the metadata
    assert (n, tau, alpha_g) == (PRODUCTION_N, TAU, ALPHA_G)
    assert abs(w_min - PRODUCTION_W_MIN) < 1e-6

    def cpp_mean_degrees(variant: str, replicates: int, seed0: int) -> np.ndarray:
        out = []
        for rep in range(replicates):
            line = _run_cpp([
                "--girg-verify", "bench",
                "--n", str(n), "--tau", str(tau), "--w-min", repr(w_min),
                "--alpha-g", str(alpha_g), "--girg-variant", variant,
                "--base-seed", str(seed0 + rep),
            ]).split()
            assert line[0] == variant and int(line[1]) == n
            out.append(2.0 * int(line[3]) / n)
        return np.array(out)

    arms = {
        "bkl": cpp_mean_degrees("bkl", MEAN_DEGREE_REPLICATES, 7001),
        "direct": cpp_mean_degrees("direct", MEAN_DEGREE_DIRECT_REPLICATES, 7501),
    }
    alpha = Z_TEST_MIN_PVALUE / len(arms)
    for variant, degrees in arms.items():
        z = (degrees.mean() - target) / (per_replicate_sd / math.sqrt(len(degrees)))
        p = 2.0 * stats.norm.sf(abs(z))
        assert p > alpha, (
            f"C++ {variant} mean degree {degrees.mean():.4f} (over {len(degrees)} "
            f"replicates) is inconsistent with the calibrated <k> = {target:.5f} "
            f"+- {per_replicate_sd:.4f} per replicate: z = {z:+.3f}, p = {p:.3e} "
            f"<= {alpha:.3e}. Either the C++ weight/point generators or the "
            f"sampler no longer match what results/processed/"
            f"girg_degree_calibration.json was produced with."
        )

    # DISCRIMINATION: the same z-test would reject a 10% error in <k> (which is
    # far SMALLER than what a broken weight law produces -- w_min alone moves
    # <k> from 1.38 at 0.100 to 645 at 3.0, per the calibration's own bracket).
    z_off = (1.10 * target - target) / (per_replicate_sd / math.sqrt(MEAN_DEGREE_REPLICATES))
    assert 2.0 * stats.norm.sf(abs(z_off)) < alpha, (
        "discrimination failed: this z-test cannot even detect a 10% shift in "
        "mean degree, so passing it means nothing"
    )
