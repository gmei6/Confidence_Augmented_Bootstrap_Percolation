"""Gate test for the C2 GIRG degree calibration script. Written before implementation.

Not the implementer's to edit. If an assertion looks wrong, stop and say which
and why. Requires scripts/calibrate_girg_degree.py to be importable and expose:

  measure_girg_degree(n, tau, w_min, alpha_g, replicates, base_seed)
      -> (realised_mean, realised_se)
  solve_w_min(target, n, tau, alpha_g, replicates, base_seed,
              tol, w_lo, w_hi, max_iter)
      -> dict with at least keys: w_min, achieved_mean_degree, achieved_se,
         iterations, converged
"""
import importlib.util
import os
import sys

import numpy as np
import pytest

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_spec = importlib.util.spec_from_file_location(
    "calibrate_girg_degree", os.path.join(_REPO, "scripts", "calibrate_girg_degree.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

N_SMALL = 1500
TAU = 2.5
ALPHA_G = 1.2


def test_measurement_deterministic_and_sane():
    m1, se1 = _mod.measure_girg_degree(N_SMALL, TAU, 1.0, ALPHA_G, replicates=6, base_seed=77)
    m2, se2 = _mod.measure_girg_degree(N_SMALL, TAU, 1.0, ALPHA_G, replicates=6, base_seed=77)
    assert m1 == m2 and se1 == se2, "measurement not deterministic given base_seed"
    assert 0.0 < m1 < N_SMALL, "insane mean degree"
    assert se1 > 0.0


def test_mean_degree_monotone_in_w_min():
    lo, _ = _mod.measure_girg_degree(N_SMALL, TAU, 0.5, ALPHA_G, replicates=6, base_seed=77)
    hi, _ = _mod.measure_girg_degree(N_SMALL, TAU, 1.5, ALPHA_G, replicates=6, base_seed=77)
    assert hi > lo, f"mean degree not increasing in w_min ({lo:.3f} vs {hi:.3f})"


def test_solver_converges_to_target():
    target = 4.5
    res = _mod.solve_w_min(target, N_SMALL, TAU, ALPHA_G, replicates=6, base_seed=77,
                           tol=0.15, w_lo=0.1, w_hi=3.0, max_iter=25)
    assert res["converged"], f"solver failed to converge: {res}"
    assert abs(res["achieved_mean_degree"] - target) <= max(0.15, 3.0 * res["achieved_se"]), (
        f"achieved {res['achieved_mean_degree']:.3f} vs target {target} "
        f"(se {res['achieved_se']:.3f})")
    # Re-solving with the same seed must be reproducible.
    res2 = _mod.solve_w_min(target, N_SMALL, TAU, ALPHA_G, replicates=6, base_seed=77,
                            tol=0.15, w_lo=0.1, w_hi=3.0, max_iter=25)
    assert res["w_min"] == res2["w_min"], "solver not deterministic given base_seed"


def test_uses_fast_sampler():
    """The port exists so calibration is feasible; the script must use the fast
    sampler, not the O(n^2) loop."""
    import inspect
    src = inspect.getsource(_mod)
    assert "sample_girg_adjacency_slow" not in src, "script imports the slow sampler"
    assert "sample_girg_adjacency" in src
