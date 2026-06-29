# Agent Memory & Lessons Learned

This file records codebase-specific gotchas, performance constraints, and modeling discoveries to prevent future agents from repeating past errors. **Read this file before starting any planning phase.**

---

## 1. Mathematical & Simulation Pitfalls

*   **Beta Distribution Concentration:** When setting individual fear distributions, use the Beta distribution concentration $\kappa$ to tune variance. Avoid truncated normal distributions because their realized mean departs from $\mu$ near boundary values.
*   **Subcriticality of Fear:** Keep in mind that $R_{\text{fear}} \approx \mu < 1$. Fear acts as an amplifier, not a primary igniter. The cascade requires a macroscopic seed to cross the saddle-node tangency point.
*   **Janson Scaling Regime:** Connectivity $p$ must scale as $p_n = \beta n^{-\alpha}$ where $\alpha \in (1/r, 1)$. Never hold $p$ constant when changing $n$ in finite-size sweeps, as it destroys the threshold scaling invariants.
*   **RNG Seeding in Multiprocessing:** When parallelizing sweeps, use `numpy.random.SeedSequence.spawn` rather than simple increments or thread-shared generators to avoid correlated random streams across worker processes.
*   **Avoid Float Dictionary Keys:** In numerical sweeps, avoid indexing dictionaries directly via float parameter keys (e.g. `0.3`), which are vulnerable to representation variance. Instead, stamp results with their grid coordinate integer indexes (`mean_fear_idx`) in the sweep runner.
*   **RNG Seeding Chain:** Avoid using simple `base_seed + trial_index` additions for thread seeding to prevent RNG stream correlation across cells in grid sweeps. Mix the base seed first using a hash (like `SplitMix64`) before adding the trial index.
*   **Near-Floor Quantization Error:** When empirical thresholds (`a_emp`) approach within 1–2 discrete grid points of the absolute floor (`min_seed_size`), statistical deviation metrics skew upwards. These are artifacts of grid spacing constraints rather than scaling law violations. Future validation tracks should incorporate variance-weighted aggregates or assign explicit low-confidence flags to high-mu rows approaching boundary thresholds.
*   **Conflating Finite-Size Inflation with Quantization Error:** Do not misattribute systematic scaling biases to physical seed-size floor constraints (quantization error) unless the data is genuinely clamped near the absolute minimum ($a \ge r$). A $\mu$-dependent residual of the finite-size inflation factor $K(\mu, n)$ can cause systematic biases well above the floor.

## 2. C++ & Performance Pitfalls

*   **Adjacency Representation:** Never materialize dense $n \times n$ adjacency matrices. Always use CSR (Compressed Sparse Row) or light coordinate lists for graph operations.
*   **Random Number Generation:** Cross-validation between Python and C++ must not rely on bitwise RNG stream agreement. Instead, validate via same-graph static runs at $\mu=0$ (exact parity of failed sets) and statistical distributions for $\mu>0$.
*   **Calibrate Cross-Language Parity Thresholds by p-value, Not Fixed Distance:** A fixed two-sample KS *distance* cutoff (e.g. `< 0.05`) is sample-size-dependent and can sit *below* the test's own critical value — at $N=1000$/engine the 5% KS critical value is $\approx 0.061$, so a 0.05 cutoff false-rejects $\approx 16\%$ of the time per check ($\approx 50\%$ across 4 parameterized cells) even when the engines are identical. This manufactures spurious "divergences" and tempts seed-shopping. Use a scale-invariant **p-value** threshold matching the z-test significance (e.g. `p > 0.005`), pair it with a single documented seed on both sides, and confirm via a multi-seed diagnostic (or grand-mean comparison) that genuine parity passes comfortably. The fix is recalibrating the test, never hunting for a seed that passes.
*   **Dynamic Multiprocessing Chunksize:** Grouping tasks using a static `chunksize` can leave workers idle on small sweeps. Dynamically compute the chunksize as `max(1, len(tasks) // (n_workers * 4))`.
*   **C++ Beta Distribution:** `<random>` lacks a native `std::beta_distribution`. Implement manually using Gamma variables ($Z = Y_1 / (Y_1 + Y_2)$) and write guards to prevent undefined C++ behavior if Gamma shape parameters are zero (e.g., at $\mu=0.0$ and $\mu=1.0$).
*   **C++ Compiler Flag Rosetta Conflict:** On Apple Silicon M-series Macs, compiling with an x86_64 target toolchain (e.g. `cmake` installed via x86_64 Homebrew) causes `-march=native` to fail during code generation since the host CPU is detected as `apple-m1`. Use CMake feature-testing dispatch targeting the specific architecture (e.g. check for `-mcpu=native` on Apple, and fallback to `-march=native` elsewhere) and compile with `-DCMAKE_OSX_ARCHITECTURES=arm64` to target ARM64 natively.
*   **Simultaneous Update Parity:** To maintain parity with simultaneous updates, separate evaluation scans from state mutations (flags and neighbor counters must remain frozen until the end of the round). Active lists can be updated in-place at the end of the round using `std::remove_if`.

