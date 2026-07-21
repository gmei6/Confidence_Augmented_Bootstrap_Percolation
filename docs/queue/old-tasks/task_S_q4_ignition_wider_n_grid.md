# Task S — Q4(iii) ignition gate: wider n-grid at μ̄=0.4

**Queued and launched:** 2026-07-17. **Conjecture under test:** C-Q4(iii) tail-gating clause,
specifically the μ̄=0.4 caveat flagged in `docs/queue/reports/q4_ignition_report.md`.

**Autonomous-safe: YES.** Config-only — no `src/` or `cpp/src/` changes, reuses the exact
validated engine and config schema from `configs/q4_ignition_tau25_n{4000,10000,20000}.json`.
Launched via `scripts/run_overnight_s051.py` (background, this session).

## Problem

At bounded seed (a=r=2), τ=2.5, the ignition probability at μ̄=0.4 *decreases* with n
(0.134 → 0.116 → 0.062 over n∈{4000, 10000, 20000}), while the μ=0 control stays flat (~0.03,
consistent with Θ(1)). Three n-points can't distinguish "slow decay toward a positive Θ(1)
limit" from "heading to zero" — the report explicitly flags this as needing a wider n-grid
before the Θ(1) claim can be cited at μ̄>0.

## Method

Two new configs, same schema as the existing three, `n_ref=10000` held fixed (per
`docs/queue/README.md`'s scaling-invariant guidance), `seed_multiple` recomputed per-n so the
bounded seed still resolves to `a=2` exactly (`round(seed_multiple · a_c0(n)) = 2`):

| n | seed_multiple | a_c0(n) |
|---|---|---|
| 40000 | 0.0048503 | 412.35 |
| 80000 | 0.0042224 | 473.66 |

(`configs/q4_ignition_tau25_n40000.json`, `configs/q4_ignition_tau25_n80000.json` — same
`mean_fear_grid=[0.0, 0.4]`, `trials_per_cell=500`, `base_seed=42`, `engine="python"` as the
existing three.)

## Expected output

`results/q4_ignition_tau25_n{40000,80000}_raw.json`, runner-stamped. Extends the existing table
to a 5-point n-grid (4k, 10k, 20k, 40k, 80k spanning a 20× range) — enough to fit a trend and
distinguish slow polynomial decay from a positive plateau. Re-run
`scripts/analyze_q4_ignition.py` against the extended raw set once both land; do not hand-edit
`results/`.

## Reports / context

`docs/queue/reports/q4_ignition_report.md`, `okf/next-actions.md` item #1(a) (superseded by this
task file).
