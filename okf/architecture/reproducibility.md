---
type: Concept
title: "§5 — Coding Standards & Architecture (5.4: reproducibility)"
description: "Frozen §5.4: seed-everything rule and the two-prong Python↔C++ cross-validation protocol."
mutability: frozen
---

# §5 — Coding Standards & Architecture (5.4: reproducibility)

### 5.4 Reproducibility (non-negotiable)
- **Seed everything** through an explicit RNG — `numpy.random.default_rng(seed)` in Python, a seeded
  `<random>` engine in C++ — with no implicit global state. A run is deterministic given (config,
  seed). In C++, seed each realization as a deterministic function of (base_seed, realization_index)
  so parallel runs stay reproducible and order-independent.
- Persist, with every results file: the **full config**, the **seed(s)**, the code **git commit
  hash**, and a timestamp.
- **Save raw per-realization outcomes** to `results/raw/`. Analysis and plotting read from disk; they
  never re-run the simulation to make a figure.
- **Cross-language validation (the C++ port must be trusted).** numpy's `Generator` and C++ `<random>`
  produce *different* streams from the same seed, so do **not** expect bit-identical Monte Carlo output
  across languages. Validate two ways: (1) **engine logic** — at $\mu=0$ the cascade is deterministic
  given the graph, so dump a graph from the Python reference, load *the same graph* in C++, and confirm
  the final failed set is identical (this tests the cascade independent of RNG); (2) **statistics** —
  for $\mu>0$, confirm the C++ and Python $P(\text{systemic})$ and $|A^*|/n$ histograms agree within
  Monte Carlo error over many seeds.
