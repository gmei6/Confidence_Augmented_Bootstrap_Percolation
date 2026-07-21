# Task R — Cross-round remote-ignition tracker (Q5 nucleation-law caveat)

**Queued:** 2026-07-17. **Conjecture under test:** C-Q5(i) — the nucleation law for remote
ignition. Currently an "honest negative" (slope ~1.2–1.5, constant leak, not the pre-registered
g²), but read with a known measurement caveat this task exists to close.

**Autonomous-safe: NOT YET** — no code exists for this yet, and what's needed is a genuine
methodology decision (what counts as a cross-round nucleus), not just a parameter sweep. Should
be drafted and reviewed via `/research-cycle` before being run. Likely **does not** require
touching `src/twocascade/geometry.py` — see design note below — so once drafted it can probably
follow the existing precedent (Tasks E–P: script-only additions under `scripts/`, Local Mode,
still gated by the `/verify` reviewer→critic→auditor cycle before being marked done, per
`docs/queue/README.md`) rather than needing worktree isolation. Flagged here rather than
started blind because the tracker's definition of "nucleus" directly determines the result.

## Problem

`geometry.py`'s `remote_nucleation` (see `EXPLAINER.md` §7.5) counts, **per round**, whether
that round's remote failures cluster into a genuine second seed (an r-clique within `2·r_n`).
But `failed_neighbor_count` is cumulative and permanent across rounds, while nucleus counting is
not — two lone remote failures in the same area in *different* rounds can jointly satisfy the
solvency channel without ever co-occurring in a single round's nucleus check. The current
C-Q5(i) reading is therefore a **documented lower bound** on remote ignition
(`okf/open-questions.md` Q5), not the full picture, and the "honest negative" verdict rests on
that lower bound.

## Proposed design (script-only, no `geometry.py` changes)

`geometry.py` already exports the primitives needed: `remote_failures` (per-round remote set),
and the r-clique-on-a-rebuilt-subgraph check `remote_nucleation` performs internally. A new
driver script (e.g. `scripts/run_task_r_cross_round.py`, modeled on
`scripts/run_task_o_duration.py`'s structure) can:

1. Run the cascade as usual (`run_cascade_local_fear`), but **accumulate** each round's remote
   failures into a running set instead of discarding them at the end of the round.
2. At the end of the run (or on a rolling window, to bound cost), apply the same
   loose-component-then-r-clique check `remote_nucleation` uses internally, but over the
   **accumulated cross-round set** rather than a single round's set.
3. Compare against the existing per-round `remote_nucleation` counts on the same trials to
   quantify how much the lower bound was undercounting.

This composes existing exported functions without modifying `geometry.py` — if that holds up
under actual implementation (it might not; the internal r-clique check may need refactoring out
of `remote_nucleation` to be reusable standalone), flag and re-scope rather than force it.

## Scope

- Grid: reuse the S-046/S-048 Task O geometry (hard RGG, disc seeding) at 1–2 representative
  `n` values first (not the full 4-point n-sweep) to validate the approach before spending the
  full compute budget.
- Output: a comparison of per-round vs. cross-round nucleus counts, and whether the g² vs.
  constant-leak distinction changes once cross-round pairs are counted.

## Reports / context

`docs/queue/reports/task_o_report.md`, `EXPLAINER.md` §7.5 ("Known measurement caveat"),
`okf/open-questions.md` Q5.
