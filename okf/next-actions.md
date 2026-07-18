---
type: Concept
title: "§10 — Next Actions"
description: "Live list of the next few concrete steps; overwritten each session."
mutability: live
---

# §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

1. **Task queue analysis (S-052, 2026-07-18, IN PROGRESS — subagent dispatched):** Task S/T raw
   data landed (S-051) but `scripts/analyze_q4_ignition.py` (`N_GRID`) and
   `scripts/analyze_q3_nu.py` (`N_LIST`) still have the old n-grids hardcoded — a subagent is
   updating both and rerunning them to get the actual updated numbers/figures, and separately
   drafting (not applying) the one-line `savefig`/`close` fix for
   `plot_fear_field_concentration` in `src/twocascade/plotting.py` for review. Q and R remain
   **not started** and out of this subagent's scope — Q needs a reviewed `src/twocascade/graphs.py`
   fix (`docs/queue/task_Q_epsilon_cap_sampler_fix.md`); R needs new script logic drafted first
   (`docs/queue/task_R_cross_round_remote_ignition.md`).
2. **Email Prof. Dhara before 2026-07-22** — the C-Q5 readout is COMPLETE for the email: (i)
   honest negative, (ii) duration dichotomy SUPPORTED (S-048 n-sweep, `task_o_duration_report.md`),
   (iii) homogenization supported. Also in hand: Q6 super-hub negative, Q4 tilt monotonicity at
   two system sizes + the τ=3.5 total gate, tightened ν (μ=0.3: 4.54±0.26), and now (pending
   item 1's analysis) an even wider n-grid on both. The `advisor-update-2026-07-22/` site
   covers all of this.
3. **RESOLVED, stale item removed (2026-07-18):** this used to say "review and commit the
   S-046/S-047 primary-checkout working tree" — verified against `git log` that this was already
   committed (`fb0ac42`, ancestor of current HEAD) before this session even started. Nothing
   left to commit; no PR needed. The item was simply never cleared after the commit landed.
4. **Machine-setup npm installs (IN PROGRESS — subagent dispatched, 2026-07-18):** a subagent is
   researching and proposing whether/why `gh-axi`, `tasks-axi`, `chrome-devtools-axi` are worth
   installing (Gary asked for the rationale before running any global `npm install -g`, not for
   them to be installed yet). Environment note: run simulations with `arch -arm64 python3`
   (Rosetta/numpy mismatch).

**Cleared 2026-07-18 (Gary's call):** the "Study the Math" deep-dive and its gating prerequisite
reading queue, and the `graphs.py` configuration-model vectorization perf item — Gary will pick
up the modeling intuition via the `advisor-update-2026-07-22/` site instead. If the perf item
matters again later, it's still recorded in `EXPLAINER.md` §12 and `graphs.py:30-45`.
