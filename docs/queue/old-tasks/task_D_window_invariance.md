# Task D — Memory-window X-invariance robustness (D-006)

**One-line task.** Confirm that the normalized fear memory-window length $X$ leaves the cascade
boundary essentially unchanged (invariant within ±0.03) while cascade **duration** grows with
$X$ — extending the D-006 pilot into a fuller paired study.

**Touches:** §3.6 fork F1 extension / **D-006** (normalized memory-window family,
$g_t = (1/n)\sum_{k=1}^X w_k a_{t-k}$, $\sum w_k = 1$), §6 Wk 9. No fork opened — $X=1$ is the
decided model; this studies the sanctioned extension.

## Why this is low-human-input

The engine already supports it: `run_cascade(..., window_len=X, weights=[...])`, and the runner
threads `pinned_params.window_len` / `pinned_params.weights`. `rounds_completed` is already in
the raw output, so the duration analysis needs no new instrumentation. Mostly config + run +
compare. A small analysis/plot helper may warrant a worktree.

## Background to honor (D-006)

- **Normalization is the safety property:** per-failure total fear offspring $= \mu\sum w_k =
  \mu < 1$, subcritical for **every** $X$. The boundary should depend only on the kernel mass
  ($=\mu$), hence be invariant in $X$.
- Exemplar weights: $X=1 \to [1.0]$; $X=4 \to [0.50, 0.25, 0.15, 0.10]$. For $X=8$ use a
  monotone-decreasing kernel that sums to 1 (e.g. extend the same decay and renormalize) — the
  **engine validates** `len(weights) == window_len` and `sum(weights) ≈ 1.0`, so get this exact.
- Pilot result to reproduce/extend (n=2000, r=2): $P(\text{systemic})$ invariant within ±0.03
  across $X∈\{1,4,8\}$; duration $\approx 13.5 \to 31.5$ rounds at $\mu=0.5$.

## Plan

1. **Configs** `configs/window_r2_X{X}.json` for `X ∈ {1, 4, 8}`, holding everything else
   matched: `r=2, n=2000, alpha=0.7, n_ref=1000, target_mean_degree=8.0, concentration=50.0,
   theta=0.5, target_high_degree=false`; `mean_fear_grid` focused on `[0.3, 0.5]` (the pilot
   points; optionally the full grid), the standard `seed_multiples`, `trials_per_cell` ≥ 300
   (paired), **shared `base_seed`** across the three configs so trials are paired;
   `pinned_params.window_len = X`, `pinned_params.weights` = the kernel above.
   `engine: "cpp"` (the C++ engine supports the window — verify against the reference if unsure
   via the existing `tests/test_window_len.py` / cross-validation skill);
   `output.raw_filepath: "results/raw/window_r2_X{X}.json"`.
2. **Run** each via `run_sweep`.
3. **Analyze:** (a) boundary / $P(\text{systemic})$ per $X$ — confirm max |ΔP| ≤ 0.03 across
   $X$ at matched cells; (b) mean `rounds_completed` per $X$ at $\mu∈\{0.3,0.5\}$ — confirm it
   grows with $X$.
4. **Figures:** $P(\text{systemic})$ overlay across $X$ (should collapse) + a duration-vs-$X$
   bar/line plot. Save under `results/figures/`.

## Definition of Done (§5.6) + what Gary checks

- [ ] Three configs committed; raw files stamped (seed + git hash + timestamp).
- [ ] Invariance figure + duration figure regenerate from raw.
- [ ] If C++ was used for the windowed runs, the §5.4 cross-validation (Prong A at $\mu=0$ /
      Prong B statistics) is run via the `cross-validation` skill and recorded — windowed fear
      is the non-trivial path, so do **not** skip this.
- [ ] `/verify` returns **AUDIT PASS**. **Gary checks:** does $P(\text{systemic})$ collapse
      across $X$ within ±0.03? Does duration grow with $X$ roughly as the pilot found? Is this
      framed as a candidate **robustness lemma** for the Q1 extension (not a new mechanism)?

## Watch-outs (from LESSONS_LEARNED)

- Weights must sum to 1 and match `window_len` exactly or the engine raises — build the $X=8$
  kernel carefully.
- Pair the arms with a **shared base seed**; an unpaired comparison inflates the apparent
  $X$-variation.
- The C++ Beta uses Gamma-ratio sampling with guards at $\mu\in\{0,1\}$ — fine here ($\mu\in
  \{0.3,0.5\}$), but keep cross-validation on since the window code path is exercised.
