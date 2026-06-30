# Task G — Scaling-law extended validation

**One-line task.** Validate the Conjecture 2 scaling law $a_c(\mu) = (1-\mu)^{r/(r-1)}a_c(0)$ across different solvency thresholds $r \in \{2, 3, 4\}$, numerically confirming the exponent $r/(r-1)$.

**Touches:** §4.4 (scaling-law conjecture), §2 (Tiered Stance).

## Why this is low-human-input

Reuses the standard sweep runner and interpolation functions; only config files and plotting scripts need to be created/run. Uses the fast C++ engine.

## Plan

1. **Configs.** Create configs `configs/scaling_law_validation_r{R}.json` for $R \in \{2, 3, 4\}$ and $N \in \{1000, 2000, 4000\}$. Hold parameters:
   - `pinned_params`: `r=R`, `concentration=50.0`, `theta=0.5`, `window_len=1`, `weights=null`, `target_high_degree=false`.
   - `scaling`: `n_ref=1000`, `target_mean_degree=8.0`, `alpha` $\in \{0.7 \text{ for } r=2, 0.5 \text{ for } r=3, 0.4 \text{ for } r=4\}$ (per §4 Janson scaling: $1/r < \alpha < 1$).
   - `sweep`: `mean_fear_grid = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]`, `seed_multiples = [0.5, 0.6, ..., 1.5]` (step 0.05 or 0.1), `trials_per_cell = 1000`, distinct `base_seed` per config.
   - `engine`: `"cpp"`.
2. **Run.** Execute sweeps for each config.
3. **Analyze (new code, worktree).** Add to `src/twocascade/analysis.py` (or reuse):
   - Extract $P(\text{systemic})$ per cell and interpolate the critical seed $a_c(\mu)$ where $P(\text{systemic}) = 0.5$.
   - Calculate the ratio $a_c(\mu)/a_c(0)$ for each $\mu$.
   - Fit $\log(a_c(\mu)/a_c(0)) \sim \gamma \log(1-\mu)$ to estimate the scaling exponent $\gamma$ for each $r$, and check if $\gamma \approx r/(r-1)$.
4. **Figure (worktree).** In `plotting.py`, plot $a_c(\mu)/a_c(0)$ vs. $\mu$ for $r \in \{2, 3, 4\}$, overlaying the theoretical curve $(1-\mu)^{r/(r-1)}$ as a dashed line. Save to `results/figures/`.
5. **Tests.** Verify that the scaling validation runs successfully and returns fitted exponents.

## Parameter grid (summary)

| knob | value |
|---|---|
| `r` | 2, 3, 4 |
| `n` | 1000, 2000, 4000 |
| `alpha` | 0.7 (r=2), 0.5 (r=3), 0.4 (r=4) |
| `n_ref`, `target_mean_degree` | 1000, 8.0 (fixed) |
| `mean_fear` | 0.0 to 0.5 (step 0.1) |
| `seed_multiples` | 0.5 → 1.5 step 0.05 |
| `trials_per_cell` | ≥ 1000 |
| `theta` | 0.5 |

## Definition of Done (§5.6) + what Gary checks

- [ ] All configs committed; raw files stamped with seed + git hash + timestamp.
- [ ] Extended scaling figure regenerates from raw results.
- [ ] `/verify` returns **AUDIT PASS** (with §5.4 cross-validation running for the C++ engine). **Gary checks:** do the fitted exponents $\gamma$ match $r/(r-1)$ (i.e., 2.0 for $r=2$, 1.5 for $r=3$, 1.33 for $r=4$)?

## Watch-outs (from LESSONS_LEARNED)

- Apply the purely empirical threshold clamping (`a_emp > grid_floor`, D-021/D-023) to filter out cells clamped to the physical seed floor before fitting.
