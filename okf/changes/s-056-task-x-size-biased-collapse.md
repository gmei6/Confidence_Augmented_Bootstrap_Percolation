---
type: Session Change
title: "S-056: Task X — C-Q4(i) γ=0→+1 tilt leg confirmed cap-free; C-Q4(ii) size-biased collapse REFUTED"
description: "On the merged Task Q water-filling sampler, the previously artifact-blocked γ=0→+1 tilt leg is now cap-free and supports C-Q4(i); the C-Q4(ii) size-biased-collapse test is a clean negative (μ* increases cross-γ spread ratio 2.05 vs μ̄). /verify AUDIT PASS."
mutability: append-only
timestamp: 2026-07-18
tags: [q4, task-x, c-q4i, c-q4ii, tilt-monotonicity, size-biased, verified]
---

# S-056: Task X — Q4 tilt γ=0→+1 leg + C-Q4(ii) size-biased collapse re-test

## Outcome
Task Q's ε-cap water-filling fix (merged `c4ef634`) unblocked the Q4 experiments that were
artifact-suspect at τ=2.5. Re-ran them on the fixed sampler (raws stamped `d70dbd8`,
`base_seed=42`, 200 trials/cell, `engine="python"`). Cleared the full `/verify` gate:
reviewer qualified sign-off (findings applied), critic PASS, **AUDIT PASS**.

- **C-Q4(i) tilt monotonicity — SUPPORTED cap-free, now including the γ=0→+1 leg.** Both
  adjacent-γ pairs (`0→−1`, `+1→0`) report 7/7 cap-free μ̄ rows with a_c^emp strictly
  decreasing in γ, 0 significant violations. The γ=0→+1 leg, previously *all* cap-affected
  (7–28% realized-μ̄ shortfall), is now a valid equal-total-fear test and it holds.
- **C-Q4(ii) size-biased collapse — REFUTED on this grid (honest negative).** Re-expressing
  the ignition boundary against the size-biased mean μ* *increases* the cross-γ spread
  (matched-μ̄ 1.51 → matched-μ* 3.11; ratio 2.05 > 1). μ̄, not μ*, is the better organizing
  variable. Physical reading: since C-Q4(i) holds (higher γ → lower a_c at matched μ̄) and μ*
  rises with γ, matching μ* pits a low-μ̄/high-γ cell against a high-μ̄/low-γ cell, so μ*
  over-corrects and the ordering inverts. Caveat (disclosed): the μ* overlap across γ is
  narrow (~[0.30,0.43]), so the ratio *magnitude* is grid-limited; the *sign/inversion* is
  robust (critic confirmed stable 2.02–2.08 across interpolation resolutions).
- **Task Q invariant validated end-to-end.** `realized_mu_bar` tracks μ̄ within tolerance
  (max_rel_shortfall 0.0000, ~2e-16) even where `cap_hit_fraction ≈ 0.30` (γ=+1, μ̄=0.7) —
  the verified invariant is realized_mu_bar tracking, NOT cap_hits→0.

## Files
- New: `scripts/analyze_task_x_tilt_capfix.py` (C-Q4(i) re-analysis; overrides the inherited
  stale `verdict.note` with a data-derived cap-free note), `scripts/analyze_q4_size_biased_collapse.py`
  (C-Q4(ii) collapse metric), `configs/q4_phase2_n10000_gamma{0,pos1,neg1}_capfix.json`
  (byte-copies of the originals, new output paths), `docs/queue/reports/task_x_report.md`.
- Regenerated (runner/analysis-owned, gitignored): `results/q4_phase2_n10000_gamma*_capfix_raw.json`,
  `results/processed/{task_x_tilt_capfix_analysis,q4_size_biased_collapse_analysis}.json`.
- Reviewer findings applied in-session: #1 (cap-free note guard now derives from cap_diagnostics
  directly, not the resolved-conditioned counter), #3 (degenerate-vs-refutation distinction),
  critic O3 (final console line shows corrected note). Old cap-affected raws preserved.

## Provenance / integrity
`reference.py` and all frozen okf files untouched; §5.4 N/A (python-only). γ=0 control raw
byte-identical pre/post fix across all 80 cells (wiring check). Resolves `okf/next-actions.md`
item 5.
