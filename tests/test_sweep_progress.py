"""Gate test for C3b-obs: Python sweeps must emit progress and stay bit-identical.

Written before implementation; not the implementer's to edit. If an assertion
looks wrong, stop and say which and why.
"""
import inspect
import json
import os
import re

import pytest

from twocascade import runner


def _tiny_config(tmp_path, name):
    raw = tmp_path / f"{name}_raw.json"
    cfg = {
        "engine": "python",
        "pinned_params": {
            "n": 200, "r": 2, "concentration": 50, "theta": 0.5,
            "window_len": 5, "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
            "target_high_degree": False,
            "graph": {"type": "gnp"},
            "fear": {"gamma": 0.0},
        },
        "scaling": {"target_mean_degree": 4.5, "n_ref": 200, "alpha": 0.6},
        "sweep": {
            "mean_fear_grid": [0.0, 0.4],
            "seed_sizes": [2, 4, 8],
            "trials_per_cell": 10,
            "base_seed": 42,
        },
        "output": {"raw_filepath": str(raw)},
    }
    cfg_path = tmp_path / f"{name}.json"
    cfg_path.write_text(json.dumps(cfg))
    return str(cfg_path), str(raw)


def test_no_unordered_imap():
    src = inspect.getsource(runner)
    assert "imap_unordered" not in src, (
        "imap_unordered permutes trial results across cells — forbidden")


def test_progress_lines_and_determinism(tmp_path, capsys):
    cfg1, raw1 = _tiny_config(tmp_path, "a")
    runner.run_sweep(cfg1, num_processes=2)
    out = capsys.readouterr().out

    lines = [l for l in out.splitlines() if re.match(r"^progress:", l.strip())]
    assert len(lines) >= 3, f"expected >=3 progress lines, got {len(lines)}:\n{out}"

    counts = []
    for l in lines:
        m = re.search(r"(\d+)\s*/\s*(\d+)", l)
        assert m, f"progress line lacks done/total: {l!r}"
        counts.append((int(m.group(1)), int(m.group(2))))
    total = counts[0][1]
    assert total == 60, f"total should be 60 tasks (2 mu x 3 seeds x 10 trials), got {total}"
    dones = [c[0] for c in counts]
    assert dones == sorted(dones), f"progress counts not monotone: {dones}"
    assert counts[-1][0] == total, f"final progress line must report {total}/{total}"

    # Determinism: a second run must produce identical results.
    cfg2, raw2 = _tiny_config(tmp_path, "b")
    runner.run_sweep(cfg2, num_processes=2)
    r1 = json.load(open(raw1))["results"]
    r2 = json.load(open(raw2))["results"]
    assert r1 == r2, "sweep results changed between identical runs — ordering or seed drift"


def test_results_schema_unchanged(tmp_path):
    cfg, raw = _tiny_config(tmp_path, "c")
    runner.run_sweep(cfg, num_processes=2)
    data = json.load(open(raw))
    assert set(data.keys()) == {"metadata", "sweep_parameters", "results"}
    assert len(data["results"]) == 6  # 2 mu x 3 seed sizes
    for cell in data["results"]:
        assert len(cell["failed_fractions"]) == 10
        assert len(cell["rounds_completed"]) == 10
