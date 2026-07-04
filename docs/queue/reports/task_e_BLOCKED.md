# Task E — BLOCKED (environment cannot run simulations)

**Date:** 2026-07-04 (fable overnight run) · **Task file left in place:** `docs/queue/task_E_fear_trajectory_concentration.md`

## Where I stopped and why

Stopped at **Plan step 1–2 (configs / run)** before writing any files. This Docker sandbox
cannot execute any part of the task's Definition of Done:

- **No Python scientific stack.** The container's only Python is `/usr/bin/python3.11` with
  no `numpy`, `matplotlib`, `scipy`, or `pytest` installed anywhere on the filesystem
  (exhaustive `find /` for `numpy`/site-packages/wheels came up empty). There is no `pip`
  and no `ensurepip`.
- **No network.** `pypi.org`, `bootstrap.pypa.io`, `registry.npmjs.org`, and `github.com`
  are all unreachable (connection refused), so nothing can be installed.
- **C++ engine unusable and insufficient.** `cpp/build/twocascade_run` is a macOS arm64
  Mach-O binary (`exec format error` on this Linux container). `g++ 12` exists so it could
  be rebuilt — but Task E explicitly requires `engine="python"` to capture round-by-round
  histories, and the C++ engine only emits `(failed_fraction, rounds)` per trial anyway.

Every DoD line therefore fails in this environment: sweeps can't run (runner imports numpy),
raw files can't be produced through the sanctioned runner path, the figure can't be
generated (no matplotlib), and the unit-test gate can't run (no pytest/numpy).

I deliberately did **not** write the untested half (configs, `analyze_fear_field_concentration`,
plotting code, tests) — shipping unrunnable, unverified numerical code claiming partial
completion would violate the tracker's honesty rule and create silent-error risk.

## One design fact discovered for whoever resumes

`twocascade.runner.run_sweep` does **not** record per-round histories —
`run_single_trial` calls `run_cascade(..., record_history=False)` and stores only
`failed_fractions[]` / `rounds_completed[]` per cell (per D-014, histories are omitted by
default to prevent JSON bloat). Task E's analysis needs the generation-size trajectory
$a_k$, so the resume must add a history-capture path first. Recommended: an additive,
default-off config flag (e.g. `output.record_history: true`, python engine only, error on
`engine="cpp"`) in `runner.py`, or a dedicated `scripts/run_fear_concentration.py` that
mirrors the runner's stamping (config + `SeedSequence.spawn` seeding + git hash + timestamp)
and calls `run_cascade(..., record_history=True)`. Cumulative history → $a_k$ =
`history[k] - history[k-1]`, and $g_k = a_{k-1}/n$.

## Exact resume point

1. Fix the environment (rebuild the sandbox with `pip install -e .` per `requirements.txt`
   /`pyproject.toml`, or run on the host).
2. Add the history-capture runner path above (a `src/` change — baseline-isolation rules apply).
3. Then follow the task file from Plan step 1 unchanged.
