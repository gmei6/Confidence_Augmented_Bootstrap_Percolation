# Implementation plan — C3a GIRG degree-dependent fear wiring

## Scope

One file: `src/twocascade/runner.py`, the `run_single_trial` graph dispatch only.

Current structure samples homogeneous fears at the top of the non-CM else-branch, before
the graph exists. Change: within the else-branch, dispatch the graph first; then

- `graph_type == "girg"`: `gamma = fear_cfg.get("gamma", 0.0)`;
  `fears, fear_stats = sample_degree_dependent_fears(weights_girg, mu, gamma, kappa, rng_fear)`
  (the `graphs.py` water-filling import already present at the top of runner.py — do NOT
  import anything from `girg.py`'s stale fear sampler).
- every other type in the else-branch: `sample_individual_fears` exactly as before.

Statement reordering is safe for other families because each purpose has its own
Generator; moving the fear draw after the graph draw does not change what either stream
yields.

## Parity scope — explicit, per §IV

- **C++ parity: NOT in scope.** No C++ GIRG path exists (`runner.py` GIRG runs Python
  only). Nothing to mirror.
- **Python reference (`reference.py`): untouched.** `sample_individual_fears` continues to
  be imported from it for the unchanged paths.

## Out of scope (do not do)

- No changes to `girg.py` (its stale `sample_degree_dependent_fears` stays as-is this
  session; removal is a separate cleanup decision).
- No config file changes, no sweep runs, no C++ code.

## Validation

Pre-written gate `tests/test_girg_fear_wiring.py`: spy asserts the girg path calls the
water-filling sampler with the weights array and that gnp does not; realized mu-bar
invariant; determinism; gamma=0 mean-fear sanity. Then the full non-slow suite.
