# Implementation plan — C3b-obs sweep progress output

## Scope

One file: `src/twocascade/runner.py`, the Python-engine branch of `run_sweep` only
(the `pool.map(run_single_trial, ...)` call around line 372).

Replace `pool.map` with ordered `pool.imap` (same `chunksize`), collected via a loop
that appends to `results_flat` and prints a progress line roughly every 5% of tasks
(`max(1, len(tasks)//20)` completions) plus a final line:

    progress: 840/2400 tasks (35%), elapsed 312s, est. remaining 580s

Elapsed from `time.monotonic()` captured before the loop; estimated remaining =
elapsed / done * (total - done). Every print `flush=True` so background logs stream.

## Parity scope — explicit, per §IV

- C++ parity: NOT in scope — the C++ cell path keeps its `pool.map` untouched (its
  tasks are per-cell, already coarse; changing it buys little and risks §5.4 churn).
- `reference.py`: untouched.

## Why imap and not imap_unordered

The python path aggregates `results_flat` by index into per-cell lists downstream;
`imap_unordered` would permute trial results across cells — silent data corruption.
`imap` preserves `map` ordering exactly; with the same chunksize the work
distribution is equivalent and per-task results are independent of scheduling.

## Out of scope

No changes to seeds, task construction, output schema, C++ path, configs, or any
other file.

## Validation

Pre-written gate `tests/test_sweep_progress.py`: runs a tiny gnp sweep (n=200,
forced python engine) through `run_sweep` twice into temp paths — asserts identical
raw results (determinism), progress lines present with increasing counts and a
final-total line, and `imap_unordered` absent from the source. Then the full
non-slow suite.
