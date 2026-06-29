"""Cross-language validation for windowed fear: C++ engine vs Python reference (tracker §5.4).

Prong B (statistical parity) for window_len > 1.
"""

from __future__ import annotations

import math
import os
import subprocess
import pytest
import numpy as np
from scipy import stats
from pathlib import Path

from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CPP_BIN = REPO_ROOT / "cpp" / "build" / "twocascade_run"

N_TRIALS = 500
THETA = 0.5
Z_TEST_MIN_PVALUE = 0.005

requires_cpp_binary = pytest.mark.skipif(
    not CPP_BIN.exists(),
    reason=f"C++ engine not built at {CPP_BIN}",
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
        timeout=600,
        env=_subprocess_env(),
    )
    assert result.returncode == 0, f"C++ failed: {result.stderr}"
    return result.stdout

@requires_cpp_binary
def test_window_cpp_vs_python_prong_b():
    """Verify statistical agreement between Python and C++ for window_len=4."""
    n = 500
    p = 0.02
    r = 2
    mu = 0.4
    kappa = 50.0
    seed_size = 5
    window_len = 4
    weights = [0.50, 0.25, 0.15, 0.10]
    
    # Python runs
    py_seed = 54321
    rng = np.random.default_rng(py_seed)
    py_fracs = np.empty(N_TRIALS)
    
    for t in range(N_TRIALS):
        adjacency = sample_gnp_adjacency(n=n, p=p, rng=rng)
        fears = sample_individual_fears(n=n, mean_fear=mu, concentration=kappa, rng=rng)
        nodes = make_nodes(individual_fears=fears)
        seeds = choose_seed(n=n, seed_size=seed_size, adjacency=adjacency, rng=rng, target_high_degree=False)
        res = run_cascade(
            adjacency=adjacency, nodes=nodes, r=r, seed_indices=seeds,
            rng=rng, record_history=False, window_len=window_len, weights=weights
        )
        py_fracs[t] = res.final_failed_fraction
        
    # C++ runs
    cpp_seed = 54321
    stdout = _run_cpp([
        "--n", str(n), "--p", str(p), "--r", str(r),
        "--mu", str(mu), "--kappa", str(kappa),
        "--seed-size", str(seed_size),
        "--trials", str(N_TRIALS),
        "--base-seed", str(cpp_seed),
        "--window-len", str(window_len),
        "--weights", ",".join(map(str, weights)),
    ])
    
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    assert len(lines) == N_TRIALS
    cpp_fracs = np.array([float(ln.split()[0]) for ln in lines])
    
    # Compare P(systemic)
    x1 = int(np.sum(py_fracs >= THETA))
    x2 = int(np.sum(cpp_fracs >= THETA))
    n1 = n2 = N_TRIALS
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)
    
    p_value = 1.0
    if pooled > 0.0 and pooled < 1.0:
        se = math.sqrt(pooled * (1.0 - pooled) * (1.0 / n1 + 1.0 / n2))
        z = (p1 - p2) / se
        p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z)))
        assert p_value > Z_TEST_MIN_PVALUE, f"P(systemic) differs: Py={p1:.3f}, C++={p2:.3f}, p={p_value:.4f}"
        
    # Compare KS test
    ks = stats.ks_2samp(py_fracs, cpp_fracs)
    assert ks.pvalue > Z_TEST_MIN_PVALUE, f"KS test rejects: dist={ks.statistic:.4f}, p={ks.pvalue:.4f}"
    print(f"Validation successful! Z-test p-val: {p_value:.4f}, KS p-val: {ks.pvalue:.4f}")
