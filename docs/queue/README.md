# Antigravity Task Queue

> **Purpose.** A queue of self-contained, low-human-input tasks for Antigravity to work
> through while Gary studies the existing work ahead of the **advisor meeting on
> 2026-07-01, 2:00pm**. Each task is scoped so the human review happens at the end:
> Antigravity runs the full `/research-cycle` (Plan → Execute → Verify → Wrap up), the
> `/verify` gate (`reviewer → critic → auditor`) runs automatically, and **Gary checks the
> result at the verify/wrap-up gate** rather than babysitting each step.

## Operating rules (do not skip)

- **Entry point:** run each task through `/research-cycle`. Honor every guardrail in
  `AGENTS.md` and `GEMINI.md` throughout.
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
| [E](task_E_fear_trajectory_concentration.md) | Fear-field trajectory concentration | §4.1 conj, §4.3 | yes (`analysis.py`) | low |
| [F](task_F_counting_process_law_binomial_test.md) | Counting-process $S(t)$ law & binomial test | §4.3 rows 9 & 11 | yes (`analysis.py`) | low |
| [G](task_G_scaling_law_extended_validation.md) | Scaling-law extended validation | §4.4 conj | small | low |
| [H](task_H_geometric_clock_collapse_bias.md) | Geometric clock-collapse bias | §4.1 note | small | low |
| [I](task_I_okf_migration.md) | OKF knowledge-bundle migration (PROJECT_TRACKER/LESSONS_LEARNED → `okf/`) | `docs/PROJECT_TRACKER.md`, `docs/LESSONS_LEARNED.md`, `AGENTS.md`, `CLAUDE.md` (pointer), new `okf/` tree, new `.agents/skills/{edit-okf,session-start,session-wrapup}/` | none | low |
| [J](task_J_config_model_fear_scoping.md) | Scoping doc: degree-dependent fear on a configuration-model graph (Q4) | new `docs/research/q4_config_model_scoping.md` | none | low |
| [K](task_K_geometric_graph_scoping.md) | Scoping doc: panic-field locality on geometric graphs (Q5) | new `docs/research/q5_geometric_graph_scoping.md` | none | low |
| [L](task_L_q1_decoupling_followup.md) | Q1 follow-up: path forward for the Asymptotic Decoupling Conjecture | new `docs/research/q1_decoupling_path_forward.md` | none | low |
| [M](task_M_q7_recovery_phase_scoping.md) | Scoping doc: optional recovery/healing phase (Q7) | new `docs/research/q7_recovery_phase_scoping.md` | none | low |

**Suggested order for new tasks:** E → F → H → G → I → J → K → L → M.
Each task is independent; do them in any order, one full `/research-cycle` each.