## 3. Workflow & Tooling Pitfalls

*   **Oracle Protection:** `src/twocascade/reference.py` is the unassailable oracle. Do not edit it as a side-effect of C++ work; any changes require a dedicated and approved plan.
*   **Running Results:** Never write simulation outputs directly to `results/raw/` or `results/figures/`. They must always be written by a runner script that logs the seed, parameters, and commit hash.
*   **GitHub Actions Path Filters and Cleanup Commits:** If a commit deletes or reorganizes temp directories (e.g. `viz-temp/`, `temp_zip/`) without touching files under the `viz/**` path filter, the Pages deploy workflow will not trigger — even if the commit message says "updated viz." When a deploy appears stale after a cleanup commit, add a trivial change (e.g. a trailing newline in `viz/README.md`) to a file inside the watched path and push to force a re-trigger.

## 4. AI Studio Code Generation Pitfalls

*   **AI Studio defaults to React/Vite regardless of spec:** Even when a spec explicitly requires "pure static HTML + CSS + JS, no build step, no frameworks," AI Studio wraps the output in a React/Vite scaffold (`package.json`, `tsconfig.json`, `src/App.tsx`). The actual usable static files are typically in a subfolder. For future requests, add the explicit constraint: *"Do NOT use React, Vite, TypeScript, or any build tool. Output must be exactly three files: index.html, style.css, script.js. No package.json."*
*   **AI Studio `.env.example` and `@google/genai` are template noise:** The generated zip includes a `.env.example` with `GEMINI_API_KEY` and `@google/genai` in `package.json` regardless of whether the spec prohibits API usage. Verify by checking the static HTML's Network tab — no actual API call may be made even when the dependency is present.
*   **`fetch()`-based ZIP download buttons require a server:** A download button implemented with `fetch()` on local files works when served (`http://`) but silently fails from `file://`. For a purely local study page, either omit the button or replace it with a static link.

## 5. Multi-agent Orchestration & CLI Tooling

*   **Avoid Float Crossing Clamping**: When interpolating empirical thresholds, crossings that are stuck at the minimum sweep seed size are clamped floor points (lower bounds, not resolved crossings) under high fear. Check `a_emp > grid_floor` (inequality) rather than checking float equality to filter them out in validation plots.
*   **Runnable Plotting Entry Point**: Keep plotting modules executable as standalone CLI scripts (e.g. via `if __name__ == "__main__":`) so that figures can be automatically regenerated from raw results on disk, ensuring complete reproducibility.
*   **Metadata Provenance Decoupling**: Plotting scripts must never write or overwrite analytical data JSONs. Figure generation should strictly *read* analysis artifacts to prevent silently rewriting `analysis_runtime_commit` stamps and compromising provenance integrity.