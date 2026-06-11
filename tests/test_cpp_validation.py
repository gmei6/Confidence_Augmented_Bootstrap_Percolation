"""Cross-language validation: C++ engine vs Python reference oracle (tracker §5.4).

Prong A (deterministic logic): at mu=0 the cascade is deterministic given the
graph + seed set + r. Dump a graph/seed/failed-set triple from the Python
oracle (dump_reference_run.py), run the C++ engine on the *same* graph and
seeds, and require the final failed sets to be identical down to node indices.

Prong B (statistical parity): for mu > 0 the two engines use different RNG
streams (numpy Generator vs std::mt19937_64), so bit-identical output is
impossible by design — expected divergence is NOT a failure (D-016). Instead,
run N_TRIALS in each engine at the same parameter cell and require:
  * two-proportion z-test on P(systemic): p-value > 0.005, with a
    zero-variance guard (pooled proportion exactly 0 or 1 -> assert the two
    proportions are equal instead of dividing by zero);
  * two-sample KS distance between the |A*|/n distributions < 0.05
    (the test_decoupling_conjecture.py convention).

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

from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)

# --------------------------------------------------------------------------- #
# Locations & constants
# --------------------------------------------------------------------------- #

REPO_ROOT = Path(__file__).resolve().parent.parent
CPP_BIN = REPO_ROOT / "cpp" / "build" / "twocascade_run"
DUMP_SCRIPT = (
    REPO_ROOT / ".agents" / "skills" / "cross-validation" / "scripts" / "dump_reference_run.py"
)

N_TRIALS = 1000          # per engine, Prong B
THETA = 0.5              # systemic-event threshold (tracker §3.5)
KS_MAX_DISTANCE = 0.05   # test_decoupling_conjecture.py convention
Z_TEST_MIN_PVALUE = 0.005
SUBPROCESS_TIMEOUT = 600  # seconds

requires_cpp_binary = pytest.mark.skipif(
    not CPP_BIN.exists(),
    reason=f"C++ engine not built at {CPP_BIN}; build cpp/ in Release mode first",
)


def _subprocess_env() -> dict:
    """Environment for child processes, ensuring src/ is importable."""
    env = dict(os.environ)
    src = str(REPO_ROOT / "src")
    env["PYTHONPATH"] = src + os.pathsep + env.get("PYTHONPATH", "")
    env["OMP_NUM_THREADS"] = "1"
    return env


def _run_cpp(args: list[str]) -> str:
    """Invoke the C++ engine, returning stdout; fail loudly with stderr on error."""
    result = subprocess.run(
        [str(CPP_BIN)] + args,
        capture_output=True,
        text=True,
        timeout=SUBPROCESS_TIMEOUT,
        env=_subprocess_env(),
    )
    assert result.returncode == 0, (
        f"C++ engine exited with {result.returncode}.\n"
        f"args: {args}\nstderr: {result.stderr}"
    )
    return result.stdout


# --------------------------------------------------------------------------- #
# Prong A — deterministic logic equivalence at mu = 0
# --------------------------------------------------------------------------- #

PRONG_A_CASES = [
    # (n, p, r, seed_size, base_seed) — chosen to cover both phases:
    pytest.param(1000, 0.01, 2, 30, 0, id="supercritical-r2"),
    pytest.param(5000, 0.005, 4, 100, 42, id="subcritical-r4"),
]


@requires_cpp_binary
@pytest.mark.parametrize("n,p,r,seed_size,base_seed", PRONG_A_CASES)
def test_prong_a_failed_sets_identical(n, p, r, seed_size, base_seed, tmp_path):
    """C++ final failed set must equal the Python oracle's, node for node."""
    out_dir = tmp_path / "xval"

    dump = subprocess.run(
        [
            sys.executable, str(DUMP_SCRIPT),
            "--n", str(n), "--p", str(p), "--r", str(r),
            "--seed-size", str(seed_size), "--base-seed", str(base_seed),
            "--out", str(out_dir),
        ],
        capture_output=True,
        text=True,
        timeout=SUBPROCESS_TIMEOUT,
        env=_subprocess_env(),
        cwd=REPO_ROOT,
    )
    assert dump.returncode == 0, f"dump_reference_run.py failed:\n{dump.stderr}"

    stdout = _run_cpp(
        [
            "--graph-file", str(out_dir / "graph.txt"),
            "--seed-file", str(out_dir / "seed.txt"),
            "--dump-failed-set",
            "--mu", "0",
            "--r", str(r),
        ]
    )

    # Parse both sides as sorted integer lists — whitespace/newline differences
    # must not cause spurious failures.
    cpp_failed = sorted(int(tok) for tok in stdout.split())
    py_failed = sorted(
        int(tok) for tok in (out_dir / "failed.txt").read_text().split()
    )

    assert cpp_failed == py_failed, (
        f"Failed sets differ: C++ has {len(cpp_failed)} nodes, "
        f"Python has {len(py_failed)} nodes.\n"
        f"C++ only: {sorted(set(cpp_failed) - set(py_failed))[:20]}\n"
        f"Python only: {sorted(set(py_failed) - set(cpp_failed))[:20]}"
    )


