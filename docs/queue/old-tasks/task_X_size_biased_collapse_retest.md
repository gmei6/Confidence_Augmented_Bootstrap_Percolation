# Task X — C-Q4(ii) size-biased collapse re-test + γ=0→+1 tilt leg (post-Q sampler fix)

**Queued:** 2026-07-18 (scoped after Task Q merged). **Conjectures under test:** C-Q4(i)
tilt monotonicity (the γ=0→+1 leg) and C-Q4(ii) size-biased collapse. This is the re-test
that converts Task Q's ε-cap sampler fix into an actual Q4 readout.

> **Why now.** Task Q (S-054, merged `c4ef634`) replaced the single-pass `Z_n` normalization in
> `sample_degree_dependent_fears` with iterative water-filling, so `realized_mu_bar` now tracks
> `mu_bar` even under a positive tilt on a heavy tail. Every prior γ=0→+1 result was cap-affected
> (7–28% realized-μ̄ shortfall, `docs/queue/reports/task_n_phase2_report.md`) and artifact-suspect.
> This task re-runs those experiments on the fixed sampler.

> **Corrected validation invariant (from `okf/next-actions.md` item 5).** The fix does NOT drive
> `cap_hits`→0 for genuinely heavy-tailed cells — that was the original task file's imprecise
> framing. The verified invariant is **`realized_mu_bar` tracking `mu_bar` within tolerance even
> when `cap_hits` stays substantial** (confirmed up to ~30% of nodes at μ̄=0.7, γ=+1, n=10000).
> Check `realized_mu_bar`, NOT `cap_hits`, when validating the re-run.

## Autonomous-safe: script/config-only, but /verify-gated

No `src/` or `cpp/src/` changes (the sampler fix already landed via Task Q). New configs + a new
read-only analysis script → Local Mode. Gate at `/verify` before "done". Uses `engine="python"`
(configuration-model + degree-fear path is Python-only).

## Method

### Step 1 — Re-run the tilt slices on the fixed sampler

Re-run the paired-seed γ slices with the merged sampler. To PRESERVE the old cap-affected raws
for a before/after comparison, write to NEW output paths (`..._capfix_raw.json`) rather than
overwriting `results/q4_phase2_n10000_gamma*_raw.json`.

- Create `configs/q4_phase2_n10000_gamma0_capfix.json`, `..._gammapos1_capfix.json`, and
  `..._gammaneg1_capfix.json` — byte-for-byte copies of the existing
  `configs/q4_phase2_n10000_gamma{0,pos1,neg1}.json` with only `output.raw_filepath` changed to
  `results/q4_phase2_n10000_gamma{0,pos1,neg1}_capfix_raw.json`. (Same grid, `base_seed=42`
  paired design — the γ=0 slice is a control that should be ~unchanged, since the γ=0 sampler
  path is mathematically unaffected by the water-filling fix; a large γ=0 change would signal a
  wiring error.)
- Run all three via `run_sweep`.

### Step 2 — C-Q4(i) tilt monotonicity, cap-free

Repoint `scripts/analyze_task_n_phase2.py`'s `PHASE1B_CONFIGS` at the three `_capfix` configs and
its `OUTPUT_PATH` at a new `results/processed/task_x_tilt_capfix_analysis.json` (do NOT overwrite
the existing Phase-2 artifact). Re-run. Expected: the `cap_free` flags for the γ>0 cells that were
previously artifact-suspect now flip to True (the `cap_diagnostics` call re-samples with the fixed
sampler, so `realized_mu_bar` tracks `mu_bar` → `gamma_is_cap_free` passes), and the γ=0→+1
paired P(systemic) comparison becomes a VALID test of tilt monotonicity rather than a cap artifact.
Report the verdict on the now-cap-free γ=0→+1 leg.

### Step 3 — C-Q4(ii) size-biased collapse (new analysis)

C-Q4(ii): cells with matched size-biased mean fear μ*(γ) should collapse onto the same
P(systemic) boundary regardless of γ (μ* is the governing quantity, `docs/queue/reports/task_j_report.md`).
The realized μ* per cell is `stats["realized_mu_star"]` from the sampler; the sweep raws carry
P(systemic) per (μ̄, seed). Build a new read-only script `scripts/analyze_q4_size_biased_collapse.py`:

- For each γ slice's `_capfix` raw, compute P(systemic) per (μ̄, seed_multiple) via `analyze_sweep`.
- Attach the realized μ* for each (μ̄, γ) cell (recompute deterministically via
  `cap_diagnostics`-style `sample_degree_dependent_fears` on a fixed degree sequence, matching the
  `analyze_task_n.py` convention — same `diag_seed_graph`/`diag_seed_fear`).
- Test collapse: re-express each γ slice's ignition curve against μ* instead of μ̄, and check
  whether the γ=0, +1 (and −1) curves collapse onto a common boundary within MC error. Report a
  quantitative collapse metric (e.g. spread of a_c^emp at matched μ*), not just a plot.

### Step 4 — Validate the fix end-to-end

Confirm, from the `_capfix` sweep metadata / cap diagnostics, that `realized_mu_bar` tracks `mu_bar`
within `CAP_TOL` for the γ=+1 cells that previously showed 7–28% shortfall — **checking
`realized_mu_bar`, not `cap_hits`** (see the corrected invariant above).

## Expected output

- `results/q4_phase2_n10000_gamma{0,pos1,neg1}_capfix_raw.json` (runner-stamped).
- `results/processed/task_x_tilt_capfix_analysis.json` (C-Q4(i) cap-free re-analysis).
- `results/processed/q4_size_biased_collapse_analysis.json` (C-Q4(ii) collapse metric).
- A wrap-up readout: (a) does the γ=0→+1 leg now support tilt monotonicity cap-free? (b) does
  C-Q4(ii) collapse hold at matched μ*? (c) confirmation that realized_mu_bar tracks mu_bar.

## Reports / context

`docs/queue/task_Q_epsilon_cap_sampler_fix.md` ("Scope after the fix lands"),
`okf/changes/s-054-task-q-epsilon-cap-fix-verified.md`, `docs/queue/reports/task_n_phase2_report.md`
(the cap-affected baseline), `scripts/analyze_task_n.py` + `analyze_task_n_phase2.py` (the C-Q4(i)
machinery), `docs/queue/reports/task_j_report.md` (C-Q4 three-clause definition, μ* as governing
quantity), `okf/open-questions.md` Q4, `okf/next-actions.md` item 5.
