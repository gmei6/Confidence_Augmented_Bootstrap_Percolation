# Agent Memory & Lessons Learned

This file records codebase-specific gotchas, performance constraints, and modeling discoveries to prevent future agents from repeating past errors. **Read this file before starting any planning phase.**

---

## 1. Mathematical & Simulation Pitfalls

*   **Beta Distribution Concentration:** When setting individual fear distributions, use the Beta distribution concentration $\kappa$ to tune variance. Avoid truncated normal distributions because their realized mean departs from $\mu$ near boundary values.
*   **Subcriticality of Fear:** Keep in mind that $R_{\text{fear}} \approx \mu < 1$. Fear acts as an amplifier, not a primary igniter. The cascade requires a macroscopic seed to cross the saddle-node tangency point.
*   **Janson Scaling Regime:** Connectivity $p$ must scale as $p_n = \beta n^{-\alpha}$ where $\alpha \in (1/r, 1)$. Never hold $p$ constant when changing $n$ in finite-size sweeps, as it destroys the threshold scaling invariants.
*   **RNG Seeding in Multiprocessing:** When parallelizing sweeps, use `numpy.random.SeedSequence.spawn` rather than simple increments or thread-shared generators to avoid correlated random streams across worker processes.
*   **Avoid Float Dictionary Keys:** In numerical sweeps, avoid indexing dictionaries directly via float parameter keys (e.g. `0.3`), which are vulnerable to representation variance. Instead, stamp results with their grid coordinate integer indexes (`mean_fear_idx`) in the sweep runner.

## 2. C++ & Performance Pitfalls

*   **Adjacency Representation:** Never materialize dense $n \times n$ adjacency matrices. Always use CSR (Compressed Sparse Row) or light coordinate lists for graph operations.
*   **Random Number Generation:** Cross-validation between Python and C++ must not rely on bitwise RNG stream agreement. Instead, validate via same-graph static runs at $\mu=0$ (exact parity of failed sets) and statistical distributions for $\mu>0$.
*   **Dynamic Multiprocessing Chunksize:** Grouping tasks using a static `chunksize` can leave workers idle on small sweeps. Dynamically compute the chunksize as `max(1, len(tasks) // (n_workers * 4))`.
*   **C++ Beta Distribution:** `<random>` lacks a native `std::beta_distribution`. Implement manually using Gamma variables ($Z = Y_1 / (Y_1 + Y_2)$) and write guards to prevent undefined C++ behavior if Gamma shape parameters are zero (e.g., at $\mu=0.0$ and $\mu=1.0$).

## 3. Workflow & Tooling Pitfalls

*   **Oracle Protection:** `src/twocascade/reference.py` is the unassailable oracle. Do not edit it as a side-effect of C++ work; any changes require a dedicated and approved plan.
*   **Running Results:** Never write simulation outputs directly to `results/raw/` or `results/figures/`. They must always be written by a runner script that logs the seed, parameters, and commit hash.