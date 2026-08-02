# Walkthrough — C3a GIRG degree-dependent fear wiring

## Scope actually touched

Only `src/twocascade/runner.py` was edited (the `run_single_trial` else-branch, as
scoped). `task.md`, `implementation_plan.md`, and
`tests/test_girg_fear_wiring.py` were pre-existing spec/gate files in the worktree at
session start and were **not** modified — confirmed by reading them first and diffing
only `runner.py` below. `girg.py`, `reference.py`, and the C++ tree were not touched.

Note on `git diff`: the full worktree diff (pasted below, per instruction) also shows
`task.md` and `implementation_plan.md` differing from HEAD. That state was already
present in the worktree before this session began (this task's spec superseding a prior
task's spec, uncommitted) — not something this session produced. The only hunk this
session is responsible for is the `src/twocascade/runner.py` one.

## What changed

Restructured the non-configuration-model `else` branch of `run_single_trial`: graph
dispatch now runs first (unchanged, for every type), then fear sampling — GIRG routes to
`sample_degree_dependent_fears(weights_girg, mu, gamma, kappa, rng_fear)` (the water-filling
sampler from `graphs.py`, already imported at module top), every other type keeps
`sample_individual_fears` exactly as before.

`src/twocascade/runner.py` diff (from `git diff`):

```diff
diff --git a/src/twocascade/runner.py b/src/twocascade/runner.py
index 0938667..f6523cc 100644
--- a/src/twocascade/runner.py
+++ b/src/twocascade/runner.py
@@ -141,7 +141,6 @@ def run_single_trial(args) -> tuple[float, int]:
         gamma = fear_cfg.get("gamma", 0.0)
         fears, stats = sample_degree_dependent_fears(degrees, mu, gamma, kappa, rng_fear)
     else:
-        fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng_fear)
         if graph_type == "gnp":
             adj = sample_gnp_adjacency(n, p, rng_pair)
         elif graph_type == "girg":
@@ -163,7 +162,14 @@ def run_single_trial(args) -> tuple[float, int]:
                 adj = build_soft_rgg_adjacency(points, r_n, alpha_g, rng_pair)
             else:
                 raise ValueError(f"Unknown graph type: {graph_type}")
-                
+
+        if graph_type == "girg":
+            gamma = fear_cfg.get("gamma", 0.0)
+            fears, fear_stats = sample_degree_dependent_fears(
+                weights_girg, mu, gamma, kappa, rng_fear)
+        else:
+            fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng_fear)
+
     nodes = make_nodes(fears)
```

No import changes: `sample_degree_dependent_fears` was already imported from
`twocascade.graphs` at module top (line 29-33); the `twocascade.girg` import (lines
34-37) only ever pulled `sample_powerlaw_weights` and `sample_girg_adjacency` — it never
imported a stale fear sampler, so nothing needed removing there. `configuration_model`
branch untouched, as scoped.

## Gate test output (measured)

Command: `arch -arm64 python3 -m pytest tests/test_girg_fear_wiring.py -v`

```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.0.2, pluggy-1.6.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /Users/garymei/Downloads/projects/tc-work
configfile: pytest.ini
plugins: anyio-4.12.1, jaxtyping-0.3.9, langsmith-0.7.25
collecting ... collected 5 items

tests/test_girg_fear_wiring.py::test_runner_does_not_use_stale_girg_fear_sampler PASSED [ 20%]
tests/test_girg_fear_wiring.py::test_girg_uses_water_filling_fears_with_weights PASSED [ 40%]
tests/test_girg_fear_wiring.py::test_gnp_path_unchanged PASSED           [ 60%]
tests/test_girg_fear_wiring.py::test_girg_trial_deterministic PASSED     [ 80%]
tests/test_girg_fear_wiring.py::test_girg_gamma_zero_mean_fear_matches_mu PASSED [100%]

============================== 5 passed in 0.16s ===============================
```

All 5 gate assertions pass as-written; none were altered (per instruction, none looked
wrong — they matched the plan's spec exactly: import-hygiene check, weights-not-degrees
spy check on the girg path, gnp-path-untouched spy check, determinism, gamma=0 mean-fear
sanity).

## Full non-slow suite output (measured)

Command: `arch -arm64 python3 -m pytest tests/ -q -m "not slow"`

```
.............sssssssssss..................................s............. [100%]
60 passed, 12 skipped, 2 deselected in 47.11s
```

60 passed, 12 skipped, 2 deselected (the `slow`-marked tests, per the `-m "not slow"`
filter). No failures. No pre-existing failures to report this run.

## `git diff` (full worktree, as requested)

```diff
diff --git a/implementation_plan.md b/implementation_plan.md
index 7134698..0291d62 100644
--- a/implementation_plan.md
+++ b/implementation_plan.md
@@ -1,47 +1,37 @@
-# Implementation plan — C1 GIRG sampler performance port
+# Implementation plan — C3a GIRG degree-dependent fear wiring
 
 ## Scope
 
-One file: `src/twocascade/girg.py`. Replace the body of `sample_girg_adjacency` with an
-exact, block-vectorized evaluation; keep the current implementation available as
-`sample_girg_adjacency_slow` for cross-validation. Public name and signature unchanged, so
-`runner.py:147-154` needs no edit.
+One file: `src/twocascade/runner.py`, the `run_single_trial` graph dispatch only.
 
-## Parity scope — explicit, per §IV
-
-- **C++ parity: NOT in scope this session.** The C++ engine has no GIRG path (`runner.py`
-  routes GIRG to Python only); there is nothing to keep in parity with. If a C++ GIRG path
-  is ever added, THIS Python implementation becomes its §5.4 oracle.
-- **Python reference (`reference.py`): untouched.** It contains no GIRG code; the oracle
-  for this change is the existing O(n²) loop, retained as `sample_girg_adjacency_slow`.
+Current structure samples homogeneous fears at the top of the non-CM else-branch, before
+the graph exists. Change: within the else-branch, dispatch the graph first; then
 
-## Approach (decided — not the delegate's to re-open)
+- `graph_type == "girg"`: `gamma = fear_cfg.get("gamma", 0.0)`;
+  `fears, fear_stats = sample_degree_dependent_fears(weights_girg, mu, gamma, kappa, rng_fear)`
+  (the `graphs.py` water-filling import already present at the top of runner.py — do NOT
+  import anything from `girg.py`'s stale fear sampler).
+- every other type in the else-branch: `sample_individual_fears` exactly as before.
 
-Exact chunked vectorization, NOT approximate bucket pruning: the kernel
-`p = min(1, (w_i w_j / (n d²))^α)` has a long-range tail, so every pair has p > 0 and any
-cell-skip scheme changes the sampled distribution. Evaluate all pairs, but in numpy blocks:
-for row-block I (size ~256–1024 rows), compute torus distances to all j > i vectorized,
-form p, draw uniforms, emit edges. Peak memory O(block × n), never n×n (constitution §I
-forbids a dense n×n adjacency; block-wise temporaries of shape (b, n) with b ≪ n are
-acceptable and must be documented in the code).
+Statement reordering is safe for other families because each purpose has its own
+Generator; moving the fear draw after the graph draw does not change what either stream
+yields.
 
-RNG: vectorized draws consume the stream differently from the scalar loop — statistical
-equivalence is the standard (same as §5.4 cross-language checks), bit-identity is not.
-Determinism given (inputs, seed) is still required.
-
-## Validation (gate test pre-written, delegate may not edit)
+## Parity scope — explicit, per §IV
 
-`tests/test_girg_fast_equivalence.py`: determinism, symmetry/no-self-loop/no-duplicate
-invariants, and two-sample statistical agreement (edge count, mean degree, degree histogram)
-old-vs-new at n=400 over fixed seed sets.
+- **C++ parity: NOT in scope.** No C++ GIRG path exists (`runner.py` GIRG runs Python
+  only). Nothing to mirror.
+- **Python reference (`reference.py`): untouched.** `sample_individual_fears` continues to
+  be imported from it for the unchanged paths.
 
-## Benchmark
+## Out of scope (do not do)
 
-Time one graph at n=2000, n=10000 for both samplers (slow one extrapolated from n=2000 if
-needed); report seconds/graph and projected time for an 11-point × 500-trial arm.
+- No changes to `girg.py` (its stale `sample_degree_dependent_fears` stays as-is this
+  session; removal is a separate cleanup decision).
+- No config file changes, no sweep runs, no C++ code.
 
-## Deliverables
+## Validation
 
-Diff in `src/twocascade/girg.py`, passing gate test, benchmark numbers, `walkthrough.md`
-with all of the above (commands + raw output). Verify gate (blind reviewer → critic →
-auditor) runs after, fed the walkthrough.
+Pre-written gate `tests/test_girg_fear_wiring.py`: spy asserts the girg path calls the
+water-filling sampler with the weights array and that gnp does not; realized mu-bar
+invariant; determinism; gamma=0 mean-fear sanity. Then the full non-slow suite.
diff --git a/src/twocascade/runner.py b/src/twocascade/runner.py
index 0938667..f6523cc 100644
--- a/src/twocascade/runner.py
+++ b/src/twocascade/runner.py
@@ -141,7 +141,6 @@ def run_single_trial(args) -> tuple[float, int]:
         gamma = fear_cfg.get("gamma", 0.0)
         fears, stats = sample_degree_dependent_fears(degrees, mu, gamma, kappa, rng_fear)
     else:
-        fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng_fear)
         if graph_type == "gnp":
             adj = sample_gnp_adjacency(n, p, rng_pair)
         elif graph_type == "girg":
@@ -163,7 +162,14 @@ def run_single_trial(args) -> tuple[float, int]:
                 adj = build_soft_rgg_adjacency(points, r_n, alpha_g, rng_pair)
             else:
                 raise ValueError(f"Unknown graph type: {graph_type}")
-                
+
+        if graph_type == "girg":
+            gamma = fear_cfg.get("gamma", 0.0)
+            fears, fear_stats = sample_degree_dependent_fears(
+                weights_girg, mu, gamma, kappa, rng_fear)
+        else:
+            fears = sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng_fear)
+
     nodes = make_nodes(fears)
     
     if seed_layout == "disc":
diff --git a/task.md b/task.md
index 3bab3ee..7bbf073 100644
--- a/task.md
+++ b/task.md
@@ -1,23 +1,37 @@
-# Task C1 — GIRG sampler performance port (Python)
+# Task C3a — wire GIRG to degree-dependent fears
 
-**Queue item:** okf/next-actions.md §10 item 3(a) (poster Comparison 2 critical path).
-**Conjecture affected:** none directly — this is infrastructure. It unblocks the geometry
-comparison (CM vs GIRG) whose eventual claims live under Q6/D-038. No threshold behavior
-changes; the sampled distribution must be **identical** to the current implementation.
+**Queue item:** poster Comparison 2 (D-038 geometry comparison), fear-model decision of
+2026-08-02: GIRG gets degree-dependent fears, same family as the configuration model, so
+that geometry is the only difference between the CM and GIRG arms.
 
-## Invariant under test
+**Conjecture affected:** none directly — wiring, not physics. Downstream claims live under
+Q6/D-038. The fear DISTRIBUTION for gamma != 0 must come from the Task Q water-filling
+sampler (`graphs.sample_degree_dependent_fears`), NOT the pre-Q implementation that still
+sits in `girg.py` — that local copy has the epsilon-cap undershoot bias Task Q was
+verified to remove (7-28% at gamma > 0 on heavy tails).
 
-`sample_girg_adjacency` must keep sampling from exactly the GIRG measure defined by the
-existing code: for each unordered pair (i,j) at torus distance d,
-`p_ij = min(1, (w_i * w_j / (n * d^2)) ** alpha_g)`, independently across pairs.
-The rewrite may change the RNG consumption order (statistical, not bit-level, equivalence —
-same standard as the §5.4 C++ checks) but not the per-pair distribution.
+## Invariants under test
+
+1. GIRG trials sample fears via `graphs.sample_degree_dependent_fears(weights, mu, gamma,
+   kappa, rng_fear)` — weights as the drawn-degree analogue. The `(w/mean)^gamma` tilt is
+   scale-invariant, so the w_min scale factor cancels.
+2. Every other graph family's behavior is unchanged: gnp/rgg/soft_rgg keep
+   `sample_individual_fears`; configuration_model keeps its existing path. RNG streams are
+   per-purpose (`rng_graph`/`rng_pair`/`rng_fear`/`rng_casc`), so reordering statements
+   must not change any other family's draws.
+3. Task Q invariant holds on the GIRG path: realized mu-bar matches nominal (exact under
+   water-filling unless `infeasible`).
+4. `reference.py` untouched. No C++ changes (no GIRG path exists there).
 
 ## Acceptance
 
-1. New sampler is deterministic given (inputs, seed).
-2. Two-sample statistical agreement with the old sampler at small n (edge count, degree
-   distribution), across independent seeds.
-3. Benchmark at n=10000 makes an 11-point × 500-trial arm feasible in hours, not days.
-4. No dense n×n matrix materialized (constitution §I) — block-wise evaluation only.
-5. `src/twocascade/reference.py` untouched. No C++ changes (no GIRG path exists there).
+Gate test `tests/test_girg_fear_wiring.py` (pre-written) passes; full non-slow suite
+passes; girg trials deterministic given seed; gamma=0 GIRG fears statistically match the
+old homogeneous distribution (same Beta(mu*kappa, (1-mu)*kappa) marginal).
+
+## Reproducibility note (recorded, not hidden)
+
+Old GIRG runs used homogeneous fears drawn in a different stream order; after this change
+they regenerate statistically, not bit-identically. Acceptable because no §5.6-stamped
+GIRG result exists (Task P was demoted to non-result, D-037); noted here so the break is
+documented rather than discovered.
```

(The `task.md`/`implementation_plan.md` hunks above were already present, uncommitted, in
the worktree before this session started — this session did not create or edit them, and
per the assignment they are "not mine to edit." Only the `runner.py` hunk is this
session's work.)

## Claims: measured vs asserted

- **Measured:** gate test tally `5 passed in 0.16s` (pasted terminal output above, exact).
- **Measured:** full non-slow suite tally `60 passed, 12 skipped, 2 deselected in 47.11s`
  (pasted terminal output above, exact).
- **Measured:** `git diff` output (pasted above, exact, full worktree).
- **Asserted (by the pre-written gate test, not independently re-derived here):** the
  girg path is fed GIRG weights (non-integer, min near `w_min`) rather than graph degrees;
  the realized mu-bar matches nominal under water-filling; gamma=0 fears' sample mean is
  within tolerance of `mu`. These are the gate test's own assertions, which passed; I did
  not separately hand-verify the statistical claims outside what the gate test checks.
- **Not run / out of scope:** the two `slow`-marked tests (excluded by `-m "not slow"` per
  instruction) — not evaluated this session, no claim made either way about their status.
- **No pre-existing failures observed** in the non-slow suite this run — nothing to report
  as "pre-existing but unrelated."

## Summary against task.md invariants

1. GIRG trials call `graphs.sample_degree_dependent_fears(weights_girg, mu, gamma, kappa,
   rng_fear)` — verified by `test_girg_uses_water_filling_fears_with_weights` (PASS),
   including the weights-not-degrees and mu_bar/gamma/kappa argument checks.
2. Every other family unchanged — verified by `test_gnp_path_unchanged` (PASS, spy shows
   zero calls to the water-filling sampler) and by the full non-slow suite passing with no
   new failures. `configuration_model` branch was not touched (diff shows no change to
   those lines).
3. Task Q invariant (realized mu-bar == nominal unless infeasible) — verified by the
   `stats["realized_mu_bar"]` assertion inside `test_girg_uses_water_filling_fears_with_weights`
   (PASS).
4. `reference.py` untouched, no C++ changes — confirmed by the diff (only `runner.py`
   touched by this session; `reference.py` and `cpp/` do not appear in the diff at all).

## Out-of-scope items confirmed untouched

- `girg.py` — not in the diff; its stale `sample_degree_dependent_fears` was left as-is.
- No config file changes, no sweep runs, no C++ code — confirmed, diff shows only the
  three markdown/python files listed above.

---

## Addendum — post-review gate hardening (orchestrator, after reviewer + critic)

The blind critic demonstrated the gate passed a mutation that wires the correct sampler to
the WRONG rng stream (rng_casc instead of rng_fear) — the spy never saw the generator.
Remedy: `test_girg_fear_stream_discipline` added to the gate — recomputes the expected
fears offline from SeedSequence(seed).spawn(4) child 2 (after consuming child 0 in the
runner's points-then-weights order) and requires bit-identity with the spy capture. This
pins stream AND order; the critic's mutation now fails the gate.

Re-run after remedy: `arch -arm64 python3 -m pytest tests/test_girg_fear_wiring.py -q` →
`6 passed`.

Follow-ups recorded for the queue (pre-existing, NOT this change): (a) girg + local fear
raises UnboundLocalError on r_n in base; (b) CM and girg branches both discard the fear
stats dict incl. the `infeasible` flag; (c) explicit engine:"cpp" override with a girg
config would silently simulate gnp — auto-detect already guards, override does not.
