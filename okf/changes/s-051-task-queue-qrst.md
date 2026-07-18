---
type: Session Change
title: "S-051: Tasks Q/R/S/T queued; S/T launched autonomously"
description: "Four new docs/queue/ tasks scoped for the 2026-07-22 advisor meeting; the two config-only ones (S, T) launched in the background, the two requiring code changes (Q, R) left for review."
mutability: append-only
timestamp: 2026-07-17
tags: [queue, Q3, Q4, Q5, autonomous-execution]
---

# S-051: Tasks Q/R/S/T queued; S/T launched autonomously

Gary asked for the outstanding experiments to be written up and set running while away from
the keyboard. Four new task files added to `docs/queue/` (letters continue the existing A–P
sequence):

- **Task Q** — `docs/queue/task_Q_epsilon_cap_sampler_fix.md`. Make
  `sample_degree_dependent_fears` (`src/twocascade/graphs.py`) cap-aware so the γ=0→+1 tilt
  pair (C-Q4(i)/(ii)) is finally testable — every reversal to date is cap-affected (7–28%
  shortfall). **Not started, not autonomous-safe**: this is a `src/` change and needs the full
  `/research-cycle` review gate (baseline isolation, reviewer/critic/auditor) before any diff
  lands — flagged, not applied unattended, per `AGENTS.md` §III.
- **Task R** — `docs/queue/task_R_cross_round_remote_ignition.md`. A cross-round nucleus
  tracker to address the known lower-bound caveat on C-Q5(i)'s "honest negative" nucleation-law
  reading. **Not started**: needs new script logic drafted (a real methodology decision, not a
  parameter sweep) before it can run, even though it likely doesn't touch `src/twocascade/`
  itself.
- **Task S** — `docs/queue/task_S_q4_ignition_wider_n_grid.md`. Extends the C-Q4(iii) bounded-seed
  ignition-gate n-grid to n∈{40000, 80000} (new configs `configs/q4_ignition_tau25_n{40000,80000}.json`,
  seed_multiples recomputed via `janson_a_c` so the bounded seed stays a=2) to resolve whether
  the μ̄=0.4 branch's decline (0.134→0.116→0.062) is slow decay or a genuine limit. **Config-only,
  no `src/` changes — launched immediately.**
- **Task T** — `docs/queue/task_T_q3_nu_extended_n.md`. Extends the Q3 finite-size ν fit to
  n=20000 (new config `configs/finite_size_r2_n20000.json`, same schema/seed as the n=10000
  config, C++ engine). **Config-only — launched immediately.**

`scripts/run_overnight_s051.py` (modeled on `scripts/run_overnight_s047.py`) runs Tasks S and T
sequentially in the background: `nohup arch -arm64 python3 scripts/run_overnight_s051.py >
overnight_s051.log 2>&1 &`. Tasks Q and R are deliberately excluded from that driver.

`docs/queue/README.md`'s task table updated with all four; its stale E/F/G/H rows (pointing at
task files removed after S-048 completion) were flagged but left as-is — out of scope for this
session. `okf/next-actions.md` rewritten to point at the queue instead of restating Q4/Q5
follow-ups inline, and to correct the advisor-meeting date (2026-07-15 → 2026-07-22, per Gary's
2026-07-17 clarification) wherever it appeared stale.
