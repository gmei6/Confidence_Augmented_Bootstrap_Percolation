"""
Integration and edge cases tests for twocascade runner, analysis, and fear boundaries.
"""

import os
import json
import pytest
import numpy as np

import types

import twocascade.runner as runner_mod
from twocascade.runner import (
    run_sweep,
    run_single_cell_cpp,
    _validate_cpp_engine_support,
    _GIRG_FEAR_CAP_EPSILON,
    REPO_ROOT,
)
from twocascade.analysis import analyze_sweep, load_raw_results
from twocascade.reference import sample_individual_fears, choose_seed, sample_gnp_adjacency

CPP_BIN = REPO_ROOT / "cpp" / "build" / "twocascade_run"
has_cpp_bin = CPP_BIN.exists()

@pytest.mark.parametrize("engine", [
    "python",
    pytest.param("cpp", marks=pytest.mark.skipif(not has_cpp_bin, reason="C++ engine binary not built"))
])
def test_sweep_and_analysis_integration(tmp_path, engine):
    """Run a micro-sweep and verify that runner and analysis integrate correctly for the selected engine."""
    config_data = {
      "engine": engine,
      "pinned_params": {
        "n": 50,
        "r": 2,
        "concentration": 50.0, 
        "theta": 0.5,
        "window_len": 1,
        "weights": None,
        "target_high_degree": False
      },
      "scaling": {
        "n_ref": 50,
        "target_mean_degree": 4.0,
        "alpha": 0.7
      },
      "sweep": {
        "mean_fear_grid": [0.0, 0.3],
        "seed_multiples": [0.8, 1.2],
        "trials_per_cell": 3,
        "base_seed": 42
      },
      "output": {
        "raw_filepath": str(tmp_path / "sweep_test_raw.json")
      }
    }
    
    config_path = tmp_path / "test_config.json"
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=2)
        
    # Run the sweep
    run_sweep(str(config_path), num_processes=1)
    
    # Check output exists
    assert os.path.exists(config_data["output"]["raw_filepath"])
    
    # Load and check JSON structure
    raw_results = load_raw_results(config_data["output"]["raw_filepath"])
    assert "metadata" in raw_results
    assert raw_results["metadata"]["engine"] == engine
    assert "results" in raw_results
    assert len(raw_results["results"]) == 4 # 2 mus * 2 multiples
    
    # Check index mapping is present
    for cell in raw_results["results"]:
        assert "mean_fear_idx" in cell
        assert "seed_multiple_idx" in cell
        assert len(cell["failed_fractions"]) == 3
        
    # Run analysis
    analysis_results = analyze_sweep(raw_results)
    assert "metadata" in analysis_results
    assert "processed_cells" in analysis_results
    assert len(analysis_results["processed_cells"]) == 4
    
    # Verify linear crossing calculations don't crash
    assert "crossings_mu" in analysis_results
    assert "empirical_thresholds" in analysis_results


# --------------------------------------------------------------------------- #
# G4 runner dispatch: which CLI the C++ worker actually builds, and which
# configs the cpp path must REFUSE. Before these tests the whole G4 dispatch
# layer was covered only by prose in the walkthrough -- the C++ binary's own
# suite cannot see runner.py, and the cross-language suite drives the binary
# directly rather than through run_single_cell_cpp.
# --------------------------------------------------------------------------- #


def _fake_completed_process(trials):
    """Stand-in for subprocess.CompletedProcess with parseable engine output."""
    return types.SimpleNamespace(
        returncode=0,
        stdout="".join("0.250000 3\n" for _ in range(trials)),
        stderr="",
    )


def test_cpp_worker_threads_girg_flags_into_the_binary_invocation(monkeypatch):
    """A girg graph_cfg must reach the C++ binary as --graph-type girg plus the
    three model parameters. Captures the subprocess call instead of requiring
    the binary, so this locks the dispatch contract even on an unbuilt tree --
    and it is the dispatch contract, not the binary, that was untested."""
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return _fake_completed_process(trials=3)

    monkeypatch.setattr(runner_mod.subprocess, "run", fake_run)

    graph_cfg = {"type": "girg", "tau": 2.7, "w_min": 0.245, "alpha_g": 1.4}
    args = (
        1000,            # n
        0.004,           # p (unused by the binary in girg mode)
        2,               # r
        0.2,             # mu
        50.0,            # kappa
        7,               # a
        3,               # trials_per_cell
        1,               # window_len
        None,            # weights
        graph_cfg,
        np.random.SeedSequence(4242),
        "/nonexistent/twocascade_run",
    )
    outcomes = run_single_cell_cpp(args)
    assert outcomes == [(0.25, 3)] * 3

    cmd = captured["cmd"]

    def flag_value(flag):
        assert flag in cmd, f"{flag} missing from C++ invocation: {cmd}"
        return cmd[cmd.index(flag) + 1]

    assert flag_value("--graph-type") == "girg"
    assert float(flag_value("--tau")) == 2.7
    assert float(flag_value("--w-min")) == 0.245
    assert float(flag_value("--alpha-g")) == 1.4
    # The shared cascade parameters must still be threaded through.
    assert flag_value("--n") == "1000"
    assert flag_value("--r") == "2"
    assert flag_value("--seed-size") == "7"
    assert flag_value("--trials") == "3"
    # --graph-file would make the binary reject --graph-type girg outright.
    assert "--graph-file" not in cmd


