# Antigravity Task Queue

> **Purpose.** A queue of self-contained, low-human-input tasks for Antigravity to work
> through while Gary studies the existing work between advisor meetings (the queue predates
> the 2026-07-01 meeting; the current one is **2026-07-22**). Each task is scoped so the
> human review happens at the end:
> Antigravity runs the full `/research-cycle` (Plan → Execute → Verify → Wrap up), the
> `/verify` gate (`reviewer → critic → auditor`) runs automatically, and **Gary checks the
> result at the verify/wrap-up gate** rather than babysitting each step.

## Operating rules (do not skip)

- **Entry point:** run each task through `/research-cycle`. Honor every guardrail in
  `AGENTS.md` throughout (Antigravity reads it natively; `CLAUDE.md` is a symlink to it).
- **Propose, don't write.** Present every diff in chat and get approval before any
  `write_to_file` / `replace_file_content` touches disk.
- **Baseline isolation.** Any change to `src/` or `cpp/src/` is done in **New Worktree
  Mode**. Config-only / docs-only tasks may use Local Mode.
- **Oracle & frozen protection.** Never modify `src/twocascade/reference.py`, any 🔒 frozen
  tracker section, or anything in `results/` by hand. The runner owns all `results/` output.
- **Tracker edits are the PI's job.** Antigravity *drafts* §8–§10 / §11–§12 updates via
  `/wrapup`; only the orchestrator (Gary) applies them via the §14 protocol.
- **Stay in the decided model.** All four tasks run on $G(n,p)$ with the incremental fear
  field, Beta fear, and the absolute-$r$ rule. **None** of them opens the advisor-gated
  forks (Q2 configuration model, Q3 critical-window *framing*). If a task seems to require
  that, STOP and surface it.

## Reusable facts (so you don't re-derive them)

- **Run a sweep:** `twocascade.runner.run_sweep(config_path, engine=...)`. It writes raw
  per-trial outcomes (stamped with config + seed + git hash + timestamp) to the path in
  `config["output"]["raw_filepath"]`.
- **Config schema** (see `configs/sweep_wk3_4_r2.json`): `engine`, `pinned_params`
  {`n, r, concentration, theta, window_len, weights, target_high_degree`},
  `scaling` {`n_ref, target_mean_degree, alpha`}, `sweep`
  {`mean_fear_grid, seed_multiples, trials_per_cell, base_seed`}, `output.raw_filepath`.
- **Janson regime (§4):** `alpha` must satisfy `1/r < alpha < 1` (runner enforces). `BETA`
  is frozen at `n_ref`, so `p_n = BETA·n^{-alpha}` and `np` grows with `n` — to vary `n`
  cleanly, **keep `n_ref` fixed across configs and change only `pinned_params.n`.**
