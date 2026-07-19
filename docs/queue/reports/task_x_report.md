# Task X — C-Q4(ii) size-biased collapse re-test + γ=0→+1 tilt leg (post-Q sampler fix)

**Session:** S-056 (2026-07-18, autonomous continuation). **Conjectures under test:**
C-Q4(i) tilt monotonicity (specifically the γ=0→+1 leg) and C-Q4(ii) size-biased
collapse. **Mode:** Local (script/config only; no `src/` or `cpp/src/` change — the
sampler fix landed via Task Q, merged `c4ef634`). **Engine:** `python` (configuration-model
+ degree-dependent fear path is Python-only). This is the re-test that converts Task Q's
ε-cap sampler fix into an actual Q4 readout.

## What changed since the cap-affected baseline

Task Q (S-054, merged `c4ef634`) replaced the single-pass `Z_n` normalization in
`sample_degree_dependent_fears` with iterative water-filling, so `realized_mu_bar` now
tracks `mu_bar` even under a positive tilt on a heavy tail. Every prior γ=0→+1 result was
cap-affected (7–28% realized-μ̄ shortfall, `docs/queue/reports/task_n_phase2_report.md`)
and artifact-suspect.

## Artifacts produced

| Artifact | Role | Provenance |
|---|---|---|
| `configs/q4_phase2_n10000_gamma{0,pos1,neg1}_capfix.json` | new configs (byte-copies of the `gamma{0,pos1,neg1}` configs with only `output.raw_filepath` changed) | new |
| `results/q4_phase2_n10000_gamma{0,pos1,neg1}_capfix_raw.json` | runner-stamped raws on the fixed sampler | runner, git `d70dbd8`, base_seed=42, 200 trials/cell |
| `results/processed/task_x_tilt_capfix_analysis.json` | Step 2, C-Q4(i) cap-free re-analysis | `scripts/analyze_task_x_tilt_capfix.py` |
| `results/processed/q4_size_biased_collapse_analysis.json` | Step 3, C-Q4(ii) collapse metric | `scripts/analyze_q4_size_biased_collapse.py` |

Old cap-affected raws (`results/q4_phase2_n10000_gamma*_raw.json`, git `fb0ac42`) and the
S-046 Phase-2 artifact were **preserved** (new output paths) for before/after comparison.

## Method & results

### Step 1 — Re-run the tilt slices on the fixed sampler
Three `_capfix` configs created (identical to the originals except `output.raw_filepath`).
All three swept via `run_sweep(engine="python")`. Raws stamped with commit `d70dbd8`
(≥ the Task Q merge `c4ef634`), confirming the fixed sampler was used. The γ=0 slice is a
control: its sampler path is mathematically unaffected by the water-filling fix, so its raws
should be unchanged — confirmed (γ=0 P(systemic) grid is byte-identical to the pre-fix γ=0
raw across all 80 cells; a large γ=0 change would have signalled a wiring error).

### Step 2 — C-Q4(i) tilt monotonicity, cap-free — **SUPPORTED (now including the γ=0→+1 leg)**
`scripts/analyze_task_x_tilt_capfix.py` re-points `analyze_task_n.py`'s machinery at the
three `_capfix` configs. The `cap_diagnostics` call re-samples with the fixed sampler.

- **Both** adjacent-γ pairs now pass cap-free: `0.0_vs_-1.0` and `1.0_vs_0.0` each report
  7/7 cap-free μ̄ rows, a_c^emp strictly decreasing in γ at every row, **0** significant
  violations, `pass_cap_free = true`, `cap_affected_mu_rows = 0`.
- The γ=0→+1 leg — previously **all** cap-affected/artifact-suspect on this grid — is now a
  valid equal-total-fear test of tilt monotonicity, and it **holds**.
- `threshold_ordering` is strictly decreasing in γ at every in-scope μ̄∈{0.1,…,0.7}:
  e.g. at μ̄=0.4, a_c^emp = 8.00 (γ=−1) → 5.83 (γ=0) → 5.41 (γ=+1).

**Fixed defect (this session):** `analyze_task_n.main()` writes a static `verdict.note`
asserting "the gamma=+1 slice is cap-affected at every mu-bar >= 0.1, so only the (−1, 0)
pair tests the clause cleanly." That is accurate for the *original* cap-affected Task N run
but **stale** here — it contradicts this run's own cap-free verdict. Rather than edit
`analyze_task_n.py` (which would corrupt the accurate S-046 Task N artifact), the Task X
wrapper now overrides `verdict.note` with one **derived from this run's pair verdicts**
(asserts cap-free only when `cap_affected_mu_rows==0` and both pairs pass; otherwise emits
an `AUTO-CHECK` flag rather than a false cap-free claim).

