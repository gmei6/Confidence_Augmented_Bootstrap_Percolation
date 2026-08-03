---
type: Session Change
title: "S-062: Comparison 2 (geometry: configuration model vs GIRG) delivered — GIRG sampler ported ~44x, calibrated, wired, and swept; Q6 gets an empirical answer, ungated at the final step"
description: "Reconstructed catch-up entry (backfilled 2026-08-03) for the 2026-08-02 poster-sprint arc C1-C3b: block-vectorized GIRG sampler port (AUDIT PASS), matched-degree calibration, degree-dependent fear wiring (AUDIT PASS), sweep progress instrumentation (AUDIT PASS), and the production sweep + analysis that answers Q6 (geometry barely moves ignition) but was never itself run through the blind /verify gate."
mutability: append-only
timestamp: 2026-08-02
tags: [poster, comparison-2, geometry, girg, q6, d-038, verify, audit-pass, backfilled]
---

# S-062: Comparison 2 (geometry) delivered — backfilled catch-up entry

**This entry is a reconstruction, not a same-day record**, written 2026-08-03 from commit
bodies, `task.md`/`implementation_plan.md`/`walkthrough.md` artifact conventions referenced in
each commit, and `git worktree`/branch state. The work happened 2026-08-02, in one day, across
five commits that took the GIRG comparison from "computationally out of reach" (pre-sprint
`okf/status.md`: pure-Python O(n²), ~2.7×10¹¹ pair evaluations for the planned sweep) to
delivered.

## The arc, commit by commit

