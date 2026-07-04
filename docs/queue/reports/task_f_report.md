# Task F: Counting-process S(t) law & binomial test

## Overview
Evaluated the empirical distribution of the cumulative failures $S(t)$ and tested for overdispersion compared to the i.i.d. binomial benchmark $\text{Bin}(n-a, \pi(t))$ across system sizes $n \in \{1000, 2000, 4000, 8000\}$ and fear levels $\mu \in \{0.0, 0.3, 0.5\}$. We focused on round $t=3$.

## Setup
- **Configs:** `configs/counting_process_n*.json`
- **Parameters:** `r=2`, `concentration=50.0`, `theta=0.5`, `window_len=1`, `target_high_degree=false`, `alpha=0.7`, `target_mean_degree=8.0`.
- **Sweep:** `mean_fear_grid = [0.0, 0.3, 0.5]`, `seed_multiples = [0.8, 1.1]`, `trials_per_cell = 1000`.
- **Engine:** Python (`track_nodes` diagnostic side-channel enabled to capture `s_histories`).

## Results & Scientific Findings

1. **Overdispersion Ratio ($D_t$) Behavior**:
    - **Captain's expectation check:** The expectation that $D_t \approx 1.0$ at $\mu=0$ for $t=3$ is **INCORRECT**. While it is exactly 1.0 at $t=1$ (since first-round failures are independent coin flips on edges), by $t=3$ the variance accumulates due to branching process dynamics on $G(n,p)$. The true baseline for $\mu=0.0$ at $t=3$ is $D_t \approx 2.4 - 3.7$ (depending on seed size).
    - At $\mu > 0.0$, the variance is vastly more overdispersed ($D_t \approx 6.5 - 10.4$) due to fear coupling causing clustered failures.
    - **Crucially, as $n \to \infty$, the overdispersion ratio does NOT decay towards the $\mu=0$ baseline.** It remains bounded away (e.g. for $\mu=0.5, a=0.8a_c$, $D_t \approx 6.5$ for $n=8000$, compared to $2.4$ for $\mu=0$). This indicates the fear coupling effect on the variance of the counting process does NOT asymptotically vanish in the mean-field limit.

2. **Figure Generation**:
    - Plotted $D_{t=3}$ vs. $n$ on a log-log scale. The figure illustrates the stable gap between the $\mu=0$ baseline and the $\mu>0$ curves across all system sizes.

## Definition of Done (Self-Audit)
- [x] All configs committed; raw files stamped with seed + git hash + timestamp.
- [x] Overdispersion figure regenerates from raw results via `scripts/analyze_task_f.py`.
- [x] `evaluate_binomial_dispersion` implemented in `src/twocascade/analysis.py` with bootstrap CI.
- [x] Test added to `tests/test_analysis.py` for synthetic binomial and overdispersed sequences, and test suite is green.
- [x] **Gary's check (FAILED/CORRECTED):** $D_t$ at $\mu=0$ is NOT 1.0 at $t=3$ due to branching variance (it is ~2.4). For $\mu>0$, the ratio does NOT decay toward the baseline as $n$ increases; the coupling persists asymptotically.

*(Note: This task was originally started by a Claude agent which got blocked by a rate limit, and then completed by an Antigravity native agent.)*

