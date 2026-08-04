---
type: Session Change
title: "S-064: Poster content-complete; single-seed result; famcompare rebase; C++ GIRG port gated and merged; QR demo live"
description: "2026-08-04 all-day sprint before the (rescheduled) 3pm advisor meeting: Fear Amplifies rebuilt on the famcompare fear-curves figure; mu-bar 0.5/0.6 arms run; famcompare CM rebased onto the matched ensemble (geometry-damping claim retracted as an ensemble artifact); single-seed ignition experiment confirms fear bridges the a=r floor; the C++ GIRG port cleared the full blind gate (AUDIT PASS) and merged; the QR demo site was designed, built, and deployed."
mutability: append-only
timestamp: 2026-08-04
tags: [poster, famcompare, single-seed, girg-cpp, qr-demo, audit-pass, stopping-point]
---

# S-064: poster complete, port merged, demo live (2026-08-04)

Session ran from morning to ~2:50pm, wrapped for the rescheduled 3:00pm advisor
meeting (moved from 2026-08-03). Orchestrated via background subagents throughout.

## Poster (commits 50d4094, b3fd325, 9b69e2e, 2f5404c, 7c33108, d795035, bc54da0, 1af8cc1, 89856a4)
- **Fear Amplifies rebuilt end-to-end.** Famcompare analysis re-run on the full
  {4k,10k,20k} grid once the GIRG n=20000 arm landed; four figure designs rendered
  and reviewed; Gary chose the single-axes "fear curves" form and iterated it
  (hero palette, n=10000 only, no CI graphics, no immunity band, open-marker
  censoring convention kept). Panel text distilled to "Fear is an amplifier with
  a dial" + two sentences; full prose moved to PRESENTER NOTES tex comments;
  viewer-facing notes added to the poster-demo page.
- **mu-bar 0.5/0.6 arms** run for ER and power-law (CM) at n=10000 (piloted
  grids, crossings ER 78/52, CM 6.0/5.1, monotone, no clamping) -> Fear and
  Structure now 7 points per non-geometric family; figure inverted (0% top,
  -100% bottom, D-042-adjacent reframe per Gary), ER-only theory line removed,
  typography matched to the famcompare sibling, near-floor rings removed (d-043).
- **Famcompare extended to 0.7 and CM REBASED (d-042):** the old CM curve was
  sourced from q4 raws at mean degree 4.0 while ER/GIRG were matched at 4.533 —
  a 13% edge-probability difference. On matched data the new CM row is
  1.26/1.58/2.21/3.05/4.26/5.26/6.63 (baseline p=0.038, none censored), GIRG
  reaches a measured 8.3x at 0.7, ER stays a censored >=26x floor, and the
  bounded arm is 0/500 through 0.7. GIRG and power-law INTERLEAVE — the
  "geometry appears to damp fear" poster sentence was cut (Gary's Option A).
- **Main column redesigned by Gary:** full-bleed hero, legend + Sec 5.4 engine
  disclosure side-by-side beneath it; Comparisons bullets shortened; "Where To
  Intervene" retitled "How To Intervene" with the body as talking-point comments
  (d-041). Zip gate 15/15 at every rebuild; final sync ~/Downloads 13:43.

## Single-seed ignition experiment (1af8cc1)
36 configs (4n x 9<k> x 8 mu-bar, 500 trials/cell, cpp engine), 144,000 trials:
single-seed (a=1) ignition occurs at every mu-bar>0 at rate ~= 1-exp(-mu-bar)
(0.501 measured vs 0.503 predicted at 0.7), ~independent of <k> and n; the mu=0
control halts at |A*|=1 in all 18,000 trials. Fear bridges the a=r floor (d-043);
P(systemic) separates cleanly from ignition (falls with n at fixed <k>).

## C++ GIRG port: gate complete, MERGED (a2b2596)
G6 ran as 4 blind reviewer rounds + fix rounds G5.1 (2bd9666, 10 items),
G5.2 (7b31698, 9 items + a NEGATIVE RESULT: the BKL level-set tolerance has no
discrimination power — re-scoped honestly), G5.3 (f013cd8, production-n parity
to L=7, generator-law checks, one reviewer premise refuted with a runtime
falsification check), G5.4 (1dcb968, unvalidated-regime warning + advisories).
Critic: NO MATERIAL BREAKAGE (exhaustive instrumented partition probe — every
pair owned exactly once, 60M+ bound checks, all mutations caught; own Prong A
6/6 exact incl. windowed/non-uniform mu=0; Prong B 3/3; L=8 band probed at
n=65537 and held; 4 near-misses recorded, N1/N2 pre-existing at merge-base).
Auditor: **AUDIT PASS** — independently reproduced the exact-probability parity,
the benchmark (52x at n=10000), and the mutation z-scores; no weakened tests, no
seed-shopping, no fabrication. Gary approved the diff; merged from the main repo.
Post-merge: stale main-repo cmake cache (from the old CABP_copy_for_antigravity
path) set aside as cpp/build.stale-cache-20260804; fresh build ctest 2/2.
**Open:** full cross-language pytest re-run in the main repo (interrupted);
the merge commit is NOT yet pushed (origin is at 8a40677).

## QR demo: designed, built, LIVE (8a40677, pushed; Pages deploy green)
Plan iterated with Gary via a Lavish session (his calls: n=300, fixed pace,
phase-6 stacked, palette + colour-blind shapes toggle, phase-7 trial chooser;
self-paced first, presenter-sync deferred). Built on precomputed reference-engine
traces (committed configs + scripts/dump_poster_demo_traces.py; per-failure
cause derived post-hoc, self-checked: mu=0 traces classify 100% structural).
Three review iterations (progress bar, three-tier edge rendering, degree-scaled
nodes). All assets verified 200 at
https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/poster-demo/.
Honest scale finding recorded on-page: at n=300 the ER bounded seed is only
~4.6x below a_c (vs ~122x at n=10000), so 1% of mu-bar=0.4 demo-scale trials
ignite — the phase-2 explainer states both numbers.

## Process notes
- Famcompare provenance/evidentiary status: analysis + figures remain
  script-level self-checked, NOT blind-gated (same tier as C3b; item 3b's
  pre-print /verify still recommended, now covering the famcompare and
  percentage-decrease steps too).
- Known seed collision documented in analyze_famcompare.py (ext mu=0.5 cell
  shares the SeedSequence child of the mu=0 baseline cell at base_seed=42).
- Two sweep-agent stall incidents (idle-wait on monitors that never fire) were
  recovered by orchestrator nudge/direct takeover; no data loss.

## [Files Changed - Validation Status - New Decisions]
- **Files:** 12 commits on antigravity (50d4094..a2b2596) + 8088092 on
  separate-legend (merged); pushed through 8a40677.
- **Validation:** zip gate 15/15 (last 13:43); single-seed + mu 0.5/0.6 raws
  runner-stamped and verified; GIRG port AUDIT PASS; demo harness green + live
  assets 200. Famcompare analysis tier: self-checked (see process notes).
- **New Decisions:** d-040..d-045 (this session's formalizations).
