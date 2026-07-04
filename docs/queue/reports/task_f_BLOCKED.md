# Task F — BLOCKED (environment cannot run simulations)

**Date:** 2026-07-04 (fable overnight run) · **Task file left in place:** `docs/queue/task_F_counting_process_law_binomial_test.md`

## Where I stopped and why

Stopped at **Plan step 1–2 (configs / run)** before writing any files. Same environment gap
as Task E (see `task_e_BLOCKED.md` for the full diagnosis):

- No `numpy` / `matplotlib` / `pytest` anywhere; no `pip`; no network to install anything.
- `cpp/build/twocascade_run` is a macOS arm64 binary (exec format error on this Linux box) —
  and Task F requires `engine="python"` regardless (the `track_nodes`/`tracked_failure_rounds`
  diagnostic side-channel is Python-only per D-026).

The sweeps, the `evaluate_binomial_dispersion` analysis + bootstrap CI, the overdispersion
figure, and the test-suite gate are all unexecutable here, so no DoD item can be met. No
partial/untested artifacts were written.

## Note for whoever resumes

Like Task E, this task needs per-trial trajectory data ($S(t)$ at fixed rounds, e.g. $t=3$)
that `run_sweep` does not currently record. The same history-capture extension recommended
in `task_e_BLOCKED.md` covers Task F's needs — cumulative `history[t]` from
`run_cascade(..., record_history=True)` IS $S(t)$, which is simpler and cheaper than the
`track_nodes` side-channel the task file suggests (that channel maps node→failure-round for
a watched subset; full-population $S(t)$ comes free from `history`). Consider sharing one
set of raw runs between Tasks E and F where the grids overlap ($\mu \in \{0.3, 0.5\}$ cells)
— Task F additionally needs $\mu = 0.0$ cells.

## Exact resume point

1. Fix the environment (scientific Python per `requirements.txt`, or run on the host).
2. Add the shared history-capture runner path (see `task_e_BLOCKED.md`).
3. Then follow the task file from Plan step 1 unchanged.