def test_cpp_worker_omits_girg_flags_for_gnp(monkeypatch):
    """The gnp path must not acquire GIRG flags -- the mirror of the test above,
    so a future edit cannot make --graph-type unconditional."""
    cmds = []

    def fake_run(cmd, **kwargs):
        cmds.append(cmd)
        return _fake_completed_process(trials=2)

    monkeypatch.setattr(runner_mod.subprocess, "run", fake_run)
    args = (
        500, 0.01, 2, 0.1, 50.0, 5, 2, 1, None,
        {"type": "gnp"}, np.random.SeedSequence(1), "/nonexistent/twocascade_run",
    )
    run_single_cell_cpp(args)
    cmd = cmds[0]
    for flag in ("--graph-type", "--tau", "--w-min", "--alpha-g"):
        assert flag not in cmd, f"{flag} leaked into the gnp invocation: {cmd}"


def test_cpp_validation_rejects_girg_with_nonzero_gamma():
    """gamma != 0 has no C++ implementation; the girg cpp path exists only
    because gamma == 0 collapses onto the global-kappa fear model."""
    with pytest.raises(ValueError, match="gamma"):
        _validate_cpp_engine_support(
            {"type": "girg", "tau": 2.5},
            {"type": "global", "gamma": 0.5},
            "uniform",
            [0.0, 0.3],
        )


@pytest.mark.parametrize("layout", ["disc"])
def test_cpp_validation_rejects_non_uniform_seed_layout(layout):
    """The C++ binary always seeds uniformly at random. Dispatching a disc-seeded
    config to it would run a completely different shock geometry and report it
    under the requested name -- silent, not a crash."""
    with pytest.raises(ValueError, match="seed_layout"):
        _validate_cpp_engine_support(
            {"type": "girg", "tau": 2.5},
            {"type": "global", "gamma": 0.0},
            layout,
            [0.0, 0.3],
        )
    # ... and the same guard must hold for the gnp cpp path.
    with pytest.raises(ValueError, match="seed_layout"):
        _validate_cpp_engine_support({"type": "gnp"}, {"type": "global"}, layout, [0.0])


def test_cpp_validation_rejects_mean_fear_above_the_girg_cap():
    """Above 1 - 1e-3 the Python girg path (capped mu + Beta) and the C++ path
    (point mass at 1.0 for mu == 1.0) are different distributions."""
    cap = 1.0 - _GIRG_FEAR_CAP_EPSILON
    with pytest.raises(ValueError, match="mean_fear_grid"):
        _validate_cpp_engine_support(
            {"type": "girg", "tau": 2.5}, {"type": "global", "gamma": 0.0},
            "uniform", [0.0, 0.5, 1.0],
        )
    # Exactly at the cap is fine -- that is the value the Python path clips to.
    _validate_cpp_engine_support(
        {"type": "girg", "tau": 2.5}, {"type": "global", "gamma": 0.0},
        "uniform", [0.0, cap],
    )


def test_cpp_validation_accepts_supported_girg_config():
    """Guard against the checks above being satisfiable only by refusing
    everything: the supported combination must still pass."""
    _validate_cpp_engine_support(
        {"type": "girg", "tau": 2.5, "w_min": 0.245, "alpha_g": 1.2},
        {"type": "global", "gamma": 0.0},
        "uniform",
        [0.0, 0.2, 0.4],
    )


def test_cpp_validation_rejects_girg_config_missing_tau():
    """graph.type='girg' without graph.tau used to pass this gate and then
    KeyError inside a multiprocessing Pool worker, because run_single_cell_cpp
    subscripts graph_cfg["tau"] directly while building the command line.

    The second half of this test is the deliberate NON-check: w_min and alpha_g
    are omitted and the config must still be ACCEPTED, because both engine
    paths default them to the same values (1.0 / 1.2). This gate exists to
    reject configs where cpp would silently simulate a different model than the
    config describes; identical defaults on both sides are not that, and
    requiring the keys here would reject configs the python path runs happily.
    """
    with pytest.raises(ValueError, match="tau"):
        _validate_cpp_engine_support(
            {"type": "girg", "w_min": 0.245, "alpha_g": 1.2},
            {"type": "global", "gamma": 0.0},
            "uniform",
            [0.0, 0.2],
        )
    _validate_cpp_engine_support(
        {"type": "girg", "tau": 2.5},
        {"type": "global", "gamma": 0.0},
        "uniform",
        [0.0, 0.2],
    )


