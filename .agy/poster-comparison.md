# Task: poster comparison sweep — Erdős–Rényi vs configuration model

Build the configs, driver, analysis and plotting for the D-038 poster's headline
comparison: **the effect of degree heterogeneity on cascade ignition**, at matched network
size and matched mean degree.

This is tasks T2–T4 of the poster plan. GIRG (the geometry comparison) is a separate,
later task — do not attempt it here.

## The calibrated constant everything depends on

Already measured by `scripts/calibrate_matched_degree.py`; result committed at
`results/processed/matched_degree_calibration.json`. **Do not re-derive it, and do not
substitute a different value:**

| quantity | value |
|---|---|
| configuration model, τ=2.5, d_min=2, n=10000 | realised ⟨k⟩ = **4.5332** ± 0.0256 (post-erasure, 20 replicates) |
| Erdős–Rényi matched at n=10000 | `target_mean_degree` = **4.5336** |

Two traps around this number:

1. The existing `configs/q4_*.json` files carry `scaling.target_mean_degree: 4.0`. That is
   **not** the configuration model's mean degree — on that code path the runner computes
   `p` and then ignores it, and the value survives only to normalise `janson_a_c` for
   `seed_multiples`. Do not copy 4.0 forward as if it were a matched value.
2. The match is to the **realised, post-erasure** mean degree, not the drawn one. Erasure
   costs about 0.09 of a degree here.

## What to build

### 1. Four configs in `configs/`

`poster_er_mu0.json`, `poster_er_mu40.json`, `poster_cm_mu0.json`, `poster_cm_mu40.json`.

All four share this grid exactly — same seed, same seed sizes, so the families are paired:

```json
"pinned_params": {
  "n": 10000, "r": 2, "concentration": 50, "theta": 0.5,
  "window_len": 5, "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
  "target_high_degree": false
},
"scaling": { "target_mean_degree": 4.5336, "n_ref": 10000, "alpha": 0.6 },
"sweep": {
  "seed_sizes": [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48],
  "trials_per_cell": 50,
  "base_seed": 42
}
```

Per-family differences, and nothing else:

- **ER configs** — omit the `graph` block entirely (`gnp` is the runner's default family).
  Leave `engine` unset so it auto-resolves to the C++ binary, which is built.
- **CM configs** — `"graph": {"type": "configuration_model", "tau": 2.5, "d_min": 2}` and
  `"fear": {"gamma": 0.0}`, both inside `pinned_params`. Set `"engine": "python"`.
  **γ = 0.0 is required and must not be changed**: the configuration-model branch is the
  only one that uses the degree-tilted fear sampler, and at γ ≠ 0 the comparison would vary
  degree heterogeneity *and* fear–degree coupling at the same time, which is precisely what
  this experiment is designed to separate.
- **`_mu0` configs** — `"mean_fear_grid": [0.0]`. **`_mu40` configs** —
  `"mean_fear_grid": [0.4]`. The μ̄ = 0 arm is a required control, not an optional extra:
  it is what lets the fear effect be reported as a difference of differences.
- `output.raw_filepath` — `results/poster_er_mu0_raw.json` and so on, matching the config name.

### 2. `scripts/run_poster_comparison.py`

Follow the structure of the existing `scripts/run_q4_psys_boundary.py`: chdir to the repo
root, then loop the four configs calling `twocascade.runner.run_sweep`. Accept optional
config-name arguments to run a subset. Do not write to `results/` yourself.

### 3. `scripts/analyze_poster_comparison.py`

Read the four raw files, compute P(systemic) per (family, μ̄, seed size) with a **Wilson
score interval** at 95%, and write `results/processed/poster_comparison.json`.

### 4. `scripts/plot_poster_comparison.py`

Read only the processed JSON — never the raws — and write
`results/figures/poster_comparison.png`. P(systemic) on y, seed size on x, error bars from
the Wilson intervals.

Encoding, which is not negotiable because the poster's headline depends on it:

- **Colour carries the family**, line style carries fear. Not the reverse — the poster's
  claim is about network structure, so family must be the more salient channel.
- Configuration model `#BD5A2E`, Erdős–Rényi `#2E6E76`. Reserve `#8E4A72` for GIRG later.
- μ̄ = 0 solid, μ̄ = 0.4 dashed.
- Figure background `#F6F3EA`, text `#1E2530`. These match the poster.
- Do not use a default matplotlib colour cycle.

## Run it, at 50 trials only

Run all four configs at `trials_per_cell: 50` and generate the figure. **Stop there.** Do
not raise the trial count — a pilot at 50 exists to check that the seed grid actually
resolves both transitions before a 500-trial run is committed to.

## What to report

In the report, give the P(systemic) table for all four configs across the seed grid, and
answer this explicitly:

> Does the seed grid `[1..48]` resolve the transition for **both** families — that is, does
> each family have points both near 0 and near 1, with intermediate values in between?

There is real reason to expect it may not. Prior results show the configuration model at
τ = 2.5 igniting from a seed as small as a = 2, while Erdős–Rényi in the Janson regime
needs a seed on the order of `janson_a_c`. If those scales are far enough apart, no single
grid resolves both — the configuration model would sit pinned near 1 everywhere and
Erdős–Rényi near 0 everywhere. If that is what you observe, say so plainly and propose a
grid that would work; do not quietly widen the grid and re-run.

## Acceptance checks

- All four raw files exist under `results/`, each stamped by the runner with seed,
  parameters and git commit.
- `results/figures/poster_comparison.png` regenerates byte-identically when
  `scripts/plot_poster_comparison.py` is run twice from the committed processed JSON.
- Every ER config resolves to the C++ engine and every CM config to Python — the runner
  prints which engine it used.
- On the μ̄ = 0.4 CM arm, confirm `realized_mu_bar` tracks the nominal 0.4.

Write your findings to `.agy/poster-comparison/report.md`. Reply with at most 5 lines: what
you changed, what you verified, and anything you could not do.
