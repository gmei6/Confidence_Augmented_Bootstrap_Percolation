---
type: Decision
title: "D-035: Retire the Task R cross-round strict-r_n-clique metric and its real-vs-null z-test as confounded; C-Q5(i) cross-round question stays open pending a supra-r_n cross-K"
mutability: append-only
timestamp: 2026-07-19
tags: [q5, task-r, c-q5i, cross-round, methodology, structural]
---

# D-035: Retire the cross-round strict-r_n-clique metric / z-test (Task R)

## Decision
The Task R operationalization of "cross-round remote nucleation" as a **pooled strict-r_n-clique
count**, together with its **real-vs-null z-test and pre-registered decision rule**
(`DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS` vs `PURSUE_FULLER_SWEEP`), is **retired**. It is
not a valid test of C-Q5(i) cross-round spatial correlation. The C-Q5(i) cross-round question
remains **OPEN**; the valid instrument is a supra-r_n cross-type statistic (pair-correlation
g(d) / Ripley cross-K between early- and late-round remote-nucleus centroids at d ∈ (r_n,
k·r_n]) — deferred (Task R "Option B").

## Rationale
1. **The metric is structurally blind by construction.** A node is certified remote in round
   *t* only if it is > r_n from every previously-failed node, so any later-round remote node is
   > r_n from every earlier remote node. No real cross-round pair is ever within r_n, hence no
   cross-round strict-r_n-clique can form — `round_gap == 0` for all nuclei by necessity (proof;
   confirmed by 0 violations in 295,403 cross-round pairs, min dist/r_n = 1.0002). The observed
   "absence" is a tautology of the measurement, not evidence about the physics.
2. **The null is asymmetrically confounded.** The matched null draws per-round from the eligible
   pool without the cross-round r_n-exclusion the real process enforces, so it admits cross-round
   cliques the real process forbids (83–87% of null nuclei are cross-round), inflating null
   counts 2.5–4.6× real and driving z strongly negative for a purely structural reason.
3. **Task O's caveat is not closed by this.** Cross-round ignition via physical
   `failed_neighbor_count` accumulation (two lone remote failures in the same ball in different
   rounds still ignite at r=2, `okf/lessons.md`) is a mechanism this metric cannot see. The
   Q5 cross-round lower-bound caveat therefore stays open.

## Relationship to prior state
- The s-055 counting-collapse fix (iterative clique-peeling, `e066fd8`) is retained and correct —
  it is what made this structural fact legible. This decision does not reverse it.
- Supersedes the S-055 provisional `DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS` reading and the
  Task R "pre-registered decision rule" as the basis for a C-Q5(i) conclusion.

## Affects
`okf/open-questions.md` Q5 (C-Q5(i)); `scripts/analyze_task_r_cross_round.py`;
`docs/queue/reports/task_r_cross_round_report.md`; session `s-057`.
