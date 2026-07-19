---
type: Session Change
title: "S-055: Task R — cross-round pilot built and run; BLOCKED on a counting-method flaw the pilot itself surfaced"
description: "scripts/run_task_r_cross_round.py + analyze + tests built and executed per a 3-round-critiqued plan; the pilot's own diagnostics revealed the pooled nucleus-counting method collapses distinct per-round nuclei into oversized merged components, invalidating the z-score verdict. Paused pending Gary's go-ahead on the fix (iterative clique-peeling) before any conclusion is drawn."
mutability: append-only
timestamp: 2026-07-18
tags: [q5, task-r, pilot, blocked, methodology]
---

# S-055: Task R — cross-round pilot built and run; BLOCKED on a counting-method flaw

## Status: PAUSED — awaiting Gary's go-ahead on a methodology pivot before re-running.

**Do not trust `results/q5_task_r_cross_round_raw.json` or
`results/processed/task_r_cross_round_analysis.json` as they stand** — both are
provisional, produced by a flawed nucleus-counting method (see below), and superseded
the moment the fix lands. Their `DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS` verdict is
**not a real finding**; it's an artifact of the bug.

## What was built (Local Mode, no `src/` changes, not yet git-committed)

- `scripts/run_task_r_cross_round.py` — the pilot driver.
- `scripts/analyze_task_r_cross_round.py` — real-vs-null z-score analysis + the
  pre-registered decision rule.
- `tests/test_task_r_cross_round.py` — 3/3 passing; confirms the duplicated
  `_pooled_nucleus_count` clustering logic exactly reproduces `remote_nucleation`'s
  (`src/twocascade/geometry.py`) output on single-round data.

All three files are new, untracked (`git status` confirms), not yet committed — hold
off committing until the fix below lands and re-verifies.

## How the plan got here (3 blind critic rounds, all resolved)

1. Round 1: naive whole-trial pooling risks a **depletion confound** — as the cascade
   front consumes the torus, remaining remote-eligible area shrinks, so unrelated
   remote failures from different rounds become more likely to land close together by
   sheer geometric coincidence, not genuine correlated secondary nucleation (worse at
   higher mu_bar, exactly where a real g^2 signal would be hoped for). Fixed via a
   matched null model: K replicates redraw the same per-round *count* of "fake" remote
   failures from the real per-round eligible pool, preserving depletion structure while
   destroying genuine spatial correlation.
2. Round 2: the null itself needed statistical rigor (K replicates + a real-vs-null
   z-score, not a single draw) and pipeline consistency (same checks on real and null).
3. Round 3: needed explicit resolution limits, per-trial excess reporting, a
   pre-registered decision rule (z>2 in >=2/3 cells -> pursue a fuller sweep), and a
   scope trim (dual attribution convention real-only, not x null).

Full Final Brief is in the conversation this session; not separately filed to
`docs/queue/` (the pilot design lives in the two scripts' docstrings instead).

## What the pilot pass found (n=4000, mu_bar in {0.2, 0.4, 0.6}, 10 trials/cell, K=30)

Fast: 5.3s wall-clock for the whole pilot (30 trials + 30 null replicates each) — no
cost concern at this scale, contrary to the pre-run worry about O(n x |failed|)
eligible-pool cost.

**But the core numbers are logically impossible for a valid pooling method:**

| mu_bar | per_round_nuclei_total | real_cross_round_n_nuc |
|---|---|---|
| 0.2 | 43 | 42 |
| 0.4 | 100 | 55 |
| 0.6 | 158 | 30 |

Pooling should only ever find as many or MORE nuclei than per-round counting (strictly
more candidate pairings available), never fewer. Something is broken.

**Root cause, diagnosed via `real_nuclei_meta`:** nearly every detected pooled nucleus
has `possible_merged_component: True`, with `component_size` values like 123, 144,
171, 180 against a winning-clique `size` of only 2-3, and `round_gap: 0` on every one
(the winning clique itself is always same-round). What's happening: pooling an entire
trial's remote failures (potentially hundreds, across dozens of rounds) into ONE
"loose graph (2*r_n) -> connected components -> one clique per component" pass lets
far-apart, physically-unrelated local clusters get transitively bridged into a single
giant connected component via intervening rounds' remote failures scattered across the
torus. `_pooled_nucleus_count` only reports **one nucleus per connected component** —
a convention correctly inherited from `remote_nucleation` (verified exact-match on
single-round data by the test file), but that assumption silently breaks at
whole-trial-pool scale: many genuinely separate per-round nuclei are getting merged
into a handful of giant components and collapsed to a single count each. This is
exactly the failure mode the `possible_merged_component` flag (added per a round-3
critic ask) was built to catch — and it's firing on almost everything, not as a rare
edge case. The safeguard worked; the underlying design didn't.

**Implication:** the pilot's pre-registered decision rule technically fired
(`DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS`, 0/3 cells passed z>2), but this is
answering the wrong question — the low `real_cross_round_n_nuc` isn't evidence about
depletion vs. genuine cross-round physics, it's an artifact of the counting method
collapsing multiple genuine nuclei into one. **No conclusion about C-Q5(i) can be
drawn from this pilot run as it stands.**

## The proposed fix (not yet implemented — this is the resume point)

In `_pooled_nucleus_count` (`scripts/run_task_r_cross_round.py`), instead of taking
just the single largest clique per connected component, **iteratively peel maximal
cliques**: find the largest clique >= r in the component's strict-r_n subgraph, count
it as one nucleus, remove its members, re-run `find_cliques` on the remainder, repeat
until no clique >= r remains. This properly counts multiple non-overlapping nuclei
within an oversized merged component instead of collapsing them to one, while still
correctly handling the normal (small, single-round) case identically to today (a
component with exactly one clique still yields exactly one nucleus).

## Next steps for whoever resumes this (in order)

1. Get Gary's go-ahead on the peeling fix (was mid-ask when this session paused —
   see the conversation's last exchange before this handoff was written).
2. Implement the peeling loop in `_pooled_nucleus_count`.
3. Add new test cases to `tests/test_task_r_cross_round.py` specifically for the
   peeling behavior: e.g. two genuinely disjoint r-cliques whose members are bridged
   into one connected component by an unrelated intervening point should now count
   as 2 nuclei, not 1 (the case this pilot run showed collapsing in production data).
   Keep the existing 3 tests passing (they test the un-peeled single-clique case,
   which must still work identically when a component contains only one clique).
4. Re-run `scripts/run_task_r_cross_round.py` (same CONFIG, same base_seed — fully
   reproducible) and `scripts/analyze_task_r_cross_round.py`.
5. Re-evaluate the decision rule with the corrected counts. Only THEN is
   "pursue a fuller n=8000+ sweep" vs. "depletion-explained, honest-negative stands"
   a trustworthy verdict.
6. Once the design is confirmed working, run `/verify` (reviewer -> critic -> auditor)
   before committing the scripts/tests, per this project's standard gate for
   non-trivial script logic (this is Local Mode, no worktree needed, but the
   verification gate itself still applies before marking Task R done).

## Reports / context

`docs/queue/task_R_cross_round_remote_ignition.md` (original task file),
`EXPLAINER.md` SS7.5, `okf/open-questions.md` Q5, `docs/queue/reports/task_o_report.md`
(the honest-negative reading this task exists to sharpen).
