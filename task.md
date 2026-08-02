# Task C3a — wire GIRG to degree-dependent fears

**Queue item:** poster Comparison 2 (D-038 geometry comparison), fear-model decision of
2026-08-02: GIRG gets degree-dependent fears, same family as the configuration model, so
that geometry is the only difference between the CM and GIRG arms.

**Conjecture affected:** none directly — wiring, not physics. Downstream claims live under
Q6/D-038. The fear DISTRIBUTION for gamma != 0 must come from the Task Q water-filling
sampler (`graphs.sample_degree_dependent_fears`), NOT the pre-Q implementation that still
sits in `girg.py` — that local copy has the epsilon-cap undershoot bias Task Q was
verified to remove (7-28% at gamma > 0 on heavy tails).

## Invariants under test

1. GIRG trials sample fears via `graphs.sample_degree_dependent_fears(weights, mu, gamma,
   kappa, rng_fear)` — weights as the drawn-degree analogue. The `(w/mean)^gamma` tilt is
   scale-invariant, so the w_min scale factor cancels.
2. Every other graph family's behavior is unchanged: gnp/rgg/soft_rgg keep
   `sample_individual_fears`; configuration_model keeps its existing path. RNG streams are
   per-purpose (`rng_graph`/`rng_pair`/`rng_fear`/`rng_casc`), so reordering statements
   must not change any other family's draws.
3. Task Q invariant holds on the GIRG path: realized mu-bar matches nominal (exact under
   water-filling unless `infeasible`).
4. `reference.py` untouched. No C++ changes (no GIRG path exists there).

## Acceptance

Gate test `tests/test_girg_fear_wiring.py` (pre-written) passes; full non-slow suite
passes; girg trials deterministic given seed; gamma=0 GIRG fears statistically match the
old homogeneous distribution (same Beta(mu*kappa, (1-mu)*kappa) marginal).

## Reproducibility note (recorded, not hidden)

Old GIRG runs used homogeneous fears drawn in a different stream order; after this change
they regenerate statistically, not bit-identically. Acceptable because no §5.6-stamped
GIRG result exists (Task P was demoted to non-result, D-037); noted here so the break is
documented rather than discovered.
