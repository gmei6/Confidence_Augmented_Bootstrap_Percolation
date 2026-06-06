---
name: cross-validation
description: The §5.4 Python↔C++ cross-validation protocol as runnable steps. Use whenever the C++ engine is built or changed, to prove it matches the reference.py oracle before any C++ result is trusted. Never relies on bit-identical RNG streams.
---

# Cross-Validation (Python reference ↔ C++ engine)

`src/twocascade/reference.py` is the oracle (§5.5). The C++ engine is trusted only
after it passes BOTH checks below. numpy's `Generator` and C++ `<random>` produce
different streams from the same seed, so **never** check for bit-identical Monte
Carlo output — validate logic and statistics instead.

## Prong A — Deterministic engine check (μ = 0)
At `mean_fear = 0` the fear channel is off (`reference.py` short-circuits the
Bernoulli draw when `fear_failure_probability == 0`), so the cascade is fully
deterministic given the graph, the seed set, and `r`. This isolates the cascade
logic from RNG.

1. Run `scripts/dump_reference_run.py` to generate a `G(n,p)` graph from the
   reference, run the μ=0 cascade, and write three artifacts to `results/raw/xval/`:
   the adjacency (edge list), the seed indices, and the sorted final failed set.
2. Load **the same graph and seed set** in the C++ engine, run it at `r` with no fear.
3. Assert the C++ final failed set is **identical** (same indices) to the reference's.
   Any difference is a logic bug in the C++ port — not an RNG artifact.

## Prong B — Statistical check (μ > 0)
1. For a small grid of `(r, μ, seed_size)` points, run many trials of
   `estimate_systemic_probability` in the reference and the matching driver in C++.
2. Confirm `P(systemic)` and the `|A*|/n` histograms agree **within Monte Carlo
   error** (compare to ±2 standard errors; a two-sample test such as KS on the
   `|A*|/n` samples is acceptable). They will not match exactly — that is expected.

## Definition of pass
Both prongs pass: identical failed sets at μ=0 AND statistical agreement for μ>0.
Record the result in the session `walkthrough.md` and report it to the orchestrator.
Until both pass, the C++ engine is not trusted and its results are not "done" (§5.6).

## Guardrails
- Never edit `reference.py` to make a check pass — the oracle defines correct behavior.
- Write artifacts only under `results/raw/` via the script, never by hand.
