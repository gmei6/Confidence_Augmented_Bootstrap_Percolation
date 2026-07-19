---
type: Session Change
title: "S-057: Task R — counting bug fixed; strict-r_n-clique metric shown STRUCTURALLY BLIND to cross-round co-location; z-test retired"
description: "The s-055 nucleus-counting collapse is fixed via iterative clique-peeling (committed e066fd8); the corrected data reveals cross-round strict-r_n-cliques are structurally impossible under the remote-certification rule, so the metric cannot test C-Q5(i) and the real-vs-null z-test is retired as confounded. Task O's cross-round caveat stays OPEN. /verify AUDIT PASS."
mutability: append-only
timestamp: 2026-07-19
tags: [q5, task-r, c-q5i, cross-round, structural, z-test-retired, verified, d-035]
---

# S-057: Task R — cross-round remote-ignition tracker resolved (structurally), superseding the S-055 block

## Resolution of the S-055 block (Gary's Option A)
S-055 paused Task R on a nucleus-counting collapse. The **iterative clique-peeling fix**
(`_pooled_nucleus_count` peels the largest strict-r_n clique per component until none ≥ r
remain) was implemented and committed (`e066fd8`); tests 4/4. The stale pre-fix
raw/analysis (stamped `c4ef634`) were **regenerated** with the fixed script (`d70dbd8`,
`base_seed=20260718`). The counting bug is fixed: the superset property is restored at every
cell (real ≥ per-round: 43=43, 105≥100, 170≥158), and peeling recovers up to 24 nuclei per
merged component instead of collapsing each to 1.

## The deeper finding (why the negative is structural, not physical)
All 318 real nuclei have `round_gap == 0` — zero cross-round nuclei — and this is a **proof,
not luck**: a node is certified "remote" in round *t* only if it is > r_n from *every*
previously-failed node (`run_task_r_cross_round.py:262-266`), so any later-round remote node
is > r_n from every earlier remote node → no real cross-round pair is within r_n → no
cross-round strict-r_n-clique can form. The critic confirmed empirically: **0 violations in
295,403 cross-round pairs**, min cross-round distance / r_n = 1.0002.

This means the pooled-strict-r_n-clique metric is **structurally incapable of detecting
cross-round co-location** — a *tautology of the measurement*, NOT a claim that cross-round
ignition is physically absent (reviewer Issue 1, corrected in-session). Task O's cross-round
lower-bound caveat (physical `failed_neighbor_count` accumulation — two lone remote failures
in the same ball in different rounds still ignite at r=2, `okf/lessons.md`) is a mechanism
this metric cannot see, so it stays **OPEN**.

## The z-test is RETIRED as confounded
The matched null draws per-round from the eligible pool *without* the cross-round r_n-exclusion
the real process enforces, so it admits cross-round cliques the real process forbids — 83–87%
of null nuclei are cross-round (critic-measured), inflating null 2.5–4.6× real. The strongly
negative z (−15…−23) and its `DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS` label are a
structural artifact, not spatial physics. Demoted to a labeled `retired_confounded_ztest`
diagnostic (evidence retained, not deleted). See decision `d-035`.

## Valid follow-up (deferred, Option B)
A genuine cross-round test needs a supra-r_n cross-type statistic — pair-correlation g(d) /
Ripley cross-K between early- and late-round remote-nucleus centroids at d ∈ (r_n, k·r_n].
This is the *only* way to answer C-Q5(i)'s cross-round question, not merely optional.

## Files
- Changed: `scripts/analyze_task_r_cross_round.py` (reframed: `primary_verdict =
  STRICT_CLIQUE_METRIC_STRUCTURALLY_BLIND_TO_CROSS_ROUND` computed from the raw's round_gap,
  with `interpretation` + `task_o_caveat_status=OPEN`; z-test → `retired_confounded_ztest`).
- New: `docs/queue/reports/task_r_cross_round_report.md`, decision `okf/decisions/d-035-*.md`.
- Regenerated (gitignored): `results/q5_task_r_cross_round_raw.json`,
  `results/processed/task_r_cross_round_analysis.json`.
- Unchanged since `e066fd8`: `scripts/run_task_r_cross_round.py`, `tests/test_task_r_cross_round.py`.

## /verify
Reviewer conditional sign-off (Issue-1 framing fix applied), critic PASS (proof empirically
confirmed; null confound quantified), **AUDIT PASS**. `reference.py`/`geometry.py` untouched;
§5.4 N/A (geometric/python). Resolves `okf/next-actions.md` item 4; supersedes S-055.
