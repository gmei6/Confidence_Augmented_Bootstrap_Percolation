# Implementation plan — C1 GIRG sampler performance port

## Scope

One file: `src/twocascade/girg.py`. Replace the body of `sample_girg_adjacency` with an
exact, block-vectorized evaluation; keep the current implementation available as
`sample_girg_adjacency_slow` for cross-validation. Public name and signature unchanged, so
`runner.py:147-154` needs no edit.

## Parity scope — explicit, per §IV

- **C++ parity: NOT in scope this session.** The C++ engine has no GIRG path (`runner.py`
  routes GIRG to Python only); there is nothing to keep in parity with. If a C++ GIRG path
  is ever added, THIS Python implementation becomes its §5.4 oracle.
- **Python reference (`reference.py`): untouched.** It contains no GIRG code; the oracle
  for this change is the existing O(n²) loop, retained as `sample_girg_adjacency_slow`.

## Approach (decided — not the delegate's to re-open)

Exact chunked vectorization, NOT approximate bucket pruning: the kernel
`p = min(1, (w_i w_j / (n d²))^α)` has a long-range tail, so every pair has p > 0 and any
cell-skip scheme changes the sampled distribution. Evaluate all pairs, but in numpy blocks:
for row-block I (size ~256–1024 rows), compute torus distances to all j > i vectorized,
form p, draw uniforms, emit edges. Peak memory O(block × n), never n×n (constitution §I
forbids a dense n×n adjacency; block-wise temporaries of shape (b, n) with b ≪ n are
acceptable and must be documented in the code).

RNG: vectorized draws consume the stream differently from the scalar loop — statistical
equivalence is the standard (same as §5.4 cross-language checks), bit-identity is not.
Determinism given (inputs, seed) is still required.

## Validation (gate test pre-written, delegate may not edit)

`tests/test_girg_fast_equivalence.py`: determinism, symmetry/no-self-loop/no-duplicate
invariants, and two-sample statistical agreement (edge count, mean degree, degree histogram)
old-vs-new at n=400 over fixed seed sets.

## Benchmark

Time one graph at n=2000, n=10000 for both samplers (slow one extrapolated from n=2000 if
needed); report seconds/graph and projected time for an 11-point × 500-trial arm.

## Deliverables

Diff in `src/twocascade/girg.py`, passing gate test, benchmark numbers, `walkthrough.md`
with all of the above (commands + raw output). Verify gate (blind reviewer → critic →
auditor) runs after, fed the walkthrough.
