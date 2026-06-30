# Task E — Fear-field trajectory concentration

**One-line task.** Measure how the variance of the fear-field trajectory across trials behaves as system size $n$ grows, validating the core concentration assumption of the Asymptotic Decoupling Conjecture.

**Touches:** §4.1 (decoupling conjecture), §4.3 (concentration criterion), row 8 & 14 in `companion_mapping.md`.

## Why this is low-human-input

The simulation setup matches Task A; the analysis checks variance ratios of generation size sequences $(a_k)$ or fear field sequences $(g_k)$ across $n \in \{1000, 2000, 4000, 8000\}$ to establish the convergence rate.

## Plan

1. **Configs.** Create configs in `configs/fear_concentration_n{N}.json` for $N \in \{1000, 2000, 4000, 8000\}$. Hold parameters matched:
   - `pinned_params`: `r=2`, `concentration=50.0`, `theta=0.5`, `window_len=1`, `weights=null`, `target_high_degree=false`.
   - `scaling`: `n_ref=1000`, `target_mean_degree=8.0`, `alpha=0.7`.
   - `sweep`: `mean_fear_grid = [0.3, 0.5]`, `seed_multiples = [0.8, 1.1]` (representing subcritical and near-critical regimes), `trials_per_cell = 1000`, distinct `base_seed` per config.
   - `engine`: `"python"` (to capture full round-by-round histories).
2. **Run.** Execute sweeps for each config.
3. **Analyze (new code, worktree).** Add to `src/twocascade/analysis.py`:
   - `analyze_fear_field_concentration(history_by_cell, ...) -> dict`: for each cell, extract the trajectory of generation sizes $a_k$ (and fear fields $g_k = a_{k-1}/n$).
   - For active rounds $k \in \{1, 2, 3\}$, compute the empirical mean $\mathbb{E}[g_k]$ and variance $\text{Var}(g_k)$ across trials (excluding trials that terminate before round $k$).
   - Compute the relative variance: $\text{Var}(g_k) / \mathbb{E}[g_k]^2$.
   - Fit the scaling relation $\log(\text{relative variance}) \sim -\gamma \log n$ to estimate the decay rate $\gamma$.
4. **Figure (worktree).** In `plotting.py`, plot the relative variance of $g_k$ vs. $n$ on a log-log scale for $k=1, 2, 3$, annotated with the fitted slope $\gamma$. Save under `results/figures/`.
5. **Tests.** Add a test in `tests/test_analysis.py` verifying that `analyze_fear_field_concentration` runs and handles degenerate inputs.

## Parameter grid (summary)

| knob | value |
|---|---|
| `r` | 2 |
| `n` | 1000, 2000, 4000, 8000 |
| `alpha`, `n_ref`, `target_mean_degree` | 0.7, 1000, 8.0 (fixed across n) |
| `mean_fear` | 0.3, 0.5 |
| `seed_multiples` | 0.8 (subcritical), 1.1 (near-critical) |
| `trials_per_cell` | ≥ 1000 |
| `theta` | 0.5 |

## Definition of Done (§5.6) + what Gary checks

- [ ] All configs committed; raw files stamped with seed + git hash + timestamp.
- [ ] Relative variance figure regenerates from raw results.
- [ ] `analyze_fear_field_concentration` has a passing unit test; full suite green.
- [ ] `/verify` returns **AUDIT PASS**. **Gary checks:** does the relative variance decay as $O(1/n)$ ($\gamma \approx 1$)? Is the decay consistent in both subcritical and near-critical seeding regimes?

## Watch-outs (from LESSONS_LEARNED)

- Exclude trials that terminate in round 0 (no new failures) to prevent dividing by zero when computing $a_k / a_{k-1}$.
- Ensure RNG seeding uses `SeedSequence.spawn` per LESSONS_LEARNED.