def test_run_single_cell_cpp_really_keyerrors_without_tau():
    """The failure the gate above prevents is real, not hypothetical: without
    a 'tau' key the worker raises KeyError while assembling argv, before the
    binary is ever launched (so this needs no built C++ engine, and the guard
    is what turns that opaque child-process KeyError into a config error).
    """
    cell_seed = np.random.SeedSequence(0)
    args = (
        50, 0.05, 2, 0.1, 50.0, 3, 1, 1, None,
        {"type": "girg", "w_min": 0.245, "alpha_g": 1.2},
        cell_seed,
        "/nonexistent/twocascade_run",
    )
    with pytest.raises(KeyError, match="tau"):
        run_single_cell_cpp(args)


@pytest.mark.skipif(not has_cpp_bin, reason="C++ engine binary not built")
def test_run_sweep_rejects_unsupported_cpp_config_end_to_end(tmp_path):
    """The validator is wired into run_sweep's explicit-engine path, not merely
    defined next to it."""
    config_data = {
        "engine": "cpp",
        "seed_layout": "disc",
        "graph": {"type": "girg", "tau": 2.5, "w_min": 0.245, "alpha_g": 1.2},
        "pinned_params": {
            "n": 50, "r": 2, "concentration": 50.0, "theta": 0.5,
            "window_len": 1, "weights": None, "target_high_degree": False,
        },
        "scaling": {"n_ref": 50, "target_mean_degree": 4.0, "alpha": 0.7},
        "sweep": {
            "mean_fear_grid": [0.0], "seed_multiples": [1.0],
            "trials_per_cell": 1, "base_seed": 42,
        },
        "output": {"raw_filepath": str(tmp_path / "never_written.json")},
    }
    config_path = tmp_path / "bad_cpp_config.json"
    with open(config_path, "w") as f:
        json.dump(config_data, f)

    with pytest.raises(ValueError, match="seed_layout"):
        run_sweep(str(config_path), num_processes=1)
    assert not os.path.exists(config_data["output"]["raw_filepath"])


def test_fear_channel_boundaries():
    """Verify boundary conditions for sample_individual_fears at mu = 0 and mu = 1."""
    rng = np.random.default_rng(123)
    n = 100
    
    # At mu = 0, all fears must be exactly 0
    fears_zero = sample_individual_fears(n, mean_fear=0.0, concentration=10.0, rng=rng)
    assert all(f == 0.0 for f in fears_zero)
    
    # At mu = 1, all fears must be exactly 1
    fears_one = sample_individual_fears(n, mean_fear=1.0, concentration=10.0, rng=rng)
    assert all(f == 1.0 for f in fears_one)


def test_targeted_seeding():
    """Verify that choose_seed with target_high_degree=True targets nodes with higher degrees."""
    rng = np.random.default_rng(999)
    n = 20
    p = 0.3
    
    # Sample a random graph
    adj = sample_gnp_adjacency(n, p, rng)
    
    # Find the degrees of all nodes
    degrees = [len(neighbors) for neighbors in adj]
    
    # Pick seed of size 3 targeted vs random
    seed_targeted = choose_seed(n, seed_size=3, adjacency=adj, rng=rng, target_high_degree=True)
    seed_random = choose_seed(n, seed_size=3, adjacency=adj, rng=rng, target_high_degree=False)
    
    # Check that degrees of targeted nodes are sorted in descending order
    targeted_degrees = [degrees[idx] for idx in seed_targeted]
    sorted_degrees = sorted(degrees, reverse=True)
    
    # The targeted seeds must be the highest degree nodes
    assert targeted_degrees == sorted_degrees[:3]





def test_fear_only_channel_terminates():
    """Verify that under p=0.0 (empty graph/disconnected), the fear-only channel behaves subcritically and halts quickly."""
    from twocascade.reference import make_nodes, run_cascade
    rng = np.random.default_rng(777)
    n = 200
    p = 0.0 # disconnected graph
    
    adj = sample_gnp_adjacency(n, p, rng)
    # E[f] = mu = 0.5 < 1.0 (subcritical)
    fears = sample_individual_fears(n, mean_fear=0.5, concentration=50.0, rng=rng)
    nodes = make_nodes(fears)
    
    # 5 seed failures. Since there are no edges, solvency channel does nothing.
    # The failures can only spread via the fear channel.
    seed_indices = choose_seed(n, seed_size=5, adjacency=adj, rng=rng, target_high_degree=False)
    
    result = run_cascade(adj, nodes, r=2, seed_indices=seed_indices, rng=rng, record_history=True)
    
    # Fear-only per-round offspring is mu * g_t = 0.5 * (a_{t-1}/n).
    # Since it is a subcritical branching process, it must terminate in o(n) steps with final failed fraction << 1.0 w.h.p.
    # For N=200, 5 seeds, it should terminate in a few rounds and fail only a handful of nodes.
    assert result.final_failed_fraction < 0.20, f"Failed too many nodes in fear-only sweep: {result.final_failed_fraction}"
    assert len(result.history) < 10, f"Branching process ran too long: {result.history}"
