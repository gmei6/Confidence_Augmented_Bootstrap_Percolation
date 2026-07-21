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
