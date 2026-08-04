---
type: Decision
title: "D-042: famcompare CM curve rebased onto the matched-4.5336 ensemble; 'geometry damps fear' retracted as an ensemble artifact"
mutability: append-only
timestamp: 2026-08-04
tags: [famcompare, ensembles, retraction]
---

# D-042: CM rebase + geometry-claim retraction

**Decision.** The Fear Amplifies (famcompare) configuration-model curve at
n=10000 is sourced from the poster CM arms' a=2 cells (mean degree 4.5336, all
eight mu-bar values, baseline poster_cm_mu0), replacing the q4-mumap source
(mean degree 4.0). A runtime pinned-param check in analyze_famcompare.py fails
loudly on any future source mismatch. The poster sentence "Geometry appears to
damp it slightly further" is RETRACTED: on matched data GIRG and power-law
interleave (GIRG 8.3x vs CM 6.6x at 0.7, tied 0.2-0.5) with overlapping CIs.

**Rationale.** The old CM source sat on a 13%-sparser ensemble than the ER and
GIRG curves it was compared against, which manufactured a consistent GIRG-below-
CM gap. The corrected comparison supports "geometry doesn't measurably change
fear's effect," consistent with Fear and Structure's threshold-level result.
n=4000/20000 CM main-panel entries remain q4-sourced and are flagged in
metadata.cm_ensemble_by_n; the figure draws n=10000 only.

**Affects.** scripts/analyze_famcompare.py, scripts/plot_famcompare_ratio.py,
okf/poster/poster.tex (Fear Amplifies), Q6's narrative in okf/open-questions.md.
