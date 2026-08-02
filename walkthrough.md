# Walkthrough — C1 GIRG sampler performance port

## Scope actually touched

Only `src/twocascade/girg.py` was edited. `implementation_plan.md`, `task.md`, and
`tests/test_girg_fast_equivalence.py` were pre-existing (untracked, spec-only) and were not
modified. `scripts/bench_girg.py` and this file are new deliverables, as specified.
`src/twocascade/reference.py`, `runner.py`, and the C++ tree were not touched.

## What changed

`git diff -- src/twocascade/girg.py` (worktree was clean at start of session):

```diff
diff --git a/src/twocascade/girg.py b/src/twocascade/girg.py
index c26fffa..df3c8b0 100644
--- a/src/twocascade/girg.py
+++ b/src/twocascade/girg.py
@@ -9,7 +9,7 @@ def sample_powerlaw_weights(n: int, tau: float, w_min: float, rng: np.random.Gen
     u = rng.uniform(0, 1, n)
     return w_min * (u ** (-1.0 / (tau - 1.0)))
 
-def sample_girg_adjacency(points: np.ndarray, weights: np.ndarray, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
+def sample_girg_adjacency_slow(points: np.ndarray, weights: np.ndarray, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
     n = len(points)
     adj = [[] for _ in range(n)]
     for i in range(n):
@@ -27,6 +27,65 @@ def sample_girg_adjacency(points: np.ndarray, weights: np.ndarray, alpha_g: floa
                 adj[j].append(i)
     return adj
 
+def sample_girg_adjacency(points: np.ndarray, weights: np.ndarray, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
+    """Block-vectorized, exact GIRG adjacency sampler.
+
+    Samples from exactly the same per-pair measure as sample_girg_adjacency_slow:
+    p_ij = min(1, (w_i * w_j / (n * d^2)) ** alpha_g) with torus distance d,
+    independently across pairs (i, j). RNG consumption order differs from the
+    scalar loop (one block draw per row-block instead of one draw per pair), so
+    equivalence is statistical, not bit-identical — same standard as the C++
+    cross-validation checks (constitution §5.4).
+
+    Constitution §I (no dense n x n adjacency): this function never
+    materializes an (n, n) array. Per-block temporaries are shape
+    (block_rows, n - start) at most, with block_rows << n, so peak memory is
+    O(block * n), not O(n^2).
+    """
+    n = len(points)
+    adj = [[] for _ in range(n)]
+    if n < 2:
+        return adj
+
+    x = points[:, 0]
+    y = points[:, 1]
+    block_size = 512
+
+    for start in range(0, n, block_size):
+        end = min(start + block_size, n)
+        rows = np.arange(start, end)          # row indices in this block
+        cols = np.arange(start, n)            # only j >= start can satisfy j > i for i in [start, end)
+
+        # Block temporary of shape (block_rows, len(cols)) <= (block_size, n) —
+        # never the full n x n matrix. Satisfies the no-dense-adjacency rule.
+        dx = np.abs(x[rows, None] - x[None, cols])
+        dx = np.minimum(dx, 1.0 - dx)
+        dy = np.abs(y[rows, None] - y[None, cols])
+        dy = np.minimum(dy, 1.0 - dy)
+        d2 = dx * dx + dy * dy
+
+        zero_dist = (d2 == 0.0)
+        d2_safe = np.where(zero_dist, 1.0, d2)  # avoid div-by-zero; overwritten below
+
+        wi = weights[rows, None]
+        wj = weights[None, cols]
+        p = np.minimum(1.0, (wi * wj) / (n * d2_safe)) ** alpha_g
+
+        # Only j > i pairs are valid; zero-distance pairs are skipped, matching
+        # the slow loop's `if dist_sq == 0: continue`.
+        j_gt_i = cols[None, :] > rows[:, None]
+        p = np.where(j_gt_i & ~zero_dist, p, 0.0)
+
+        u = rng.random(p.shape)  # one rng call per block
+        local_rows, local_cols = np.nonzero(u < p)
+        for lr, lc in zip(local_rows, local_cols):
+            i = start + int(lr)
+            j = start + int(lc)
+            adj[i].append(j)
+            adj[j].append(i)
+
+    return adj
+
 def sample_degree_dependent_fears(weights: np.ndarray, mu_bar: float, gamma: float, kappa: float, rng: np.random.Generator) -> List[float]:
     n = len(weights)
     mean_w = np.mean(weights)
```

Notes on the approach:
- `sample_girg_adjacency_slow` is the original body, renamed only — verified byte-identical
  in behavior by the gate test's `test_slow_sampler_is_verbatim_pre_port`, which reimplements
  the original scalar loop independently and asserts exact adjacency-list equality.
