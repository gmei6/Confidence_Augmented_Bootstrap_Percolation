---
type: Reference
title: "Coker & Gunderson (2015)"
description: "Sharp threshold for a modified 2-neighbour bootstrap percolation with recovery on Z^2."
resource: arXiv:1505.08030
tags: [recovery, non-monotone, sharp-threshold, Q7]
---

# Coker & Gunderson (2015)

**Coker, T. & Gunderson, K. (2015)** — "A sharp threshold for a modified bootstrap
percolation with recovery," arXiv:1505.08030.

Defines a non-monotone modification of 2-neighbour bootstrap percolation on `[n]²`:
healthy sites with ≥2 infected neighbours become infected *and*, simultaneously,
infected sites with **zero** infected neighbours "recover" back to healthy (Definition 1,
the recovery update rule `R`). Unlike ordinary bootstrap percolation, the infected set is
not monotone under `R` — a site can cycle between infected and healthy. The paper proves
a sharp threshold `p_c([n]², R)` for the critical initial-infection probability at which
the process still percolates (every site eventually infected) with probability ≥ 1/2,
adapting finite-grid sharp-threshold techniques from the monotone case.

**Relevance:** flagged 2026-07-17 as candidate literature for a possible future revisit
of Q7 (D-031 rejected an SIR-style recovery/healing phase because it breaks monotonicity
— see `../decisions/d-031-discard-tracks-4-5.md`). This is a rigorous existence proof
that a *specific* non-monotone recovery rule (recover only at zero infected neighbours)
still admits a sharp threshold — losing monotonicity does not automatically kill
tractability. The rule as stated is much narrower than a general SIR/healing phase and
would need to be checked against TwoCascade's absolute-`r` solvency channel before it's
usable as-is.
