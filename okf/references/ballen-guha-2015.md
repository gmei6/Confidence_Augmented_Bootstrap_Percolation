---
type: Reference
title: "Ballen & Guha (2015)"
description: "Non-uniform-threshold bootstrap percolation sharp dichotomy, plus post-hoc behavioral interventions to halt spread."
resource: arXiv:1512.00834
tags: [non-uniform-threshold, intervention, sharp-dichotomy, Q7, Q8]
---

# Ballen & Guha (2015)

**Ballen, P. & Guha, S. (2015)** — "Behavioral Intervention and Non-Uniform Bootstrap
Percolation," arXiv:1512.00834.

Two contributions: (1) the first sharp-dichotomy result for bootstrap percolation on
Erdős–Rényi graphs with **non-uniform**, per-vertex thresholds `r(u)` (via a "Templated
Multisection" graph construction), extending Janson et al.'s uniform-threshold result;
(2) **behavioral interventions** — after infection reaches a `λn`-node "residual state,"
an external policy (e.g. randomly deleting edges, or raising thresholds) is applied to
try to halt further spread, and the intervention itself is shown to exhibit its own sharp
phase transition between success and failure.

**Relevance:** flagged 2026-07-17 alongside Coker & Gunderson (2015) as candidate
literature for a future revisit of Q7/Q8 (D-031). This is *not* a recovery/healing model
in TwoCascade's sense — infected vertices never revert — so it doesn't directly supply a
"deactivation" mechanism. Relevant for two adjacent reasons instead: (a) the
non-uniform-threshold ER analysis is the technique base if the solvency channel's
threshold `r` were ever made heterogeneous, and (b) "intervention that halts spread" is a
structurally different way to get non-monotone-feeling dynamics without breaking the
absorbing-failure monotonicity D-031 protected — worth comparing against a literal
recovery phase before deciding which is closer to what's wanted.
