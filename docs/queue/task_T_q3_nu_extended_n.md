# Task T — Q3 ν: extend the finite-size fit to n=20000

**Queued and launched:** 2026-07-17. **Question:** Q3 — further tighten Task A / S-048's
finite-size transition-width exponent ν confidence intervals.

**Autonomous-safe: YES.** Config-only — no `src/` or `cpp/src/` changes, C++ engine already
built (`cpp/build/twocascade_run`), reuses the exact schema from
`configs/finite_size_r2_n10000.json`. Launched via `scripts/run_overnight_s051.py` (background,
this session).

## Problem

S-048 added an n=10000 point (C++ engine) and tightened both exponents' CIs materially
(μ=0: ±1.57→±1.04; μ=0.3: ±0.51→±0.26), separating the fear-accelerated-sharpening result to
~4 combined SEs from baseline. One of the three open items surfaced on the advisor-update site
is whether to push further — nothing was queued for it before now.

## Method

New config `configs/finite_size_r2_n20000.json`: identical to `finite_size_r2_n10000.json`
except `pinned_params.n=20000` and a new `output.raw_filepath`; `n_ref=1000`,
`target_mean_degree=8.0`, `alpha=0.7`, the 17-point seed-multiple grid, `trials_per_cell=1000`,
and `base_seed=202607041` are all unchanged (same scaling invariant, same seed — only `n`
moves, per `docs/queue/README.md`'s guidance).

## Expected output

`results/raw/finite_size_r2_n20000.json`, runner-stamped. Extends the ν fit to a 5-point grid
(n∈{1000, 2000, 5000, 10000, 20000}). Re-run `scripts/analyze_q3_nu.py` (500 bootstrap reps,
`fit_finite_size_exponent`) once it lands to get the updated ν(μ=0) / ν(μ=0.3) estimates and
CIs; regenerate `results/figures/finite_size_scaling_r2_n10000.png`'s successor via the
existing plotting path rather than hand-editing anything in `results/`.

## Reports / context

`docs/queue/reports/q3_nu_n10000_report.md`, `advisor-update-2026-07-22/index.html` (the "run
an even larger network size" open item this task now answers).
