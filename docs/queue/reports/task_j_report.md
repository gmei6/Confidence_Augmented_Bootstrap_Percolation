# Task J Report: Q4 Scoping Doc — Degree-Dependent Fear on a Configuration Model

**Date:** 2026-07-04 (fable overnight run) · **Research question affected:** Q4 (D-028 advisor directive) — this is a new `docs/research/` document, no existing research doc revised (stated per the AGENTS.md §III research-document rule).

## What was produced

`docs/research/q4_config_model_scoping.md` — a self-contained, implementation-ready design doc:

1. **Graph model fully specified:** erased configuration model, Hurwitz-normalized power-law degrees $\mathbb P(D=k)\propto k^{-\tau}$, $k \ge d_{\min}=r$ (avoids a solvency-immune fringe), documented evenness fix, contrast regimes $\tau=3.5$ (finite variance) vs $2.5$ (infinite variance) grounded in the advisor's own papers (in-repo Bhamidi–Dhara–vdH–Sen EJP 2022 §1.1 and the 2024 tiny-giant paper) and van der Hofstad Vol. I. Erased-CM hub-distortion named as a measured risk with a Norros–Reittu fallback.
2. **Fear function fully specified (no TBD):** mean-tilted Beta $f_i\,|\,d_i \sim \mathrm{Beta}(\mu(d_i)\kappa,(1-\mu(d_i))\kappa)$ with $\mu(d)=\bar\mu\,(d/\langle D\rangle)^\gamma/Z_n(\gamma)$ capped at $1-\varepsilon$; the empirical normalizer pins population mean fear at $\bar\mu$ for every tilt, which (a) preserves the subcritical-amplifier invariant $R_\text{fear}\approx\bar\mu<1$ by construction and (b) makes the experiment isolate the fear–degree covariance. $\gamma=0$ reproduces the frozen baseline exactly. The size-biased mean fear $\mu^\star(\gamma)$ is identified as the governing quantity.
3. **Preserved-vs-broken table:** engine dynamics, incremental field (D-005/D-006), Beta family (D-002) carry over; the §4 Janson benchmark and D-004 regime explicitly do **not** apply — reconciled head-on via D-004's own "reserved for a configuration-model pivot (Q2)" clause, which D-028 resolved. North-Star tension (leaving the Janson-extension theory route for the ACM/branching lineage) is flagged as the advisor's conscious trade, not silently absorbed.
4. **Falsifiable conjecture C-Q4** in three clauses — tilt monotonicity, size-biased collapse (matched-$\mu^\star$ boundary collapse), and tail-gated bounded-seed ignition ($\tau\in(2,3)$ vs $\tau>3$) — each with an operational refutation test on plain $P(\text{systemic})$ grids.
5. **Mean-field sketch:** 2-D node/edge-probability tree recursion replacing §4's Poisson map, size-biased offspring law carrying $\mu^\star$, fear exposure telescoping ($\sum_t g_t = A^*/n$), tangency condition, honesty caveats (round-free map; D-025 decoupling does not transfer automatically).
6. **Implementation plan (§IV convention):** new `src/twocascade/graphs.py` (three named functions), additive runner config branch with byte-identical legacy path, **zero `reference.py` changes** (the engine is graph-agnostic — oracle protection is the design's load-bearing choice), C++ parity explicitly scoped out of the pilot / into Phase 2, a three-prong §5.4-style validation plan (generator stats, exact μ=0 same-graph, D-024 p-value statistical prong), numerical re-anchor of the μ=0 benchmark, and RNG/adjacency pitfalls from LESSONS (separate SeedSequence children per stage; no dense matrices; the degree-sampling↔pairing correlated-stream trap named).
7. **Risks with kill-switches:** tilt inertness (cheap paired-trial pilot at $\gamma=\pm2$ before anything else, plus an analytic $\mu^\star$-compression pre-check), erasure distortion, benchmark loss, heavy-tail self-averaging cost, and the direction guard (Q4 stays a track, not the model, until a d-031+ decision).

## Definition of Done check

- [x] Doc exists and is self-contained (defines its own notation, states provenance, readable without the task file).
- [x] Graph model and fear function concrete — every symbol given a value or a named sweep range.
- [x] Conjecture stated precisely enough to test (refutation criteria included).
- [x] §2/§4 reconciliation explicit; tensions flagged rather than absorbed (D-004 clause cited; North-Star trade named; adoption deferred to a future decision entry).
- [x] No file outside `docs/research/` modified.

## Notes for the reviewer

- The task file's worktree references don't apply (docs-only task; container has no git) — edited in place per the task's own environment note.
- The `/verify` (reviewer→critic→auditor) gate is not invocable in this sandbox; substituted a line-by-line self-audit against the DoD and the four watch-out decisions (D-002/D-004/D-005/D-006 — each addressed explicitly in the doc).
- The doc builds on `docs/research/other/souvik_dhara_papers_application.md`'s closing observation (fear heterogeneity is first-order in bounded-degree CM) — Q4's tilt is framed as the direct probe of that claim, which gives the extension a pre-registered reason to expect a live effect.
