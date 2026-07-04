---
mutability: frozen
type: concept
---

# §2 — North Star & Contribution Claim 🔒

**This is what the project *is*. Do not let it drift.**

The honest novelty is **incremental-to-moderate**, and the contribution must be framed accordingly:

> *"A clean, analyzable instance that couples a rigorously-understood local-threshold (Janson-style,
> absolute-$r$) solvency rule with a **self-reinforcing global panic field**, and a characterization
> of how the two channels jointly set the cascade boundary, via a probability-of-systemic-event
> phase diagram."*

**Claim this:** the *self-referential* global feedback (panic proportional to the system's own
recent failure rate — a positive feedback, not an exogenous constant) combined with the *absolute*
threshold rule, analyzed through the systemic-event phase diagram.

**Do NOT claim:** a new contagion *mechanism*. Hybrid local-threshold + probabilistic-channel models,
and threshold + external-field models, are an established subfield (Choi/Min et al. 2018; Miller
2015; Shu et al. 2024; Ruan et al. 2015). Overclaiming will be caught immediately. The ingredients
are known; the specific *instantiation* (global realized-failure-rate field with heterogeneous
individual susceptibility on top of an absolute-$r$ bootstrap rule) appears new.

**Rigor stance (✅ DECIDED D-009, 2026-06-04):** Adopt a **Tiered Stance**.
1. **Rigorously Prove** the auxiliary safety lemmas (specifically, that the fear-only channel at $p=0$ is a subcritical branching process with expected offspring $\mu < 1$, which terminates in $o(n)$ steps with $A^* = O(a)$ w.h.p., and that fear acts as a stochastically bounded amplifier under the combined model).
2. **Conjecture with Mean-Field Analysis** the $(1-\mu)^{r/(r-1)}$ scaling law for the critical seed $a_c(\mu)$ derived from the Poisson-combined self-consistent equations.
3. **Validate via Simulation** the phase diagrams, bimodality, and scaling exponent $\nu$ using a high-performance C++ implementation to preempt finite-size effect arguments.
