# Task C3b-obs — progress output for Python sweeps

**Motivation (Gary, 2026-08-02):** the Python sweep path is a single blocking
`pool.map` — a multi-hour production sweep runs with zero output between "Starting
sweep..." and completion, so a stalled or crashed run is indistinguishable from a
healthy one. The upcoming Comparison-2 production run is ~6 h; it must be monitorable
from its log alone.

**Conjecture affected:** none — observability only. The sweep's RESULTS must be
bit-identical to the current implementation.

## Invariants

1. Result content and ORDER unchanged: `results_flat` must remain index-aligned with
   `tasks` exactly as `pool.map` returns it. (`imap` preserves order; `imap_unordered`
   does not and is therefore forbidden.)
2. Per-task seeds unchanged — progress reporting must not touch seed derivation.
3. C++ path (`run_single_cell_cpp` / its `pool.map`) untouched.
4. `reference.py` untouched; no C++ changes.

## Acceptance

Gate test `tests/test_sweep_progress.py` (pre-written) passes; full non-slow suite
passes; a small sweep's raw output is deterministic across two runs; progress lines
appear during the run with monotonically increasing counts and a final 100% line.