- `sample_girg_adjacency` iterates row blocks of size 512 (within the spec's 256–1024
  range). For block `[start, end)`, only columns `[start, n)` are evaluated (smaller j is
  provably invalid since j must be > i ≥ start), which cuts compute roughly in half versus
  evaluating full-width `(block, n)` blocks every time, while still never materializing an
  n×n array — the largest temporary is `(block_size, n - start) ≤ (512, n)`.
- One `rng.random(p.shape)` call per block (not per pair), matching the "one rng call per
  block" instruction. This changes RNG consumption order vs. the scalar loop, which is why
  equivalence is validated statistically, not bit-for-bit (per task.md and the plan).
- `d2 == 0` pairs are excluded via an explicit mask (`zero_dist`), matching the original's
  `if dist_sq == 0: continue`, with a `d2_safe` substitution used only to avoid a
  divide-by-zero warning before the mask is applied — the substituted values are always
  overwritten to `p = 0.0` afterward, so they cannot affect output.

## Gate test output

Command: `arch -arm64 python3 -m pytest tests/test_girg_fast_equivalence.py -v`

```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.0.2, pluggy-1.6.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /Users/garymei/Downloads/projects/tc-work
configfile: pytest.ini
plugins: anyio-4.12.1, jaxtyping-0.3.9, langsmith-0.7.25
collecting ... collected 3 items

tests/test_girg_fast_equivalence.py::test_determinism_and_invariants PASSED [ 33%]
tests/test_girg_fast_equivalence.py::test_statistical_equivalence_with_slow_sampler PASSED [ 66%]
tests/test_girg_fast_equivalence.py::test_slow_sampler_is_verbatim_pre_port PASSED [100%]

============================== 3 passed in 3.39s ===============================
```

All 3 gate tests pass: determinism/invariants (no self-loops, no duplicates, symmetric,
deterministic given seed), statistical equivalence to the slow sampler (edge count, mean
degree, degree histogram chi-square), and byte-exact verbatim-ness of the renamed slow
sampler against an independent reimplementation of the pre-port loop.

## Full suite

`pytest-timeout` is not installed in this environment, so `--timeout` was dropped as the
task instructions allow.

**First attempt** (`arch -arm64 python3 -m pytest tests/ -x -q`, unfiltered) was still
running after ~7 minutes of CPU time with no output — the output was fully buffered by the
trailing `| tail -15`/`| tail -20` pipe, so nothing would print until the whole run
finished, and it did not finish within a reasonable window. This is **not** related to
`girg.py`: `tests/test_pairwise_decoupling.py` has two `@pytest.mark.slow`-marked tests
(lines 152, 260) which are the only slow-marked tests in the suite and are the evident
cause. Per the coordinator's explicit instruction, I killed that run (it produced only a
partial, non-terminated line of dots/`s` on kill and no summary line — not a usable result,
discarded) and reran excluding slow tests.

**Second attempt**, excluding slow tests:

Command: `arch -arm64 python3 -m pytest tests/ -x -q -m "not slow"`

```
.............sssssssssss........................s.............           [100%]
50 passed, 12 skipped, 2 deselected in 34.78s
```

50 passed, 12 skipped (pre-existing skip conditions, unrelated to this change — not
investigated further per "touch nothing else"), 2 deselected (the two `slow`-marked tests
in `test_pairwise_decoupling.py`, confirmed via `grep -rn "pytest.mark.slow" tests/`).
**The two slow-marked tests were not run in this session.** They live in
`test_pairwise_decoupling.py`, have no relation to `girg.py`, and were excluded solely
because the unfiltered run did not complete in a practical amount of time — stated
explicitly here per the instruction to report anything skipped.

No failures in either run. Nothing in the passing 50 touches `girg.py` behavior beyond what
the dedicated gate test already covers (grep confirms `test_girg_fast_equivalence.py` is the
only test file importing from `twocascade.girg`).

## Benchmark

Script: `scripts/bench_girg.py`. Times single-graph sampling with a fixed seed via
`time.perf_counter`; slow sampler at n=10000 is extrapolated quadratically from the n=2000
measurement (not run directly — see script docstring) rather than executed, since the
O(n²) scalar loop at n=10000 would take on the order of a minute per call and isn't needed
for the projection.

Command: `PYTHONPATH=/Users/garymei/Downloads/projects/tc-work/src arch -arm64 python3 scripts/bench_girg.py`

