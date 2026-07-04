---
type: Decision
mutability: append-only
timestamp: 2026-06-04
---

# D-008: Fork F2: m/k fear-marks mechanism dropped

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-008 | 2026-06-04 | Resolved fork F2: Drop the $m/k$ fear marks mechanism for the MVP (option a in §3.6). Standardize on the direct-failure fear channel (§3.3) for both Python and C++ engines. | The marks mechanism violates critical Janson-regime assumptions at the threshold level (even $m=1$ mark reduces the solvency barrier to $r-1$, making $np^{r-1} \to \infty$ and trivially satisfying solvency, which destroys the sharp threshold dichotomy). Furthermore, marks break the subcritical amplifier property ($R_{\text{fear}} \approx \mu < 1$) when $m \ge r$ or when marks stack, and render the mean-field saddle-node bifurcation analysis mathematically intractable by replacing the scalar map with a high-dimensional coupled map. Dropping marks avoids a massive parameter space explosion ($r, \mu, m, k$) and keeps the 10-week timeline viable, while the memory-window family (D-006) already provides a clean, tractable persistence handle without coupling to the solvency threshold. | §3.3, §3.6, §8, §9, §10