# --------------------------------------------------------------------------- #
# Prong B — statistical parity at mu > 0
# --------------------------------------------------------------------------- #

# One discriminating cell near the combined threshold so P(systemic) is
# (ideally) interior — a cell deep in either phase would pass trivially.
PRONG_B_PARAMS = dict(n=1000, p=0.01, r=2, mu=0.5, kappa=50.0, seed_size=2)
PRONG_B_PY_SEED = 20260611
PRONG_B_CPP_SEED = 123


def _python_fractions() -> np.ndarray:
    """N_TRIALS final failed fractions from the Python reference engine."""
    P = PRONG_B_PARAMS
    rng = np.random.default_rng(PRONG_B_PY_SEED)
    fractions = np.empty(N_TRIALS)
    for t in range(N_TRIALS):
        adjacency = sample_gnp_adjacency(n=P["n"], p=P["p"], rng=rng)
        fears = sample_individual_fears(
            n=P["n"], mean_fear=P["mu"], concentration=P["kappa"], rng=rng
        )
        nodes = make_nodes(individual_fears=fears)
        seeds = choose_seed(
            n=P["n"], seed_size=P["seed_size"], adjacency=adjacency,
            rng=rng, target_high_degree=False,
        )
        result = run_cascade(
            adjacency=adjacency, nodes=nodes, r=P["r"], seed_indices=seeds,
            rng=rng, record_history=False,
        )
        fractions[t] = result.final_failed_fraction
    return fractions


def _cpp_fractions() -> np.ndarray:
    """N_TRIALS final failed fractions from the C++ engine."""
    P = PRONG_B_PARAMS
    stdout = _run_cpp(
        [
            "--n", str(P["n"]), "--p", str(P["p"]), "--r", str(P["r"]),
            "--mu", str(P["mu"]), "--kappa", str(P["kappa"]),
            "--seed-size", str(P["seed_size"]),
            "--trials", str(N_TRIALS),
            "--base-seed", str(PRONG_B_CPP_SEED),
        ]
    )
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    assert len(lines) == N_TRIALS, (
        f"Expected {N_TRIALS} output lines from C++ engine, got {len(lines)}"
    )
    return np.array([float(ln.split()[0]) for ln in lines])


@pytest.fixture(scope="module")
def prong_b_fractions():
    if not CPP_BIN.exists():
        pytest.skip(f"C++ engine not built at {CPP_BIN}")
    return _python_fractions(), _cpp_fractions()


@requires_cpp_binary
def test_prong_b_systemic_probability_z_test(prong_b_fractions):
    """Two-proportion z-test on P(systemic): engines must agree within MC error."""
    py_fracs, cpp_fracs = prong_b_fractions
    x1 = int(np.sum(py_fracs >= THETA))
    x2 = int(np.sum(cpp_fracs >= THETA))
    n1 = n2 = N_TRIALS
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)

    if pooled == 0.0 or pooled == 1.0:
        # Zero-variance guard: both engines saw all-subcritical or
        # all-systemic outcomes. Equality is the only meaningful check, but
        # note the cell is then non-discriminating (see PRONG_B_PARAMS).
        assert p1 == p2
        return

    se = math.sqrt(pooled * (1.0 - pooled) * (1.0 / n1 + 1.0 / n2))
    z = (p1 - p2) / se
    p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z)))
    assert p_value > Z_TEST_MIN_PVALUE, (
        f"P(systemic) differs beyond Monte Carlo error: "
        f"Python {p1:.3f} vs C++ {p2:.3f} (z = {z:.3f}, p = {p_value:.5f})"
    )


@requires_cpp_binary
def test_prong_b_failed_fraction_ks_distance(prong_b_fractions):
    """KS distance between the |A*|/n distributions must be < 0.05."""
    py_fracs, cpp_fracs = prong_b_fractions
    ks = stats.ks_2samp(py_fracs, cpp_fracs)
    assert ks.statistic < KS_MAX_DISTANCE, (
        f"KS distance {ks.statistic:.4f} >= {KS_MAX_DISTANCE} "
        f"(p = {ks.pvalue:.5f}); distributions diverge beyond parity tolerance"
    )
