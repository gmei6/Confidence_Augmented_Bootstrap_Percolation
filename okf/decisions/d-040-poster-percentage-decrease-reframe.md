---
type: Decision
title: "D-040: Fear x Structure uses per-family percentage decrease, not the D-012 prediction ratio"
mutability: append-only
timestamp: 2026-08-04
tags: [poster, framing]
---

# D-040: percentage-decrease reframe (formalizes Gary's 2026-08-03 call)

**Decision.** The poster's Fear and Structure section states each family's own
measured percentage decrease in a_c(mu-bar) relative to ITS OWN mu-bar=0 anchor,
instead of scoring measured crossings against the D-012 (1-mu-bar)^{r/(r-1)}
prediction. mu-bar=0.7 re-enters for every family. (2026-08-04 follow-ons: the
y-axis is inverted so a decrease reads downward, and the ER-only theory curve is
no longer drawn — it remains in the analysis JSON.)

**Rationale.** (1-mu-bar)^2 is derived for ER only; treating it as a baseline the
configuration model and GIRG were never predicted to meet framed real
measurements as failures. Per-family anchoring is self-contained, and the old
mu-bar=0.7 "exclusion" was an artifact of the prediction-ratio check, not a
property of the measurement. Recorded first in S-063; formalized here.

**Affects.** okf/poster/poster.tex (Fear and Structure), scripts/
analyze_poster_fear_structure.py, D-012's poster-facing use (unchanged as an ER
result; no longer used as a cross-family yardstick on the poster).
