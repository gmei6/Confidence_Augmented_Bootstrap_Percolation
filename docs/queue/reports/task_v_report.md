# Task V — addendum: the pooled μ̄=0.4 replicate strengthens Task W's non-flattening verdict

**Session:** S-058 (2026-07-19). **Status of Task V itself:** already DONE and `/verify`-cleared
in `d70dbd8` (reviewer sign-off, critic PASS, AUDIT PASS) — see that commit's body. This file is
**not** a Task V report; it records one statistic derived from Task V's data that was not computed
at the time.

## The unexploited replicate

Task V's μ̄=0.4 column is an **independent replicate** of the Task S μ̄=0.4 series, not a
reproduction. `engine="python"` takes `runner.py:318-326`, where cell seeds are drawn from a flat
`ss.spawn(num_cells * trials_per_cell)` consumed in cell-major order — so widening the fear grid
from 2 to 5 values re-indexes μ̄=0.4 onto a different stream (μ̄=0.0, at index 0 in both grids,
stays bit-identical). The two series agree: per-n two-proportion z = +0.19, +1.69, −0.99, −0.14,
+0.16; joint Σz² = 3.91 on 5 df, **p = 0.56**. Pooling to 1000 trials/n is therefore valid at
**μ̄=0.4 only** — μ̄=0.0 is the same trials and would double-count.

## Result

Task W's verdict (the n≈20000 flattening is not a shared crossover) rests in part on the
n≥20000 ignition trend test, and W's own critic recorded it as marginal and endpoint-sensitive:
**z = −2.12, p = 0.034**. Pooling the replicate addresses exactly that weakness:

| μ̄=0.4, n≥20000 | counts | test | p |
|---|---|---|---|
| Task S, single series | 31, 25, 22 /500 | χ²(2) = 1.70 | 0.43 |
| Pooled replicate, 3 pts | 70, 51, 43 /1000 | χ²(2) = 7.44 | 0.024 |
| Pooled + n=160000 | 70, 51, 43 /1000, 17/500 | χ²(3) = 11.58 | 0.009 |
| **Pooled + n=160000, Cochran–Armitage trend** | — | **z = −3.31** | **0.0009** |

**Reading:** the ignition branch is still declining at n≥20000, now at p=0.0009 rather than
p=0.034. This **corroborates and strengthens** Task W's existing verdict — it does not revise it.
Task S's original p=0.43 flattening reading came from a single 500-trial series and does not
survive doubling the trials.

**Caveat:** the pooled analysis was specified after the replicate was discovered, so it is a
directed re-test of Task S's stated claim, not a pre-registered one. It is reported here as one
test on one pre-existing series, without multiplicity adjustment, on that basis.

## Provenance

Derived from committed artifacts only: `results/q4_ignition_tau25_mumap_n{N}_raw.json` and
`results/q4_ignition_tau25_n{N}_raw.json` (all `base_seed=42`, 500 trials/cell, `engine="python"`,
commit `e066fd8`). No `src/`, `cpp/src/`, `configs/`, or `results/` changes. §5.4 N/A (Python-only).
The statistics above are **not** currently regenerable from a committed script —
`scripts/analyze_q4_mumap.py` emits the p-grid and Wilson intervals but no inferential layer.
Folding them into that script is the clean fix if this number is cited.
