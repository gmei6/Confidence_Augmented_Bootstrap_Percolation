---
type: Session Change
title: "S-046: Q4 tilt analysis, Q5 locality sweep, Tracks 4/5 decision"
description: "Q4 tilt-monotonicity analysis, Q5 locality sweep, and the D-031 track decision."
mutability: append-only
timestamp: 2026-07-04
tags: [q4, q5, tilt-monotonicity, locality, decision]
---

# S-046: Q4 tilt analysis, Q5 locality sweep, Tracks 4/5 decision

Resumed from the S-045 handoff (Claude Code session, Gary authorized autonomous execution of next-actions items 1–3 equivalents). All changes are in the working tree, uncommitted, pending Gary's review.

## Task N (Q4) — C-Q4(i) tilt monotonicity
- Diagnosed the S-044 Phase 1 grid as entirely supercritical (Janson a_c seed multiples do not transfer to the tau=2.5 CM; transition sits at a in [2,32]).
- Ran gamma companions on the old grid (configs/q4_phase1_gamma0.json, _gamma_neg1.json) and a full Phase 1b small-seed sweep (configs/q4_phase1b_gamma{neg1,0,pos1}.json, 200 trials/cell, paired on base_seed=42).
- Verdict: cap-free pair gamma=-1->0 PASSES 7/7 mu rows; gamma=0->+1 untestable (epsilon-cap compresses realized mu-bar 6–28% — the scoping §7 early-warning, confirmed via sample_degree_dependent_fears stats). Artifacts: results/processed/task_n_tilt_analysis.json, results/figures/q4_tilt_monotonicity_r2.png, docs/queue/reports/task_n_report.md.
- Fixed tests/test_q4_prong_a.py (test called the oracle without required record_history — the test was wrong, case (a); 4/4 Q4 tests now pass incl. real C++ Prong A).

## Task O (Q5) — localized fear: nucleation law + coverage entropy
- geometry.py run_cascade_local_fear: additive round_log instrumentation, fear_adjacency=None global fast path, and an exact scatter-count optimization (~40x). Oracle untouched. New tests tests/test_q5_local_fear.py (5/5).
- Sweep: scripts/run_task_o.py (hard RGG, D=2 log n, n=4000, disc seed a=30, fields global / ell=r_n / ell=4r_n, mu in {0,0.2,0.4,0.6}, 40 trials/cell, base_seed=2026) -> results/q5_localized_fear_raw.json.
- Verdict: C-Q5(iii) homogenization SUPPORTED relative to the mu=0 control (global H at theta reaches 0.91; ell=r_n pinned to control, zero remote nuclei); C-Q5(i) NOT supported as pre-registered (slopes ~1.2–1.5 vs g_t, ~1.0–1.4 vs the windowed drive phi_t — constant leak), with the cross-round-ignition measurement caveat logged. C-Q5(ii) deferred to an n-sweep. Artifacts: results/processed/task_o_locality_analysis.json, results/figures/q5_locality_r2.png, docs/queue/reports/task_o_report.md.

## Decision
- d-031: Track 4 (SIR recovery, Q7) REJECTED (breaks monotonicity, invalidates the Janson baseline); Track 5 (weighted edges, Q8) DEFERRED indefinitely. open-questions Q7/Q8 updated.

## Environment
- Root-caused the S-044 'missing numpy' blocker: Rosetta x86_64 python vs arm64 numpy; use arch -arm64 python3. Task H is unblocked.

## OKF maintenance
- status.md, next-actions.md, open-questions.md overwritten; lessons.md gained 5 entries (Janson-grid transfer, epsilon-cap, nucleus-count kinematics, Rosetta/numpy, and the phi_t-vs-g_t fitting pitfall folded into the nucleus entry); decisions/index.md synced.