### Step 3 — C-Q4(ii) size-biased collapse — **NOT SUPPORTED (honest negative)**
C-Q4(ii) predicts the size-biased mean fear μ*(γ) — not plain μ̄ — governs ignition: cells
with matched μ* should share the same ignition boundary a_c^emp regardless of γ.
`scripts/analyze_q4_size_biased_collapse.py` computes a_c^emp(μ̄) per γ (resolved crossings
only, D-021 grid-floor filter), attaches the deterministic realized μ* per (μ̄,γ), then
compares the cross-γ spread of a_c^emp interpolated onto a common **μ*** grid vs a common
**μ̄** grid.

- matched-μ̄ spread (mean) = **1.51**; matched-μ* spread (mean) = **3.11**;
  ratio μ*/μ̄ = **2.05 > 1** → `collapse_supported: false`.
- Re-expressing against μ* **increases** the cross-γ spread, so μ* is not the governing
  quantity; μ̄ organizes the boundary better on this grid.
- **Why (physical reading):** since C-Q4(i) holds (higher γ → lower a_c at matched μ̄) and
  μ* rises with γ, matching μ* pits a low-μ̄/high-γ cell against a high-μ̄/low-γ cell, so μ*
  over-corrects — at matched μ*, the ordering flips (higher γ → *higher* a_c). Concretely,
  in the common μ*∈[0.30,0.43] window, γ=+1 a_c ≈ 6.9–9.0 vs γ=−1 a_c ≈ 4.4–6.6.

**Honest caveat (recorded, not hidden):** the μ* ranges barely overlap across γ (γ=−1 spans
μ*∈[0.06,0.43], γ=+1 spans [0.30,0.85]); the common window is narrow (~[0.30,0.43]) and
a_c^emp is steep there, so the *magnitude* of the ratio is grid-limited. The *direction*
(μ* does not collapse; the ordering inverts) is robust and does not depend on the narrow
window. A dedicated μ*-matched sweep would sharpen the magnitude but not the sign.

### Step 4 — End-to-end validation of the Task Q fix — **CONFIRMED**
Checking the **corrected invariant** (`realized_mu_bar` tracking `mu_bar`, NOT `cap_hits`):
all three γ slices report `all_cap_free = True` with `max_rel_shortfall = 0.0000`, including
γ=+1 where the pre-fix shortfall was 7–28%. The fix does **not** drive `cap_hits`→0 — the
γ=+1 diagnostics still show substantial cap activity (up to `cap_hit_fraction ≈ 0.297` at
μ̄=0.7), yet `realized_mu_bar` is exact — exactly the S-054 verified invariant.

## Definition of Done (§5.6) status
- Configs committed-ready (3 new `_capfix` configs); seeds logged (base_seed=42 in-config).
- Raw per-trial outcomes saved, runner-stamped with config+seed+git+timestamp (`d70dbd8`).
- Analysis reads from disk only; no re-simulation for readout.
- §5.4 cross-validation: **N/A this task** — no C++ change, `engine="python"` only. The
  sampler itself already cleared §5.4 at the Task Q merge.
- No figure was requested by the task; readout is the two processed JSON artifacts + this
  report. (A μ*-vs-a_c collapse figure is an optional follow-up, not a DoD gate here.)
- Oracle (`reference.py`) untouched; no frozen okf file edited.

## One-line summary of Q# touched
**Q4:** C-Q4(i) tilt monotonicity now confirmed cap-free including the γ=0→+1 leg (was
artifact-blocked); C-Q4(ii) size-biased-collapse **refuted** on this grid (μ̄ ≻ μ* as the
organizing variable); Task Q water-filling fix validated end-to-end via `realized_mu_bar`.

## [Files Changed · Validation Status · New Decisions]
- **Files:** +3 configs (`configs/q4_phase2_n10000_gamma{0,pos1,neg1}_capfix.json`),
  +2 scripts (`scripts/analyze_task_x_tilt_capfix.py`, `scripts/analyze_q4_size_biased_collapse.py`),
  +3 raws + 2 processed artifacts (runner/analysis-owned), +this report.
- **Validation:** C-Q4(i) cap-free PASS (both pairs 7/7); C-Q4(ii) honest negative
  (ratio 2.05); Task Q invariant confirmed (max_rel_shortfall 0.0000). §5.4 N/A. Pending
  `/verify` gate (reviewer → critic → auditor).
- **New decisions:** none at the model level. Drafts for wrap-up: (a) C-Q4(ii) reads as a
  negative — μ̄ governs the ignition boundary better than μ* on the τ=2.5 grid; (b)
  `okf/next-actions.md` item 5 is now resolved.
