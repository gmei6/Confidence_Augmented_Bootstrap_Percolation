---
name: reproducible-run
description: The §5.6 Definition of Done as an actionable checklist. Use before marking any simulation result, figure, or experiment "done" to confirm it is fully reproducible from a committed config and a logged seed.
---

# Reproducible Run (Definition of Done)

A result that cannot be regenerated from a seed and a config does not count as done
(§5.4–§5.6). Run this checklist before claiming any result, figure, or experiment is
complete. All items must hold; if any fails, the result is not done.

## Checklist
1. **Config-driven.** The result is produced by a script from a committed config file
   in `configs/` — one file per experiment, no magic numbers in code (§5.3).
2. **Seed logged.** Every RNG is explicit (`numpy.random.default_rng(seed)` in Python,
   a seeded `<random>` engine in C++ — no implicit global state). In C++, each
   realization is seeded as a deterministic function of `(base_seed, realization_index)`.
3. **Raw outputs saved.** Per-realization outcomes are written to `results/raw/` by the
   runner — never by hand — each stamped with the full config, seed(s), git commit
   hash, and a timestamp.
4. **Figure regenerates.** Any figure is reproduced by `plotting.py` reading from
   `results/raw/`; plotting never re-runs the simulation.
5. **Validation passes.** For anything validatable, the check passes — e.g. μ=0
   reproduces Janson's `a_c`; pytest is green.
6. **Cross-language check (if C++ involved).** The result has passed the cross-validation
   skill's two prongs against the Python reference.
7. **Recorded.** The result is reflected in tracker §8, and any fork it resolves is
   logged in §11 (via the session-wrapup agent and the §14 protocol — drafts first).

## Guardrails
- Never write to `results/raw/` or `results/figures/` directly; the runner owns all output.
- "Done" is binary: if you are unsure a result is correct, it is not done — say so (§0 rule 3).
