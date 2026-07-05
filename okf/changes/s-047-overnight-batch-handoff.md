---
type: Session Change
mutability: append-only
timestamp: 2026-07-04
tags: [handoff, overnight, q3, q4, q5, task-h]
---

# S-047: Overnight Batch Handoff (sandbox agent)

> Handoff document for the agent supervising the S-047 overnight compute batch. Written by the S-046 Claude Code session on Gary's instruction; the batch runs in a SANDBOX copy of this repo, so record results in your copy's OKF and reports — Gary reconciles afterward.

## Prompt for the incoming agent

You are resuming TwoCascade after session S-046 (read `okf/changes/s-046-q4-q5-analysis-and-track-decision.md` for what just landed, and `okf/lessons.md` before planning — constitution rule). Your job tonight is to run and supervise one unattended compute batch, then verify and record its outcomes. Do not start other work; do not touch `src/twocascade/reference.py`; never write into `results/` by hand.

1. **Launch** (from the repo root; this machine needs the arm64 interpreter — Rosetta python vs arm64 numpy, see lessons):
   `nohup arch -arm64 python3 scripts/run_overnight_s047.py > overnight_s047.log 2>&1 &`
   The driver is sequential, skips steps whose outputs exist, continues past failures, and ends with a per-step summary. Expected total: several hours; the long poles are the n=32000 duration cells and the n=10000 tilt grid.
2. **On completion, read the OVERNIGHT SUMMARY in `overnight_s047.log`.** For each failed step, capture the traceback in your session report; do not silently retry more than once.
3. **Verify outputs exist and are runner-stamped** (metadata carries git_commit, base_seed):
   - `results/q5_duration_raw.json` — C-Q5(ii) duration dichotomy n-sweep (n=4k..32k, global vs ell=r_n, mu=0 control).
   - `results/q4_ignition_{tau25,tau35}_n{4000,10000,20000}_raw.json` — C-Q4(iii) bounded-seed (a=r=2) ignition gates, 500 trials/cell. Expected shape: tau=2.5 ignition probability stays Theta(1) or grows with n; tau=3.5 must NOT ignite (decays with n). Read P(systemic) per cell with `twocascade.analysis.analyze_sweep`.
   - `results/raw/fear_concentration_n{1000,2000,4000,8000}.json` + `results/figures/clock_collapse_bias.png` — Task E history regen feeding Task H (scripts/run_task_h.py runs inside the driver).
   - `results/q4_phase2_n10000_gamma{neg1,0,pos1}_raw.json` + `results/q4_phase2_n10000_tau35_gamma0_raw.json` — Phase 2 tilt grid. To analyze the n=10000 tilt slices with `scripts/analyze_task_n.py`, point its PHASE1B_CONFIGS at the three `configs/q4_phase2_n10000_gamma*.json` files (same paired-seed design, base_seed=42); expect the gamma=-1 to 0 ordering to reproduce and the gamma=+1 cap caveat to persist (check cap_diagnostics realized_mu_bar first, lessons entry on the epsilon-cap).
   - `results/raw/finite_size_r2_n10000.json` — Q3 nu tightening input; analyze with the Task A machinery (`estimate_transition_width` / `fit_finite_size_exponent` in `src/twocascade/analysis.py`, cf. `scripts/plot_finite_size_scaling.py`).
4. **For C-Q5(ii)**, compute per (n, field, mu): mean T_theta over systemic trials, then the ballistic ratio T_theta / sqrt(n / log n). Prediction: ratio roughly constant for local_1 (ballistic), decreasing in n for global. Record the table; a figure is optional tonight.
5. **Record outcomes** in your copy's OKF per the `edit-okf` skill: overwrite `okf/status.md` / `okf/next-actions.md`, append your own s-NNN change entry + `okf/log.md` line, and write `docs/queue/reports/` entries for what completed. End your wrap-up with [Files Changed · Validation Status · New Decisions].
6. **Escalate, do not improvise:** if a step fails for a non-transient reason (bad config, engine error), report it with evidence and move on; the morning session triages. Anything touching `src/` or the oracle is out of scope tonight.

## What S-046 queued (rationale)

- **Q5 duration n-sweep** — completes the deferred C-Q5(ii) clause; with (i) and (iii) done it closes the C-Q5 readout for the July-15 advisor email.
- **Q4 ignition gates** — C-Q4(iii) is the tail-gating clause: tau=2.5 ignites at bounded seeds, tau=3.5 must not; the n-grid gives the decay direction.
- **Q4 Phase 2 at n=10000 + tau=3.5 tilt slice** — turns the S-046 one-n tilt result into a scaling statement and gates it by tail heaviness.
- **Task E regen + Task H** — the fear-concentration history raws died with the S-044 worktrees; regenerating them unblocks the deferred Q3 clock-bias analysis (numpy blocker root-caused in S-046: use arch -arm64).
- **Q3 nu at n=10000** — tightens Task A's wide confidence intervals via the C++ engine.

New artifacts backing the batch: 11 configs (`configs/q4_phase2_*`, `configs/q4_ignition_*`, `configs/finite_size_r2_n10000.json`), `scripts/run_task_o_duration.py`, `scripts/run_overnight_s047.py` (driver verified: step wiring, skip-if-exists, config parse — all checked in S-046).
