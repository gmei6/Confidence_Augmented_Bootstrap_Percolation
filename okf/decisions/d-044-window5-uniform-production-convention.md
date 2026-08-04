---
type: Decision
title: "D-044: window_len=5 with uniform weights is the recorded production convention"
mutability: append-only
timestamp: 2026-08-04
tags: [model, convention]
---

# D-044: X=5 uniform memory window, recorded

**Decision.** All production sweeps since 2026-07-04 pin window_len=5, weights
[0.2]x5. This is hereby recorded as the standing convention; comparisons must
keep it pinned across arms.

**Rationale.** The value 5 entered with the Q4 configuration-model configs
(8ef3669) without a recorded decision — this entry closes that gap. It is
justified after the fact by D-006 (normalization keeps fear subcritical for
every X) and Task D (S-035, gated: P(systemic) invariant in X within +-0.03
across X in {1,4,8}; only duration grows with X). The specific value is
arbitrary within the proven invariance — a strength when asked, not a tuning.
The core theoretical model remains X=1 (D-006/D-010); the (5, [0.2]x5) cell now
also has direct cross-language Prong B parity (G5.3).

**Affects.** configs/* (pinned_params), advisor-facing explanations of the fear
field; no code change.
