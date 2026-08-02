"""Gate test for C3a: GIRG trials must use degree-dependent (water-filling) fears.

Written before implementation; not the implementer's to edit. If an assertion
looks wrong, stop and say which and why.
"""
import inspect

import numpy as np
import pytest

from twocascade import runner


MU = 0.4
KAPPA = 2.0
N = 600

GIRG_CFG = {"type": "girg", "tau": 2.5, "w_min": 0.186377, "alpha_g": 1.2}
GNP_P = 0.005
WINDOW_WEIGHTS = [0.2, 0.2, 0.2, 0.2, 0.2]


def _trial_args(graph_cfg, fear_cfg, seed=1234, mu=MU):
    # (n, p, r, mu, kappa, a, target_high_degree, window_len, weights,
    #  graph_cfg, fear_cfg, seed_layout, child_seed)
    return (N, GNP_P, 2, mu, KAPPA, 3, False, 5, WINDOW_WEIGHTS,
            graph_cfg, fear_cfg, "uniform", seed)


class _Spy:
    def __init__(self, real):
        self.real = real
        self.calls = []

    def __call__(self, degrees, mu_bar, gamma, kappa, rng):
        fears, stats = self.real(degrees, mu_bar, gamma, kappa, rng)
        self.calls.append({
            "degrees": np.asarray(degrees, dtype=float).copy(),
            "mu_bar": mu_bar, "gamma": gamma, "kappa": kappa,
            "fears": list(fears), "stats": stats,
        })
        return fears, stats


def test_runner_does_not_use_stale_girg_fear_sampler():
    src = inspect.getsource(runner)
    assert "from twocascade.girg import" in src
    girg_import = src.split("from twocascade.girg import", 1)[1].split(")", 1)[0]
    assert "sample_degree_dependent_fears" not in girg_import, (
        "runner imports the stale pre-Task-Q fear sampler from girg.py")


def test_girg_uses_water_filling_fears_with_weights(monkeypatch):
    spy = _Spy(runner.sample_degree_dependent_fears)
    monkeypatch.setattr(runner, "sample_degree_dependent_fears", spy)
    frac, rounds = runner.run_single_trial(
        _trial_args(GIRG_CFG, {"type": "global", "gamma": 1.0}))
    assert len(spy.calls) == 1, "girg trial must call the water-filling sampler exactly once"
    call = spy.calls[0]
    # Fed the GIRG weight array: n floats, non-integer (power-law), min near w_min.
    assert call["degrees"].shape == (N,)
    assert not np.allclose(call["degrees"], np.round(call["degrees"])), (
        "sampler was fed integers — expected GIRG weights, not graph degrees")
    assert abs(call["degrees"].min() - GIRG_CFG["w_min"]) < 0.05
    assert call["mu_bar"] == MU and call["gamma"] == 1.0 and call["kappa"] == KAPPA
    # Task Q invariant: realized mu-bar exact unless infeasible.
    stats = call["stats"]
    if not stats.get("infeasible", False):
        assert abs(stats["realized_mu_bar"] - MU) < 1e-6, (
            f"realized_mu_bar {stats['realized_mu_bar']} != nominal {MU}")
    assert 0.0 <= frac <= 1.0 and rounds >= 0


def test_gnp_path_unchanged(monkeypatch):
    spy = _Spy(runner.sample_degree_dependent_fears)
    monkeypatch.setattr(runner, "sample_degree_dependent_fears", spy)
    frac, rounds = runner.run_single_trial(
        _trial_args({"type": "gnp"}, {"type": "global"}))
    assert spy.calls == [], "gnp must keep homogeneous fears"
    assert 0.0 <= frac <= 1.0


def test_girg_trial_deterministic():
    a = runner.run_single_trial(_trial_args(GIRG_CFG, {"type": "global", "gamma": 1.0}, seed=99))
    b = runner.run_single_trial(_trial_args(GIRG_CFG, {"type": "global", "gamma": 1.0}, seed=99))
    assert a == b, "girg trial not deterministic given child_seed"


def test_girg_fear_stream_discipline(monkeypatch):
    """Fears must come from rng_fear (child stream 2) after weights from
    rng_graph (child stream 0) — recompute the exact expected fears offline
    and require bit-identity. Catches a wiring that uses the right sampler on
    the wrong stream, which the spy alone cannot see."""
    from twocascade.girg import sample_torus_points, sample_powerlaw_weights
    from twocascade.graphs import sample_degree_dependent_fears as wf

    seed = 4242
    spy = _Spy(runner.sample_degree_dependent_fears)
    monkeypatch.setattr(runner, "sample_degree_dependent_fears", spy)
    runner.run_single_trial(_trial_args(GIRG_CFG, {"type": "global", "gamma": 1.0}, seed=seed))

    child_seeds = np.random.SeedSequence(seed).spawn(4)
    rng_graph = np.random.default_rng(child_seeds[0])
    rng_fear = np.random.default_rng(child_seeds[2])
    sample_torus_points(N, rng_graph)  # consume, matching runner order
    exp_weights = sample_powerlaw_weights(N, GIRG_CFG["tau"], GIRG_CFG["w_min"], rng_graph)
    exp_fears, _ = wf(exp_weights, MU, 1.0, KAPPA, rng_fear)

    call = spy.calls[0]
    assert np.array_equal(call["degrees"], np.asarray(exp_weights, dtype=float)), (
        "girg fears fed different weights than rng_graph's draw")
    assert call["fears"] == list(exp_fears), (
        "girg fears differ from the rng_fear-stream expectation — wrong stream or order")


def test_girg_gamma_zero_mean_fear_matches_mu(monkeypatch):
    spy = _Spy(runner.sample_degree_dependent_fears)
    monkeypatch.setattr(runner, "sample_degree_dependent_fears", spy)
    runner.run_single_trial(_trial_args(GIRG_CFG, {"type": "global", "gamma": 0.0}, seed=7))
    fears = np.array(spy.calls[0]["fears"])
    # Beta(mu*k, (1-mu)*k): sd <= sqrt(mu(1-mu)/(k+1)) ~ 0.283; se at n=600 ~ 0.0116.
    assert abs(fears.mean() - MU) < 0.06, f"gamma=0 mean fear {fears.mean():.4f} far from {MU}"
