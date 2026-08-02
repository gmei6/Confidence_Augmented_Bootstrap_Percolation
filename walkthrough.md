# Walkthrough — C3b-obs: progress output for Python sweeps

## Provenance note

Implementation by a delegated agent (diff below); the agent stalled waiting on a
suite run slowed by a concurrent production pilot and was stopped by the
orchestrator, who completed verification. One gate-test assertion was corrected by
the orchestrator mid-verification — the ORIGINAL TEST WAS WRONG, not the code: its
line filter `re.search("progress", line)` matched the runner's pre-existing
"Raw results saved to <path>" line because pytest's tmp directory embeds the test
name (`test_progress_lines_...`). Fixed to `re.match("^progress:", ...)`. Recorded
per the constitution's test-semantics rule (case a: test corrected).

## Change (git diff vs 8956d75, src/twocascade/runner.py only)

- `import time` added.
- Python-engine branch of run_sweep: `pool.map(run_single_trial, tasks, chunksize)`
  replaced by ordered `pool.imap` (same chunksize) collected in a loop appending to
  results_flat, printing every max(1, total//20) completions and at completion:
  `progress: {done}/{total} tasks ({pct}%), elapsed {s}s, est. remaining {s}s`,
  flush=True, elapsed via time.monotonic(). imap preserves map's result order, so
  the index-aligned per-cell aggregation downstream is unchanged. imap_unordered is
  NOT used (would permute trials across cells; gate enforces its absence).
- C++ branch, seed derivation, task construction, output schema: untouched.

## Evidence (all commands run from the worktree root)

1. Gate (after the test-filter fix):
   `arch -arm64 python3 -m pytest tests/test_sweep_progress.py -q` -> `3 passed in 3.61s`
   Covers: no imap_unordered in source; >=3 `progress:`-prefixed lines with monotone
   `N/M` counts, correct total (60), final line at 60/60; determinism (two identical
   tiny sweeps produce byte-equal results lists); output schema unchanged
   (metadata/sweep_parameters/results, 6 cells x 10 trials).
2. Full non-slow suite: `arch -arm64 python3 -m pytest tests/ -q -m "not slow"` ->
   `64 passed, 12 skipped, 2 deselected in 57.24s` (61 pre-change + 3 new gate tests;
   12 skips are the pre-existing cpp-engine-not-built set).
3. Gate-test tamper check: sha256 attested before implementation
   (f96ff239...), verified unchanged before the orchestrator's own single-line fix,
   which is itself documented above.

## Measured vs asserted

- Measured: both tallies above (pasted from terminal), the progress-line format
  (exercised by the gate's regex), determinism.
- Asserted, not separately measured: wall-clock overhead of imap vs map is
  negligible (chunksize identical; the loop adds one append + integer ops per task).
- Not done: no production-scale sweep was run under this code yet; the first will
  be the C3b production run.
