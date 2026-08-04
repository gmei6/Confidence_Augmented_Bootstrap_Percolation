---
type: Decision
title: "D-043: the a>=r floor is a mu=0 theorem, not a model invariant; near-floor visuals removed from the poster"
mutability: append-only
timestamp: 2026-08-04
tags: [model, single-seed, poster]
---

# D-043: fear bridges the floor

**Decision.** The a>=r=2 "structural floor" on the critical seed is treated as
deterministic ONLY at mu=0. With fear active, a fear-channel failure can supply
the second failed neighbour, so ignition from a=1 has strictly positive
probability. The poster's near-floor rings/asterisks and footnote were removed
on this basis (the near_floor flags remain in the analysis JSON).

**Rationale.** Gary's argument (2026-08-04), immediately confirmed by the
single-seed experiment (1af8cc1): ignition from a=1 occurs at every mu-bar>0 at
rate ~= 1-exp(-mu-bar), ~independent of <k> and n (expected round-1 fear
failures from one seed are n * mu-bar * (1/n) ~= mu-bar — the n cancels); the
mu=0 control halts at |A*|=1 in 18,000/18,000 trials. Qualifies how the floor is
used in D-012 exclusion logic and the near-floor quantization lesson.

**Affects.** okf/poster/poster.tex, scripts/plot_poster_fear_structure.py,
okf/lessons.md (new entry), interpretation of a_c floors throughout.
