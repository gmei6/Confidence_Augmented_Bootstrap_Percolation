# Task F — Counting-process S(t) law & binomial test

**One-line task.** Characterize the empirical distribution of the cumulative failures $S(t)$ and test for overdispersion compared to the i.i.d. binomial benchmark $\text{Bin}(n-a, \pi(t))$ across system sizes $n$ and fear levels $\mu$.

**Touches:** §4.3 rows 9 and 11 in `companion_mapping.md` (counting process exact law and fear-coupling binomial gap).

## Why this is low-human-input

Uses the existing Python-only diagnostic side-channel (`track_nodes`/`tracked_failure_rounds`, D-026) to extract step-by-step cumulative failure counts.

## Plan

1. **Configs.** Create configs in `configs/counting_process_n{N}.json` for $N \in \{1000, 2000, 4000, 8000\}$. Set parameters:
   - `pinned_params`: `r=2`, `concentration=50.0`, `theta=0.5`, `window_len=1`, `weights=null`, `target_high_degree=false`.
   - `scaling`: `n_ref=1000`, `target_mean_degree=8.0`, `alpha=0.7`.
   - `sweep`: `mean_fear_grid = [0.0, 0.3, 0.5]`, `seed_multiples = [0.8, 1.1]`, `trials_per_cell = 1000`, distinct `base_seed` per config.
   - `engine`: `"python"` (required for the node-tracking diagnostic side-channel).
2. **Run.** Run the sweeps using `engine="python"`.
3. **Analyze (new code, worktree).** Add to `src/twocascade/analysis.py`:
   - `evaluate_binomial_dispersion(failures_at_t, seed_size, n) -> dict`: for a fixed round $t$ (e.g., $t=3$), compute the empirical mean fraction $\pi(t) = \mathbb{E}[S(t) - a]/(n-a)$, empirical variance $\text{Var}(S(t))$, and the overdispersion ratio $D_t = \text{Var}(S(t)) / [(n-a)\pi(t)(1-\pi(t))]$.
   - Compute a bootstrap CI for $D_t$.
4. **Figure (worktree).** In `plotting.py`, plot the overdispersion ratio $D_t$ at $t=3$ vs. $n$ on a log-log or semi-log axis for each $\mu \in \{0.0, 0.3, 0.5\}$.
   - **Expectation:** For $\mu=0.0$, $D_t \approx 1.0$ (binomial variance holds exactly). For $\mu > 0.0$, does $D_t$ decay towards $1.0$ (indicating coupling vanishes asymptotically), or does it remain bounded away from $1.0$?
5. **Tests.** Add a test in `tests/test_analysis.py` for `evaluate_binomial_dispersion` on synthetic binomial and overdispersed sequences.

## Parameter grid (summary)

| knob | value |
|---|---|
| `r` | 2 |
| `n` | 1000, 2000, 4000, 8000 |
| `engine` | **python** (required for `track_nodes`) |
| `alpha`, `n_ref`, `target_mean_degree` | 0.7, 1000, 8.0 (fixed across n) |
| `mean_fear` | 0.0, 0.3, 0.5 |
| `seed_multiples` | 0.8, 1.1 |
| `trials_per_cell` | ≥ 1000 |
| `theta` | 0.5 |

## Definition of Done (§5.6) + what Gary checks

- [ ] All configs committed; raw files stamped with seed + git hash + timestamp.
- [ ] Overdispersion figure regenerates from raw results.
- [ ] `evaluate_binomial_dispersion` test passes; full suite green.
- [ ] `/verify` returns **AUDIT PASS**. **Gary checks:** is the overdispersion ratio $D_t$ at $\mu=0$ indistinguishable from 1.0? For $\mu>0$, does the ratio decay toward 1.0 as $n$ increases?

## Watch-outs (from LESSONS_LEARNED)

- Ensure the Python engine is used, as the C++ engine does not populate `tracked_failure_rounds`. Keep trial counts and sizes balanced to avoid excessive runtimes (Python is slower).
