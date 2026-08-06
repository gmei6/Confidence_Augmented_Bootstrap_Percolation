---
type: Concept
title: "Verify — Critic"
description: "Adversarial-test and §5.4 cross-validation criteria for the verify skill's blind critic subagent."
mutability: live
---

# Verify — Critic

Writes and runs adversarial tests: boundary and memory failures, hostile/malformed input, and
anything the reviewer (focused on design) would not have thought to try.

**If C++ changed, run the §5.4 two-prong cross-validation** (`okf/architecture/reproducibility.md`):
1. **Engine logic** — at $\mu=0$ the cascade is deterministic given the graph: dump a graph from
   the Python reference, load the *same* graph in C++, and confirm the final failed set is
   identical (tests the cascade independent of RNG).
2. **Statistics** — for $\mu>0$, confirm the C++ and Python $P(\text{systemic})$ and $|A^*|/n$
   histograms agree within Monte Carlo error over many seeds.

**Bit-identical C++/Python output is never required** — numpy's `Generator` and C++ `<random>`
produce different streams from the same seed by design (§5.4). Do not flag that divergence as a
breakage.

Material breakages (real ones, not the expected RNG-stream divergence) route back to the owning
agent for a fix; re-run the critic after.
