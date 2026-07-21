# Task Y — Does the fear multiplier come from the g_t normalization?

**Queued:** 2026-07-21. **Status:** hypothesis test, not a confirmatory run.
**Bears on:** the "no mechanism for the multiplier" gap (okf/open-questions), C-Q4(iii).

## The hypothesis

Expected fear-induced failures in one round is
`n · E[f] · g_t = n · μ̄ · (w₁·a/n) = w₁·μ̄·a` — **the n cancels analytically.**
If this is what produces the observed multiplier, two things follow:

1. The multiplier is constant in n and linear in μ̄. Both are observed:
   measured 1.5/1.9/2.6/3.2 at μ̄=0.1…0.4; constrained fit `1 + 5.3·μ̄`, R²=0.98.
2. **Ignition depends on w₁ — the weight on the most recent round — not on
   kernel mass.** This is the discriminating prediction.

## Why (2) is a real test and not a restatement

D-006 (Task D) established the *boundary* is window-invariant: per-failure fear
offspring is μ̄·Σwₖ = μ̄ for every kernel. That is a statement about **steady
state**. Ignition from a bounded seed is a **transient**: at t=1 only one round
has any failures, so only w₁ multiplies it. So:

- D-006 predicts: boundary unchanged by kernel shape.
- This sketch predicts: ignition probability changes by ~w₁ ratio.

If both hold, the mechanism is supported and the two results are complementary.
If ignition is *also* invariant, the sketch is wrong and the multiplier needs
another explanation.

## Method (config-only, autonomous-safe, Local Mode)

Re-run the Task V μ̄-map with a **front-loaded kernel**, everything else identical:

| arm | window_len | weights | w₁ |
|---|---|---|---|
| control (existing raws, no re-run) | 5 | [0.2,0.2,0.2,0.2,0.2] | 0.2 |
| treatment (new) | 5 | [1.0,0.0,0.0,0.0,0.0] | 1.0 |

`window_len` stays 5 in BOTH arms. Do not "shorten the window" instead —
`reference.py:187` halts on `window_len` consecutive empty rounds, so changing it
would alter the halting rule and confound the result.

Configs: copy `configs/q4_ignition_tau25_mumap_n{N}.json`, edit only
`pinned_params.weights` and `output.raw_filepath`. Keep `base_seed=42` and
`seed_multiples` untouched.

## Prediction, pre-registered

multiplier−1 scales by w₁ ratio = 5×. At μ̄=0.4: control 3.2× → treatment ≈ 12×.
Effect is large; n ∈ {4000, 10000, 20000} suffices. **Record the prediction before
looking** — this is exactly the grid-too-narrow trap that cost the Θ(1) claim.

## Falsifies the sketch if

- Ignition is invariant to w₁ (→ mechanism is not the g_t normalization), or
- multiplier−1 scales but not ~linearly in w₁ (→ higher-order effects dominate).

Both outcomes are publishable as constraints. A null here is informative.

---

> **CORRECTION — 2026-07-21, same day as queuing. The pre-registered test above does
> not discriminate. Do not run this task as written.**
>
> An exploratory paired pilot falsified the prediction within hours of writing it.
> Configuration model, τ=2.5, n=4000, μ̄=0.4, d_min=2, r=2, κ=50, seed a=2,
> window_len=5 in both arms, **same graph and same fears in both arms** (paired on
> `default_rng([99, trial])`), 400 trials per arm:
>
> | kernel | w₁ | ignition |
> |---|---|---|
> | uniform `[0.2,0.2,0.2,0.2,0.2]` | 0.2 | **0.147** (59/400) |
> | front-loaded `[1.0,0,0,0,0]` | 1.0 | **0.110** (44/400) |
>
> Two-sided Fisher p = 0.14. The predicted ~5× increase in multiplier−1 is absent;
> the point estimate is if anything in the *opposite* direction, though the pilot
> cannot distinguish that from no effect.
>
> **Why the prediction was wrong.** Both kernels satisfy Σwₖ = 1, so total expected
> fear offspring over the cascade is identical — this is exactly D-006's kernel-mass
> invariance, which the section above cites and then argues past. The claim that
> ignition should still track w₁ rested on ignition being a *transient* (at t=1 only
> one round has failures, so only w₁ multiplies it). That reasoning does not survive a
> multi-round cascade: failures are permanent and `failed_neighbor_count` is
> cumulative, so spreading the same fear mass over five rounds keeps the field alive
> longer and compensates.
>
> **A second correction, to the Method section.** It says shortening the window would
> "confound the result" via the `reference.py:187` halting rule. Too strong for *this*
> measurement: under a front-loaded kernel a zero-failure round zeroes the fear field
> (`1.0 × 0`) and solvency can add nothing new, so the cascade is already over and
> `window_len=5` merely takes four more rounds to notice. Same final state, same
> ignition probability. `window_len` would confound a **duration** measurement, not an
> ignition one. (Raised by Gary, 2026-07-21.)
>
> **What survives.** The n-cancellation is unaffected and needs no experiment:
> `n · μ̄ · (Σwₖ a/n) = μ̄ · Σwₖ a` holds for *any* kernel. So "why is the multiplier
> flat in n" is answered by algebra. It was never contingent on the w₁ test.
>
> **The one salvageable test.** The sketch also predicts the multiplier is *linear* in
> μ̄ (`1 + 5.3·μ̄`, R²=0.98 on four points, μ̄=0.1…0.4). Extending the ignition μ̄-grid to
> 0.5/0.6/0.7 would test that — stays linear ⇒ real support; bends ⇒ sketch incomplete.
> That is a genuine test rather than a confirmation, and it is the version worth
> rewriting this task around.
>
> **Status of the pilot itself: EXPLORATORY.** In-memory only. Nothing written to
> `results/`, no config committed, no seed stamped, no `/verify` gate. It is **not** a
> §5.6 result and must not be cited as one. It is sufficient to retire a prediction,
> not to establish a finding.
>
> **Process note for the record.** This task proposed a mechanism *and* its test in one
> step, and the test was never itself checked for discriminating power before being
> pre-registered. That is the failure mode `okf/lessons.md` §3 already names —
> "a mechanism claim needs its own check, separate from the observation that prompted
> it" — committed while writing that very entry.