**C1 — `6c5491a`: exact block-vectorized GIRG sampler, ~44× at n=10000.**
Replaces `sample_girg_adjacency`'s O(n²) pure-Python double loop with a block-vectorized numpy
evaluation of the identical kernel $p=\min(1,(w_iw_j/(nd^2))^\alpha)$ (torus distance, each
unordered pair evaluated once). No dense $n\times n$ array materialized (512×n block
temporaries). The pre-port loop is retained verbatim as `sample_girg_adjacency_slow` and serves
as the equivalence oracle. Measured 1.38 s/graph at n=10000 (was ~62 s extrapolated) — the
planned 3-arm 11-point×500-trial sweep drops from ~284h to ~6.4h of sampling.
Equivalence: per-pair probabilities bit-identical over 244k pairs (incl. forced min-branch and
coincident points); edge-set level-set identity fast-vs-slow at n=1300 across three blocks
(committed test `test_multiblock_level_set_identity`, added after the critic found the original
gate blind to cross-block edge loss — all its cases were single-block).
**Baseline isolation: worktree branch `c1-girg-fast-sampler`**, verified in this catch-up to
point at the identical commit SHA as the one landed on `antigravity` — the isolation mechanism
the constitution requires for any `src/` change was actually used, not skipped.
**Verification: blind reviewer→critic→auditor, AUDIT PASS.** C++ parity explicitly out of
scope — no C++ GIRG path exists; this implementation becomes the oracle if one is ever added
(recorded in the session's `implementation_plan.md`).

**C2 — `c1dcd84`: calibrate GIRG $w_{\min}$ to the matched mean degree.**
`scripts/calibrate_girg_degree.py` mirrors the Comparison-1 T1 calibration script
(SeedSequence-per-replicate, same `rng_graph`/`rng_pair` split as `runner.py:121-130`) and
bisects $w_{\min}$ against the configuration model's realized target from
`matched_degree_calibration.json`. Result at n=10000, τ=2.5, $\alpha_g$=1.2, 20 replicates,
base_seed=20260802: **$w_{\min}=0.186377$, achieved ⟨k⟩=4.5224±0.0772** vs target
4.5332±0.0257, 11 bisection iterations, converged. Validated on an independent seed set the
solver never saw (base_seed=31415, 20 replicates): ⟨k⟩=4.638±0.125, z=+0.84 vs target — not an
artifact of the fixed bisection replicates. Gate: `tests/test_girg_calibration.py`, 4/4
(determinism, monotonicity in $w_{\min}$, solver convergence, fast-sampler-only).
**Not a `src/` change** (config-generating script only) — no isolation branch, and **not** run
through the blind reviewer→critic→auditor gate. All three poster families now share
⟨k⟩=4.53 at n=10000.

**C3a — `8956d75`: GIRG trials use degree-dependent (water-filling) fears.**
Wires the `girg` path in `run_single_trial` to `graphs.py`'s Task Q water-filling
`sample_degree_dependent_fears`, fed the GIRG weight array (the drawn-degree analogue; the
$(w/\text{mean})^\gamma$ tilt is scale-invariant so the $w_{\min}$ scale cancels). This is a
direct consequence of D-038: geometry must be the *only* difference between the CM and GIRG
arms, so GIRG cannot be left on the homogeneous `sample_individual_fears` path CM does not use.
Every other family keeps `sample_individual_fears`, proven bit-identical base-vs-new across
gnp/rgg/soft_rgg/rgg+disc+local/CM (15/15 trials, reviewer and critic independently).
**Baseline isolation: worktree branch `c3-girg-fears`**, verified identical to the landed
commit. **Verification: blind reviewer→critic→auditor, AUDIT PASS.** Pre-existing defects
surfaced and explicitly queued, not fixed here: `girg+local` fear `UnboundLocalError` on
`r_n` (crashes on the pre-existing base too, not a regression); CM and GIRG branches both
discard the fear-stats dict including the infeasible flag (must be surfaced before any
high-$\gamma$ GIRG sweep; the poster sweeps run $\gamma=0$, where this cannot fire).
Reproducibility note recorded in the commit: old GIRG runs regenerate statistically, not
bit-identically, after this change — no §5.6-stamped GIRG result existed before it
(Task P was demoted, D-037), so nothing auditable breaks.

**C3b-obs — `0179110`: progress output for Python sweeps.**
The Python sweep path was a single blocking `pool.map` — ahead of the ~4h Comparison-2
production run, a stall would have been indistinguishable from a healthy run. Change: ordered
`pool.imap` (same chunksize) with progress lines every `max(1, total//20)` completions plus a
guaranteed final line. `imap` preserves `map`'s result order, so index-aligned per-cell
aggregation is unchanged; `imap_unordered` is forbidden and its absence gate-enforced (it would
silently permute trials across cells). Equivalence: 9-cell sweep bit-identical base-vs-new
excluding timestamp/git_commit metadata. Gate: `tests/test_sweep_progress.py`, 3 tests — one
assertion was corrected during verification because **the test was wrong** (constitution case
a, not a code regression): its line filter matched pytest's own `Raw results saved to <path>`
line since pytest's tmp dir embeds the test name; tightened to `^progress:`.
**Baseline isolation: worktree branch `c3b-sweep-progress`**, verified identical to the landed
commit. **⚠️ This worktree is still checked out** at `/Users/garymei/Downloads/projects/tc-work`
as of this catch-up (2026-08-03) — clean working tree, but never removed; carried into
`okf/next-actions.md` as housekeeping. **Verification: blind reviewer→critic (combined, small
diff)→auditor, AUDIT PASS.**

**C3b — `2024c23`: GIRG comparison arms — geometry barely moves ignition; poster hero goes to
9 curves.** The result-delivering commit, and the one step in this arc with no `/verify` gate.
Three GIRG arms ($\bar\mu\in\{0,0.4,0.7\}$, n=10000, 500 trials/cell, calibrated
$w_{\min}=0.186377$, degree-dependent fears, on the C1 fast sampler). A 100-trial log-spaced
pilot bracketed the transitions; production grids densified around them (8/9/9 interior
points, bar was ≥3). Wall time 40/96/57 min per arm.

**Result (empirical P=0.5 crossings, verified against `results/processed/poster_comparison.json`
in this catch-up, not just the commit prose):**

| family | $\bar\mu=0$ | $\bar\mu=0.4$ | $\bar\mu=0.7$ |
|---|---|---|---|
| ER  | 313.6 | 111.0 | 30.8 |
| CM  | 10.2  | 6.8   | 4.3  |
| GIRG| 11.4  | 7.3   | 4.3  |

1. **Geometry barely moves ignition.** GIRG sits ~11.7% above CM at zero fear (11.408/10.217 =
   1.1166; commit prose rounds to "~11%") — a real but small locality penalty, dwarfed by the
   ~30× heterogeneity gap to ER at matched ⟨k⟩=4.53. Hubs, not distance, set the threshold.
2. **The D-012 departure follows the degree distribution, not geometry.** From GIRG's own
   $\bar\mu=0$ anchor, measured/predicted = 1.783 at $\bar\mu=0.4$ (`d012_table` in the
   processed JSON), close to CM's 1.839. GIRG's $\bar\mu=0.7$ row is EXCLUDED for the same
   reason as CM's: predicted crossing 1.027, below the r=2 structural floor
   (`below_floor: true` in the JSON, confirmed by direct inspection).

**Poster hero figure confirmed (by reading `scripts/plot_poster_comparison.py`'s
`series_config`, not inferred from prose) to plot exactly 9 series** — 3 families ×
$\bar\mu\in\{0,0.4,0.7\}$ — out of the 15 curves now in `poster_comparison.json`; the other 6
(ER/CM at $\bar\mu\in\{0.1,0.2,0.3\}$, from S-061) feed `scaling_law_departure.png` instead.
This resolves the "one-axis vs. separate figures" design question — recorded only as an inline
comment in `okf/poster/poster.tex:78-82` ("Gary accepted the 9-curve figure as the hero"), not
as a `d-0NN` decision file. **Flagged as a judgment call in `EVIDENCE.md`:** whether this
warrants a formal decision entry (the pattern D-037 set for Q6-adjacent results) is left for
the orchestrator, since it was not in this catch-up's requested file list.

`okf/poster/poster.tex` also picks up the §5.4 cross-engine disclosure here (closing
`next-actions` item 2c): "ER on the C++ engine; configuration model and GIRG on the Python
reference implementation (cross-engine agreement verified)."

**⚠️ Not `/verify`-gated.** This commit touches only `configs/`, `scripts/`,
`results/`, and `okf/poster/poster.tex` — no `src/` file — so per the constitution's own scope
rule it did not require baseline isolation or the full gate. But that also means **the
headline "geometry barely moves ignition" claim, the 9-curve figure, and the poster prose have
never been reviewed by a blind reviewer, critic, or auditor.** The commit body's own
verification note: "the analysis extension agent died on an API error after completing its
work; all outputs verified from disk against pre-delegation snapshots" — a self-check by the
same delegated process, not an independent one. This is the weakest evidentiary link in an
otherwise fully-gated arc, and it is the step that actually produces the number this session's
Q6 answer rests on.

## Files changed
`src/twocascade/girg.py`, `src/twocascade/runner.py` (C1, C3a, C3b-obs — each `/verify`-gated);
`scripts/bench_girg.py`, `scripts/calibrate_girg_degree.py`, `scripts/analyze_poster_comparison.py`
(extended to 3 families), `scripts/plot_poster_comparison.py` (GIRG series + plum ramp),
`scripts/run_poster_girg_pilots.py`, `scripts/run_poster_girg_production.py` (new);
`configs/poster_girg_mu{0,40,70}{,_pilot}.json` (new, 6 files);
`results/poster_girg_mu{0,40,70}{,_pilot}_raw.json` (new, 6 files);
`results/processed/girg_degree_calibration.json` (new), `results/processed/poster_comparison.json`
(extended to 15 curves), `results/figures/poster_comparison.png`,
`results/figures/scaling_law_departure.png` (both regenerated with the GIRG family present),
`okf/poster/poster.tex` (GIRG narrative + §5.4 disclosure + 9-curve hero);
`tests/test_girg_fast_equivalence.py`, `tests/test_girg_calibration.py`,
`tests/test_girg_fear_wiring.py`, `tests/test_sweep_progress.py` (new, all committed).

## Open at session close (still open as of this catch-up, 2026-08-03)
- The `tc-work` worktree (branch `c3b-sweep-progress`) is still checked out and unremoved.
- C3b's final analysis/figure/poster-text step has no `/verify` record — see the ⚠️ above and
  `EVIDENCE.md`. Recommend a `/verify` pass (or documented equivalent) before this result is
  cited on the physical poster as more than "strong preliminary."
- Whether the "9-curve hero" design choice warrants a `d-0NN` decision entry was not resolved
  here — flagged for the orchestrator.

## [Files Changed · Validation Status · New Decisions]
- **Files:** see above; full detail in the cited commits (`6c5491a`, `c1dcd84`, `8956d75`,
  `0179110`, `2024c23`).
- **Validation:** §5.4 N/A for C1/C3a/C3b-obs — no C++ GIRG path exists, explicitly out of
  scope in each commit's `implementation_plan.md`. C1, C3a, C3b-obs: blind reviewer→critic→
  auditor, **AUDIT PASS** each, on isolation branches verified identical to the landed commits.
  C2: own test suite (4/4), not `/verify`-gated. **C3b (the result-bearing commit): UNGATED —
  no reviewer, critic, or auditor involvement recorded.**
- **New Decisions:** None recorded in this catch-up. Candidate for a future `d-039` (Q6
  empirical resolution, symmetric with D-037's demotion) — see `EVIDENCE.md` judgment calls.
