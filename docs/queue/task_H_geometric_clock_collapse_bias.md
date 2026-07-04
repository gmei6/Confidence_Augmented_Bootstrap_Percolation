# Task H — Geometric clock-collapse bias

**One-line task.** Verify the finite-$n$ step-vs-generation survival bias of the fear-only channel, and confirm that the generational survival probability converges to the step-level geometric clock limit as $a_k = o(n)$.

**Touches:** §4.1 note (step-vs-generation clock mismatch) and the derivation of the $\pi(t)$ form.

## Why this is low-human-input

Purely observational analysis using standard or diagnostic simulation runs. Requires no new simulation knobs, only a small analysis function and plot.

## Plan

1. **Configs.** Reuse the outputs from Task E or F, or create a matched configuration if needed:
   - `pinned_params`: `r=2`, `concentration=50.0`, `theta=0.5`, `window_len=1`, `weights=null`, `target_high_degree=false`.
   - `scaling`: `n_ref=1000`, `target_mean_degree=8.0`, `alpha=0.7`.
   - `sweep`: `mean_fear_grid = [0.3, 0.5]`, `seed_multiples = [0.8, 1.1]`, `trials_per_cell = 1000`, distinct `base_seed` per config.
   - `engine`: `"python"`.
2. **Run.** Execute sweeps if not already run.
3. **Analyze (new code, worktree).** Add to `src/twocascade/analysis.py`:
   - `analyze_clock_collapse_bias(history_by_cell, ...) -> dict`: for each trial and round $k \ge 1$:
     - Calculate the theoretical step-level survival probability: $P_{\text{step}} = (1 - \mu/n)^{a_{k-1}}$.
     - Calculate the generational survival probability: $P_{\text{gen}} = 1 - \mu a_{k-1}/n$.
     - Compute the difference: $\Delta P = P_{\text{step}} - P_{\text{gen}}$.
     - Average this difference over all trials at matched $a_{k-1}$ and $n$.
     - Track the maximum bias across trials.
4. **Figure (worktree).** In `plotting.py`, plot the average bias $\mathbb{E}[\Delta P]$ and maximum bias vs. the ratio $a_{k-1}/n$ for different system sizes $n$.
   - **Expectation:** Demonstrate that the bias vanishes as $a_{k-1}/n \to 0$.
5. **Tests.** Add a unit test in `tests/test_analysis.py` for `analyze_clock_collapse_bias`.

## Parameter grid (summary)

| knob | value |
|---|---|
| `r` | 2 |
| `n` | 1000, 2000, 4000, 8000 |
| `alpha`, `n_ref`, `target_mean_degree` | 0.7, 1000, 8.0 (fixed) |
| `mean_fear` | 0.3, 0.5 |
| `seed_multiples` | 0.8, 1.1 |
| `trials_per_cell` | ≥ 1000 |
| `theta` | 0.5 |

## Definition of Done (§5.6) + what Gary checks

- [ ] All configs committed; raw files stamped.
- [ ] Bias figure regenerates from raw results.
- [ ] `analyze_clock_collapse_bias` has a passing unit test; full suite green.
- [ ] `/verify` returns **AUDIT PASS**. **Gary checks:** does the average bias $\mathbb{E}[\Delta P]$ vanish as $a_{k-1}/n \to 0$? Does this confirm that the generational clock collapses to the step-level geometric clock in the thermodynamic limit?

## Watch-outs (from LESSONS_LEARNED)

- Ensure the analysis accounts for the actual individual fear values $f_i$ when computing individual probabilities, or uses the mean-field approximation with $\mu$ where appropriate. Clarify this distinction in the task description.
