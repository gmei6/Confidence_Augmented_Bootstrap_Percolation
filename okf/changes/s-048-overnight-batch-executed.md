---
type: Session Change
title: "S-048: S-047 Overnight Batch Executed — 5/5 OK (sandbox copy)"
description: "S-047 overnight batch executed in the sandbox: 5/5 steps OK; C-Q5 readout complete."
mutability: append-only
timestamp: 2026-07-05
tags: [overnight, q3, q4, q5, task-h, sandbox]
---

# S-048: S-047 Overnight Batch Executed — 5/5 OK (sandbox copy)

Autonomous sandbox session executing the S-047 handoff (`okf/changes/s-047-overnight-batch-handoff.md`), branch `fm/s047-batch-x7` in a disposable worktree of the sandbox copy. Gary reconciles into the primary checkout.

## Batch execution

- Verified `arch -arm64 python3` (numpy 2.4.4), launched `scripts/run_overnight_s047.py` via nohup (PID 70731). **OVERNIGHT SUMMARY: 5/5 steps OK, ~13 min total** (`overnight_s047.log`; the handoff's multi-hour estimate was far exceeded by this machine). No failures, no retries needed.
- **Pre-empted the one guaranteed failure:** this copy had no `cpp/build/twocascade_run`; built it before step 5 needed it (Release, `-DCMAKE_OSX_ARCHITECTURES=arm64` per lessons; `test_engine` passes). Build only — no `cpp/src` or `src/` changes anywhere this session.
- All outputs verified runner-stamped (git_commit `fb0ac42`, base_seeds 2027 / 42 / 202607041-4).

## Results (details in the five reports under docs/queue/reports/)

- **C-Q5(ii) SUPPORTED** — ballistic ratio flat vs the mu=0 control for ell=r_n, decaying for global (t~-46); C-Q5 fully read out. (`task_o_duration_report.md`; verdict criterion = slope vs the control slope, since the control carries the finite-size drift of the ballistic constant.)
- **C-Q4(iii) gate HOLDS** — tau=3.5: 0/3000 ignitions at a=r=2; tau=2.5 ignites everywhere. Flag: the mu=0.4 branch decreases in n; Theta(1) only clean at mu=0. (`q4_ignition_report.md`)
- **C-Q4(i) scales** — gamma=-1->0 passes 7/7 cap-free rows at n=10000 (as at n=4000); gamma=+1 still cap-affected everywhere (7-28% shortfall); tau=3.5 tilt slice is a total gate (0/16000 over the whole seed grid). (`task_n_phase2_report.md`)
- **Task H unblocked + confirmed** — clock bias collapses onto a/n, <=1.2e-5 for a/n<=0.01; Task E histories regenerated in-batch. (`task_h_report.md`)
- **Q3 nu tightened** — nu(mu=0)=8.65+/-1.04, nu(mu=0.3)=4.54+/-0.26 with the n=10000 C++ point; the n in {1k,2k,5k} raws (lost with the S-044 worktrees) were regenerated from committed configs, exercising the section 5.6 regenerability invariant. (`q3_nu_n10000_report.md`)

## Defect found (not fixed - src/ frozen overnight)

`plot_fear_field_concentration` (`src/twocascade/plotting.py`) lacks its `savefig`/`close` tail: Task E prints "Done!" but the relvar figure is never written. Lesson recorded; morning fix is one line but touches `src/`.

## New artifacts

Scripts: `analyze_task_o_duration.py`, `analyze_q4_ignition.py`, `analyze_task_n_phase2.py`, `analyze_q3_nu.py`, `plot_task_n_phase2.py` (the two Phase-2 wrappers repoint the Task N machinery without overwriting the S-046 artifacts). Processed: `task_o_duration_analysis.json`, `q4_ignition_analysis.json`, `task_n_phase2_n10000_analysis.json`, `task_a_nu_n10000.json`. Figures: `clock_collapse_bias.png`, `q4_tilt_monotonicity_r2_n10000.png`, `finite_size_scaling_r2_n10000.png`. Raws: 11 batch outputs + 3 regenerated finite-size raws. Reports: 5 new under `docs/queue/reports/`.

## Wrap-up contract

[Files Changed: overnight_s047.log; 14 results raws (batch + finite-size regen); 4 processed analyses; 3 figures; 5 scripts; 5 reports; okf/{status,next-actions,lessons}.md overwritten/extended; this entry + log.md line + changes/index.md sync · Validation Status: batch 5/5 OK; all raws runner-stamped; C++ test_engine passes; verdicts — C-Q5(ii) supported, C-Q4(iii) gate holds (mu=0.4 n-direction flagged), C-Q4(i) reproduced at n=10000 (cap caveat persists), Task H confirmed, nu tightened; no src/, oracle, or hand-written results/ edits · New Decisions: none — no d-NNN entries; two triage flags recorded in next-actions]