(Note: the interpreter on this machine resolves a bare `twocascade` import to
`/Users/garymei/Downloads/projects/CABP/src/twocascade` via a path entry ahead of the
worktree, unrelated to this change — `pytest.ini`'s `pythonpath = src` setting handles this
automatically for pytest, but the standalone benchmark script needed `PYTHONPATH` set
explicitly to pick up the worktree's `girg.py` instead of the main repo's. Verified via
`python3 -c "import twocascade; print(twocascade.__file__)"` before and after setting
`PYTHONPATH`.)

Raw output:

```
Timing slow sampler...
  slow n=1000: 0.6219 s
  slow n=2000: 2.4478 s
Timing fast sampler...
  fast n=1000: 0.0280 s
  fast n=2000: 0.0826 s
  fast n=10000: 1.3817 s

============================================================
sampler        n    sec/graph  note
------------------------------------------------------------
slow        1000       0.6219  measured
slow        2000       2.4478  measured
slow       10000      61.1946  extrapolated (quadratic from n=2000)
fast        1000       0.0280  measured
fast        2000       0.0826  measured
fast       10000       1.3817  measured
============================================================

Speedup at n=2000: 29.6x (slow 2.4478s / fast 0.0826s)
Projected speedup at n=10000: 44.3x (slow extrap 61.1946s / fast measured 1.3817s)

Projected sampling-only cost for 11 grid points x 500 trials x 3 fear arms = 16500 graphs at n=10000:
  fast sampler:          6.333 hours (22798.5 s)
  slow sampler (extrap): 280.5 hours (1009710.7 s)
```

Interpretation: 29.6x measured speedup at n=2000, ~44x projected at n=10000. The fast
sampler brings the target 11-point × 500-trial × 3-fear-arm sweep at n=10000 from a
projected ~280 hours (slow, extrapolated — infeasible) down to a projected ~6.3 hours
(sampling cost only; does not include cascade simulation time on top of sampling).

## Summary against acceptance criteria (task.md)

1. Deterministic given (inputs, seed) — verified by
   `test_determinism_and_invariants` (PASS).
2. Two-sample statistical agreement (edge count, degree distribution) at small n across
   independent seeds — verified by `test_statistical_equivalence_with_slow_sampler` (PASS).
3. n=10000 benchmark makes an 11-point × 500-trial arm feasible in hours, not days —
   6.3 projected hours for sampling across all 3 fear arms (task.md says "an" arm; my table
   reports the full 3-arm total per the task's own benchmark instruction — per-arm alone is
   ~2.1 hours). Either reading is comfortably "hours, not days."
4. No dense n×n matrix — largest temporary per block is `(512, n)`, documented in-code.
5. `reference.py` untouched; no C++ changes — confirmed, `git status` shows only
   `girg.py` modified plus the new `scripts/bench_girg.py` and this file.

## Honesty notes / what was skipped or uncertain

- The two `@pytest.mark.slow` tests in `test_pairwise_decoupling.py` were not run this
  session (see "Full suite" above) — excluded on explicit instruction after the unfiltered
  run failed to complete in a practical window. They are unrelated to `girg.py`.
- The first full-suite attempt was killed mid-run and produced no usable summary; no
  pass/fail result is claimed from it.
- The 12 skipped tests in the filtered run were not investigated (pre-existing, not part of
  this task's scope, "touch nothing else").
- The n=10000 slow-sampler timing is an extrapolation, not a measurement, as explicitly
  permitted by the task instructions.
- This file (`walkthrough.md`) previously contained unrelated content from a different,
  earlier task in this worktree (a Q4 P(systemic) boundary-fit writeup). It has been
  overwritten with this task's content, as instructed ("Write ... walkthrough.md").

---

## Addendum — post-review hardening (orchestrator, after reviewer + critic passes)

The blind critic showed the original gate test never exercised the multi-block path
(all cases n <= 512 = one block): a mutant dropping every cross-block edge passed the
gate (its harness: scratchpad/critic/mutate.py). Two remedies applied before audit:

1. `tests/test_girg_fast_equivalence.py`: added `test_multiblock_level_set_identity` —
   constant-threshold stub RNG at n=1300 (three blocks, uneven last), edge-set identity
   fast-vs-slow at c in {1e-6, 0.3, 0.9}. This deterministically catches cross-block
   edge loss and constant-factor probability errors (verified by the critic's mutants).
2. `src/twocascade/girg.py`: one-line `assert alpha_g > 0` guarding the only parameter
   region where the min/power reordering diverges (unreachable in any current config).

Re-run after remedies:
- `arch -arm64 python3 -m pytest tests/test_girg_fast_equivalence.py -q` → `4 passed in 8.65s`
- `arch -arm64 python3 -m pytest tests/ -q -m "not slow"` → `51 passed, 12 skipped, 2 deselected in 39.80s`
