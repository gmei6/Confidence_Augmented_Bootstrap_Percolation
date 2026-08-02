# Task C1 — GIRG sampler performance port (Python)

**Queue item:** okf/next-actions.md §10 item 3(a) (poster Comparison 2 critical path).
**Conjecture affected:** none directly — this is infrastructure. It unblocks the geometry
comparison (CM vs GIRG) whose eventual claims live under Q6/D-038. No threshold behavior
changes; the sampled distribution must be **identical** to the current implementation.

## Invariant under test

`sample_girg_adjacency` must keep sampling from exactly the GIRG measure defined by the
existing code: for each unordered pair (i,j) at torus distance d,
`p_ij = min(1, (w_i * w_j / (n * d^2)) ** alpha_g)`, independently across pairs.
The rewrite may change the RNG consumption order (statistical, not bit-level, equivalence —
same standard as the §5.4 C++ checks) but not the per-pair distribution.

## Acceptance

1. New sampler is deterministic given (inputs, seed).
2. Two-sample statistical agreement with the old sampler at small n (edge count, degree
   distribution), across independent seeds.
3. Benchmark at n=10000 makes an 11-point × 500-trial arm feasible in hours, not days.
4. No dense n×n matrix materialized (constitution §I) — block-wise evaluation only.
5. `src/twocascade/reference.py` untouched. No C++ changes (no GIRG path exists there).
