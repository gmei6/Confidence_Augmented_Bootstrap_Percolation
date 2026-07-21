# Q3 Report — Finite-Size $\nu$ Tightening with $n = 10000$ (Task A Extension)

**Session:** S-048 (2026-07-05, S-047 overnight batch, sandbox copy). **Question:** Q3 — tighten Task A's wide transition-width exponent confidence intervals by adding an $n=10000$ point via the C++ engine.

## Setup

- New raw: `results/raw/finite_size_r2_n10000.json` — C++ engine, $n=10000$, 34 cells × 1000 trials ($\mu \in \{0.0, 0.3\}$ × 17 seed multiples $[0.6, 1.4]$), `base_seed=202607041`, run inside the overnight driver (commit `fb0ac42`).
- The Task A raws for $n \in \{1000, 2000, 5000\}$ died with the S-044 worktrees; they were **regenerated** from their committed configs via `scripts/run_finite_size_sweeps.py` (C++ engine, same base_seeds — the §5.6 regenerability invariant in action). All four raws runner-stamped.
- Analysis: `scripts/analyze_q3_nu.py` — same machinery as Task A (`estimate_transition_width`, 500 bootstrap reps, seed 20260629; `fit_finite_size_exponent`).

## Findings

Widths $w$ (logistic 10–90%, seed-multiple units) and 4-point fits $w \sim n^{-1/\nu}$:

| $\mu$ | $w(1000)$ | $w(2000)$ | $w(5000)$ | $w(10000)$ | $\nu$ (4-pt) | $\nu$ (Task A 3-pt) |
|---|---|---|---|---|---|---|
| 0.0 | 0.762±0.023 | 0.759±0.019 | 0.643±0.014 | 0.605±0.012 | **8.65 ± 1.04** ($R^2=0.92$) | 8.39 ± 1.57 |
| 0.3 | 0.887±0.016 | 0.814±0.016 | 0.654±0.015 | 0.527±0.014 | **4.54 ± 0.26** ($R^2=0.97$) | 5.33 ± 0.51 |

- **Both CIs tightened materially** ($\mu=0$: ±1.57 → ±1.04; $\mu=0.3$: ±0.51 → ±0.26).
- **The Task A headline is confirmed and sharpened:** global fear accelerates boundary sharpening — the $\mu=0.3$ exponent (4.54) is now separated from the $\mu=0$ baseline (8.65) by ~4 combined standard errors (the 3-pt fits overlapped within ~2).
- The $\mu=0.3$ central value shifted down (5.33 → 4.54, ~1.5 old-SE): the $n=10000$ point pulls the fit toward faster sharpening; the 3-pt fit was extrapolating from a narrow $n$ range.

> **SUPERSEDED 2026-07-18 (Task W, D-036).** The 4-point fits above are retired — do not cite
> $\nu=8.65\pm1.04$ or $\nu=4.54\pm0.26$. The grid now runs to $n=80000$, and the 7-point fits
> ($n\in\{1000,2000,5000,10000,20000,40000,80000\}$) give $\nu(\mu=0)=5.61\pm0.18$
> ($R^2=0.953$) and $\nu(\mu=0.3)=4.82\pm0.15$ ($R^2=0.978$)
> (`results/processed/task_a_nu_n10000.json`, `exponent_fits_by_mu`). The $\mu=0$ interval
> tightened from ±1.04 to ±0.18 and its central value moved by ~3 old-SE — the 4-point fit was
> still extrapolating. **The qualitative headline is unchanged:** fear accelerates boundary
> sharpening, and the two exponents remain separated. Widths keep shrinking through $n=80000$
> with residuals not one-signed (`one_signed_bend_at_large_n: false`), i.e. no flattening.
> The figure `results/figures/finite_size_scaling_r2_n10000.png` is the 7-point version.

## Artifacts

- Raw: `results/raw/finite_size_r2_n{1000,2000,5000,10000}.json` (runner-stamped).
- Analysis: `results/processed/task_a_nu_n10000.json` (`scripts/analyze_q3_nu.py`).
- Figure: `results/figures/finite_size_scaling_r2_n10000.png` (watermarked "Preliminary, pending advisor alignment", matching Task A).
