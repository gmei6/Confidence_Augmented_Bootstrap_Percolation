# Task B — θ- and κ(σ)-robustness

**One-line task.** Show the cascade boundary is robust to the systemic-event threshold
$\theta$ and to fear heterogeneity (Beta concentration $\kappa$, i.e. $\sigma$).

**Touches:** §3.5 (θ robustness over $[0.2,0.8]$; separate $\kappa$-sweep), §7 (Watts-window
robustness), §6 Wk 9. No fork opened.

## Why this is low-human-input

The **θ half needs no new simulation at all** — the existing `sweep_wk3_4_r{2,3,4}.json` raw
files already store per-trial `failed_fractions`, so $P(\text{systemic})$ can be recomputed at
any $\theta$. The $\kappa$ half is a handful of cheap configs.

## Plan — Part 1: θ-robustness (re-analysis only, likely worktree for the helper)

1. Confirm `results/raw/sweep_wk3_4_r{2,3,4}.json` exist and contain `failed_fractions` per
   cell. (If absent, regenerate via the committed `configs/sweep_wk3_4_r*.json` first.)
2. **New analysis fn** in `analysis.py`:
   `systemic_prob_at_theta(failed_fractions, theta) -> float`, and a driver that recomputes
   the full $(\mu, \text{seed})$ boundary for `theta ∈ {0.2, 0.35, 0.5, 0.65, 0.8}`.
3. **Figure:** overlay the empirical boundary (e.g. the $\mu$ at which $P$ crosses 0.5 along
   seed-multiple, or a small multi-panel heatmap) for each $\theta$, showing the boundary
   barely moves inside the bimodal trough. Save to `results/figures/`.
4. Add a unit test: `systemic_prob_at_theta` on a known `failed_fractions` vector.

## Plan — Part 2: κ(σ)-sweep (new runs)

1. **Configs** `configs/kappa_sweep_r2_k{K}.json` for `concentration ∈ {2, 10, 50, 200}`
   (recall $\sigma^2 = \mu(1-\mu)/(\kappa+1)$ — small $\kappa$ = high heterogeneity, the
   near-two-point limit; large $\kappa$ = near point-mass at $\mu$). Hold everything else at
   the wk3_4 r=2 settings (`r=2, alpha=0.7, n_ref=1000, target_mean_degree=8.0, n=1000`,
   the standard `mean_fear_grid` and `seed_multiples`, `trials_per_cell=500`, `theta=0.5`,
   distinct `base_seed` per config), `engine="cpp"`,
   `output.raw_filepath: "results/raw/kappa_sweep_r2_k{K}.json"`.
2. **Run** each via `run_sweep`.
3. **Figure:** boundary location vs $\kappa$ — expectation per §3.5 is that $\kappa$ enters
   only at **2nd order**, so the boundary should shift little across the range. Confirm or, if
   it shifts materially, flag it (that would itself be a finding worth surfacing).

## Definition of Done (§5.6) + what Gary checks

- [ ] θ part: boundary recomputed at all five θ from existing raw, figure regenerates, helper
      unit-tested. **No new raw files** (and none written by hand).
- [ ] κ part: four configs committed; raw files stamped with seed + git hash + timestamp;
      figure regenerates from raw.
- [ ] Full test suite green; `/verify` returns **AUDIT PASS** (no C++ logic changed → §5.4
      prongs N/A).
- [ ] `/wrapup` drafts the §8 line. **Gary checks:** is the boundary visibly stable across θ
      in $[0.2,0.8]$? Does κ move the boundary only weakly (2nd order)? Any surprise is flagged,
      not smoothed over.

## Watch-outs (from LESSONS_LEARNED)

- Index results by integer grid coordinates, not float parameter keys.
- Plotting must stay **read-only** on raw + analysis JSONs (no re-stamping
  `analysis_runtime_commit`; D-022).
- At small $\kappa$ the Beta is near two-point $\{0,1\}$ — sanity-check that
  `sample_individual_fears` still returns $E[f]\approx\mu$ (it should; guards exist for
  $\mu\in\{0,1\}$).
