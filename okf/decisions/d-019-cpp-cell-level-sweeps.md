---
type: Decision
title: "D-019: C++ engine integrated at grid-cell level"
description: "C++ engine integrated into runner.py sweeps at grid-cell level, cutting subprocess overhead to O(N_cells)."
mutability: append-only
timestamp: 2026-06-11
---

# D-019: C++ engine integrated at grid-cell level

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-019 | 2026-06-11 | Integrate C++ engine into runner.py sweeps at grid-cell level. | Grouping trials per cell reduces subprocess spawning overhead from O(N_trials) (~25,000+) to O(N_cells) (<100), allowing C++ to handle multi-trial loops natively. Enforcing OMP_NUM_THREADS=1 per worker prevents thrashing, while keeping run_single_trial preserves backwards compatibility. | §5.1, §5.4
