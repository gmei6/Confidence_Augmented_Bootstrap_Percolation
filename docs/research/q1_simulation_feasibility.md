# Q1 Simulation Feasibility: Implementation Lift for Bulletproof Validation

This document assesses the implementation lift and computational bottlenecks of building a simulation suite to validate the heuristic mean-field predictions (including the $(1-\mu)^{r/(r-1)}$ scaling law) for the two-channel cascade model.

## 1. Current State of the Codebase
The Python prototype `src/twocascade/reference.py` is a solid foundation. It implements:
- Sparse $G(n,p)$ generation using the Batagelj-Brandes algorithm ($O(n + \text{edges})$).
- The counter-based, two-channel single-cascade engine.
- Simultaneous update dynamics (§3.4).
- Beta-distributed individual fears.

However, to build a *bulletproof* validation suite that can support a research paper, we need to build orchestration scripts, statistical analysis, and plotting components.

## 2. Required Simulation Components for Bulletproof Validation
To validate our heuristic mean-field analysis, we must implement:

### A. 1-D and 2-D Phase Diagrams
- **What**: Expose sweeps over $\mu \in [0, 1]$ (e.g., 30-50 points) and $a$ (seed size relative to $a_c(0)$) to plot $P(\text{systemic})$ contours.
- **Lift**: ~80 lines in `runner.py` / `analysis.py`.
- **Complexity**: Low.

### B. Bimodality Analysis
- **What**: Compute histograms of the final failed fraction $|A^*|/n$. Near the transition, the distribution must be highly bimodal (concentrated at $\approx 0$ and $\approx 1$). We need to compute the Sarle bimodality coefficient to justify the threshold choice $\theta = 0.5$.
- **Lift**: ~40 lines in `analysis.py`.
- **Complexity**: Low.

### C. Mean-Field Overlay & $(1-\mu)^{r/(r-1)}$ Verification
- **What**: Solve the self-consistent recurrence numerically to find the exact saddle-node tangency point for arbitrary parameters. Plot this analytical curve directly over the empirical phase boundary to check for agreement.
- **Lift**: ~60 lines in `meanfield.py`.
- **Complexity**: Moderate (requires a numerical solver like `scipy.optimize` or simple bisection to find the tangency point of the Poisson-combined map).

### D. Finite-Size Scaling & Critical Window Exponent ($\nu$)
- **What**: Run sweeps for $n \in \{1000, 2000, 4000, 8000, 10000\}$ to estimate the transition width $\Delta(n) = p_{90} - p_{10}$ or $a_{90} - a_{10}$, and fit the power-law $\Delta(n) \sim n^{-1/\nu}$.
- **Lift**: ~80 lines in `analysis.py`.
- **Complexity**: Moderate (requires curve fitting and very large sample sizes to reduce noise).

### E. Reproducibility Infrastructure
- **What**: Config parser (JSON/YAML) and seed/metadata logger that records the git hash, seeds, and execution time with every raw output file in `results/raw/`.
- **Lift**: ~50 lines.
- **Complexity**: Low.

## 3. Computational Limits & Bottlenecks
- **Monte Carlo Variance**: Near the critical boundary, variance in $P(\text{systemic})$ is maximal. To obtain a precision of $\pm 0.01$ (95% CI), we need $N \approx 2500$ realizations per cell. For a $50 \times 50$ grid, that is $6.25 \times 10^6$ realizations.
- **Execution Time**:
  - In pure Python, at $n=4000$ and $np \approx 10$, a single realization is fast (~2ms), but $10^6$ runs takes **~33 hours**.
  - A full grid sweep or a multi-n finite-size analysis is **computationally infeasible in pure Python** on a single laptop.
  - **C++ Port Importance**: Porting the hot path (sparse graph generation + single cascade loop) to C++ with OpenMP parallelization is **essential** (D-001). The C++ engine should run at least 50-100x faster, bringing the 33-hour run down to **20 minutes**.
- **Memory**: The sparse representation keeps memory usage minimal ($O(n + np)$). Even for $n=10000$, memory is a few megabytes per realization. Threads in parallel runs do not share mutable state, so memory scale-out is perfect.

## 4. Implementation Effort Summary

| Component | Lines of Code | Complexity | Estimated Time |
|---|---|---|---|
| Phase Diagram Sweeps & Metadata | 100 | Low | 1 day |
| Mean-Field Tangency Solver | 60 | Moderate | 1 day |
| Finite-Size Scaling Exponent Fit | 80 | Moderate | 1.5 days |
| C++ Port + CLI wrapper | 200 | Moderate-High | 3 days |
| Plotting Suite (`plotting.py`) | 120 | Low | 1 day |

**Total focused work**: ~8 days to build a production-quality, bulletproof simulation pipeline.