- **Seed sizes** are `max(r, round(seed_multiple · a_c0))` with
  `a_c0 = model.janson_a_c(n, p, r)` recomputed per `n` — i.e. multiples are relative to the
  per-`n` critical seed (exactly §4's prescription).
- **Raw output per cell** stores `failed_fractions[]` and `rounds_completed[]` — so $\theta$
  re-thresholding and cascade-duration analysis need **no re-runs**.
- **C++ engine limitation:** it raises on `target_high_degree=True`. Targeted-seeding runs
  must use `engine="python"` (keep `n` and trial counts modest).
- **Where code lives:** analysis fns in `src/twocascade/analysis.py`; figures in
  `src/twocascade/plotting.py` (read-only on raw + analysis artifacts); sweep orchestration
  pattern in `scripts/plot_wk3_4.py`; analysis tests in `tests/test_analysis.py`.

## Tasks

| ID | Title | Touches | New `src/`? | Risk |
|----|-------|---------|-------------|------|
| [A](old-tasks/task_A_finite_size_nu.md) | Finite-size transition-width exponent ν | §6 Wk 6–7; informs Q3 | yes (`analysis.py`, `plotting.py`) | med |
| [C](old-tasks/task_C_targeted_seeding.md) | Random vs. targeted seeding (negative result) | §3.1, Wk 9 | none likely | low |
| [D](old-tasks/task_D_window_invariance.md) | Memory-window $X$-invariance (D-006) | §3.6, Wk 9 | small | low |
| [E](old-tasks/task_E_fear_trajectory_concentration.md) | Fear-field trajectory concentration | §4.1 conj, §4.3 | yes (`analysis.py`) | low |
| [F](old-tasks/task_F_counting_process_law_binomial_test.md) | Counting-process $S(t)$ law & binomial test | §4.3 rows 9 & 11 | yes (`analysis.py`) | low |
| [G](old-tasks/task_G_scaling_law_extended_validation.md) | Scaling-law extended validation | §4.4 conj | small | low |
| [H](old-tasks/task_H_geometric_clock_collapse_bias.md) | Geometric clock-collapse bias | §4.1 note | small | low |
| [I](old-tasks/task_I_okf_migration.md) | OKF knowledge-bundle migration (PROJECT_TRACKER/LESSONS_LEARNED → `okf/`) | `docs/PROJECT_TRACKER.md`, `docs/LESSONS_LEARNED.md`, `AGENTS.md`, `CLAUDE.md` (pointer), new `okf/` tree, new `.agents/skills/{edit-okf,session-start,session-wrapup}/` | none | low |
| [J](old-tasks/task_J_config_model_fear_scoping.md) | Scoping doc: degree-dependent fear on a configuration-model graph (Q4) | new `docs/research/q4_config_model_scoping.md` | none | low |
| [K](old-tasks/task_K_geometric_graph_scoping.md) | Scoping doc: panic-field locality on geometric graphs (Q5) | new `docs/research/q5_geometric_graph_scoping.md` | none | low |
| [L](old-tasks/task_L_q1_decoupling_followup.md) | Q1 follow-up: path forward for the Asymptotic Decoupling Conjecture | new `docs/research/q1_decoupling_path_forward.md` | none | low |
| [M](old-tasks/task_M_q7_recovery_phase_scoping.md) | Scoping doc: optional recovery/healing phase (Q7) | new `docs/research/q7_recovery_phase_scoping.md` | none | low |
| [Q](old-tasks/task_Q_epsilon_cap_sampler_fix.md) | ε-cap sampler fix (Q4 Phase 2 unblock) | `graphs.py` | **yes** — needs review before running | med |
| [R](old-tasks/task_R_cross_round_remote_ignition.md) | Cross-round remote-ignition tracker (Q5 nucleation-law caveat) | new `scripts/run_task_r_cross_round.py` | probably none (script-only) but undrafted | low-med |
| [S](old-tasks/task_S_q4_ignition_wider_n_grid.md) | Q4(iii) ignition gate: wider n-grid at μ̄=0.4 | new configs only | none | low |
| [T](old-tasks/task_T_q3_nu_extended_n.md) | Q3 ν: extend finite-size fit to n=20000 | new config only | none | low |
| [U](old-tasks/task_U_q5_duration_asymptotic_form.md) | Q5 C-Q5(ii) refinement: asymptotic form of global-field sub-ballistic decay | new scripts (copies of Task O) | none | low-med |
| [V](old-tasks/task_V_q4_ignition_mu_map.md) | Q4 ignition: intermediate-μ̄ map (0.1/0.2/0.3) across the 5-point n-grid | new configs + 1 read-only analysis script | none | low |
| [W](old-tasks/task_W_finite_size_crossover.md) | Shared finite-size crossover: push Q3-ν and Q4-ignition series past n=20000 | new configs + 1-line edits to 2 analysis scripts | none | low |
| [X](old-tasks/task_X_size_biased_collapse_retest.md) | C-Q4(i)/(ii) cap-free re-test after the Q sampler fix | new analysis only | none | low |
| [Y](task_Y_fear_multiplier_mechanism.md) | **OPEN** — does the fear multiplier come from the $g_t$ normalization? | new configs only | none | low |

**Suggested order for new tasks:** E → F → H → G → I → J → K → L → M.
Each task is independent; do them in any order, one full `/research-cycle` each.

## Status (updated 2026-07-21, S-058)

**Tasks A–X are all CLOSED. The only open task is Y.** Every A–X task file now lives in
`old-tasks/`; the table links above point there. Reports are in `reports/`.

⚠️ **Closure records for Q–X live in commit bodies and `okf/changes/`, not in
`reports/`.** A missing report file does **not** mean a task is open — this misread cost a
session. Closure evidence, audited 2026-07-21:

| Task | Closure |
|---|---|
| Q | AUDIT PASS, merged `c4ef634` (S-054) |
| R | AUDIT PASS, `aea2ac4` (S-057); retired the strict-clique metric under D-035 |
| S, T | Closed **by supersession** under **D-036** — no gate of their own, by explicit decision. Their values are retired as known-wrong; do not cite them |
| U, V, W | `/verify` cleared in `d70dbd8` (reviewer sign-off, critic PASS, AUDIT PASS) |
| X | AUDIT PASS, `a08033c` (S-056) |

**Corrections to what this file previously said**, all wrong as of 2026-07-21:
- ~~"Q and R are NOT started"~~ — both are **done with AUDIT PASS**. This line survived four
  sessions after the fact.
- ~~E/F/G/H task files "removed"~~ — they were **archived to `old-tasks/`** (`c23364b`), never
  deleted. Links above now corrected.
- ~~U/V/W share the "n≈20000 flattening" theme~~ — **Task W refuted that crossover.** Three
  independent series all fail to flatten; the framing is retired, not pending.
- ~~`okf/open-questions.md` Q5 "C-Q5(ii) … deferred" is stale~~ — that line has **since been
  fixed**; it now reads "C-Q5(ii) duration dichotomy SUPPORTED". The note was itself stale.

**Known-thin evidence, flagged not resolved:** Task U's closure traces to a single source —
the `d70dbd8` commit body. There is no `okf/changes/` file, no `okf/log.md` entry, and no
report for it. Judged sufficient (the commit body names the gate specifically) but it is one
source, not several. Separately, U's and W's task files asked for a **human** at the verify
gate and got a blind one — a process gap recorded in D-036, not an ungated result.
