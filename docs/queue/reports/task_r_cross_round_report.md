# Task R — cross-round remote-ignition tracker (Q5, C-Q5(i)): resolved as a STRUCTURAL negative

**Sessions:** S-055 (built + pilot, BLOCKED on a counting flaw) → S-057 (2026-07-19,
counting flaw fixed, re-run, and resolved via Gary's **Option A** — structural reframing).
**Conjecture:** C-Q5(i) cross-round remote nucleation (does secondary remote nucleation in
later rounds cluster spatially with earlier-round nuclei?). **Mode:** Local (no `src/`
change). **Engine:** geometric (Q5 torus), `arch -arm64 python3`.

## Resolution in one line
The pooled strict-r_n-clique metric is **structurally blind to cross-round co-location** —
by the remote-certification rule, no real cross-round pair is ever within r_n, so
`round_gap == 0` for all 318 nuclei *by construction* (proof, empirically confirmed). This
is a **tautology of the measurement, not a physics result**: C-Q5(i)'s cross-round question
is *untestable* by this operationalization, and Task O's cross-round lower-bound caveat
(physical `failed_neighbor_count` accumulation, which this metric cannot see) stays **OPEN**.
The real-vs-null z-test is **retired as confounded**. The valid test is a supra-r_n cross-K
(**Option B**), deferred.

> **Correction (S-057 /verify, reviewer Issue 1):** an earlier draft framed this as a clean
> "structural negative" that "gives Task O's honest-negative a mechanism." That overstated —
> metric-blindness is not the same as physical absence. Corrected throughout.

## History (why this took two sessions)
- **S-055:** `run_task_r_cross_round.py` + `analyze_...` + `tests/` built through a
  3-round blind-critic plan. The pilot's own `possible_merged_component` safeguard fired on
  almost everything: pooling a whole trial's remote failures into one loose (2·r_n) graph
  bridged unrelated clusters into giant components (size 100–180), and the one-nucleus-per-
  component rule collapsed them — producing the logically-impossible `real < per_round`
  counts (42<43, 55<100, 30<158). **Paused for Gary's go-ahead on the fix.**
- **Peeling fix (committed `e066fd8`):** `_pooled_nucleus_count` now iteratively peels the
  largest strict-r_n clique (≥ r) per component (greedy disjoint-clique cover), recovering
  the multiple nuclei a giant component hides. Tests **4/4** (incl. the new peeling case).

## S-057 — what I did (Option A)
1. **Confirmed the fix is real, not just committed.** The on-disk raw/analysis (stamped
   `c4ef634`) predated `e066fd8`, so I **regenerated** both with the fixed script
   (`base_seed=20260718`, fully reproducible; 4.7s). New raw stamped `d70dbd8` (descendant
   of the fix). The superset property is restored at every cell: real ≥ per-round
   (43=43, 105≥100, 170≥158); `nuclei_in_component` now ranges up to 24 (giant components
   correctly decomposed instead of collapsed to 1). **The s-055 counting bug is fixed.**
2. **Found the deeper issue the corrected data exposes.** All 318 nuclei have
   `round_gap == 0` — zero cross-round nuclei. This is **structural, not empirical:** a node
   is certified remote in round *t* only if it is > r_n from *every previously-failed node*
   (`run_task_r_cross_round.py:259-266`), so any later-round remote node is > r_n from every
   earlier remote node → no real cross-round pair is within r_n → **no cross-round strict
   r_n-clique can ever form.** The pooled-strict-clique metric therefore *cannot* detect
   cross-round correlation for the real process.
3. **Showed the z-test is confounded.** The null (`:311-320`) draws per-round from the
   eligible pool **without** the cross-round r_n-exclusion the real process enforces, so it
   *does* form cross-round cliques → null is 2.5–4.6× real per trial (4.3→19.7, 10.5→32.8,
   17.0→43.2). The strongly-negative z (−15…−23) is a **structural artifact of an asymmetric
   null**, not spatial physics. The verdict `DEPLETION_EXPLAINED_HONEST_NEGATIVE_STANDS` is
   directionally safe (real can never exceed null) but is **not an informative test**.
4. **Reframed the analysis (Gary's Option A).** `analyze_task_r_cross_round.py` now emits
   `primary_verdict = STRICT_CLIQUE_METRIC_STRUCTURALLY_BLIND_TO_CROSS_ROUND` (computed from
   the raw: `structural_cross_round_nuclei_total = 0` of 318), with an `interpretation` field
   flagging it as a tautology of the measurement and `task_o_caveat_status = OPEN`; the z-test
   is demoted to `retired_confounded_ztest` with the confound stated. Nothing is asserted that
   the raw doesn't evidence.

## Result
| cell (μ̄) | per_round | real (pooled) | cross-round nuclei (round_gap>0) |
|---|---|---|---|
| 0.2 | 43 | 43 | **0** |
| 0.4 | 100 | 105 | **0** |
| 0.6 | 158 | 170 | **0** |

**Primary verdict: the strict-r_n-clique metric is STRUCTURALLY BLIND to cross-round
co-location** — 0/318 nuclei span rounds, by proof, so this operationalization *cannot test*
C-Q5(i). It is **not** a physics result: Task O's cross-round lower-bound caveat stays OPEN
(the metric cannot see `failed_neighbor_count` accumulation across rounds). The valid test is
Option B, deferred.

## What is deliberately deferred (Option B, not done this session)
A test that *can* see cross-round clustering needs a supra-r_n cross-type statistic —
a pair-correlation g(d) or Ripley cross-K between early- and late-round remote-nucleus
centroids at d ∈ (r_n, k·r_n] — a different measurement. **This is the only way to actually
answer C-Q5(i)'s cross-round question** (not merely optional), since the strict-clique metric
is definitionally blind to it.

## Definition of Done (§5.6)
- Reproducible from a committed driver + logged seed (`base_seed=20260718` in `CONFIG`);
  raw runner-stamped (config+seed+git `d70dbd8`+timestamp). Analysis read-only on the raw.
- §5.4 cross-validation: **N/A** — no C++ change; geometric-engine Q5 path, Python-only.
- Oracle `reference.py` untouched; no frozen okf file edited.
- Tests: `tests/test_task_r_cross_round.py` 4/4 (peeling logic).

## [Files Changed · Validation Status · New Decisions]
- **Files:** `scripts/analyze_task_r_cross_round.py` (reframed: primary verdict = metric is
  structurally blind to cross-round + retired z-test); regenerated
  `results/q5_task_r_cross_round_raw.json` + `results/processed/task_r_cross_round_analysis.json`
  (runner/analysis-owned); this report. (`scripts/run_task_r_cross_round.py`, `tests/…` already
  committed `e066fd8`, unchanged this session.)
- **Validation:** `/verify` gate PASS — reviewer conditional sign-off (Issue-1 framing fix
  applied: metric-blindness ≠ physical absence), critic PASS (structural proof empirically
  confirmed: 0 violations in 295,403 cross-round pairs, min dist/r_n = 1.0002; null confound
  confirmed: 83–87% of null nuclei cross-round), auditor [pending]. Counting fix verified
  (superset property restored, peeling to 24/component).
- **New decisions (draft for wrap-up):** D-0xx — the strict-r_n-clique cross-round metric is
  structurally blind to cross-round co-location and its real-vs-null z-test is retired as
  confounded; **C-Q5(i)'s cross-round question is untested by this operationalization and Task
  O's cross-round lower-bound caveat stays OPEN**; a supra-r_n cross-K (Option B) is the only
  valid test. Resolves `okf/next-actions.md` item 4 (supersedes the s-055 BLOCKED state) by
  determining the metric is the wrong tool, not by producing a cross-round finding.
