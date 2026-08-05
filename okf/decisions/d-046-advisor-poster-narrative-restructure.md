---
type: Decision
title: "D-046 — Advisor directive: poster narrative restructure + model schematic (2026-08-04)"
mutability: append-only
timestamp: 2026-08-04
tags: [advisor, scope, poster]
---

# D-046 — Poster narrative restructure + model schematic

**Decision (advisor-directed, meeting 2026-08-04):** The poster gains a new required
element — a small schematic of the model itself (network diagram, red nodes = infected/
failed, a distinct visual encoding for fear, consistent color-coding throughout) — and a
narrative restructure: an explicit motivating sentence framing the fear+heterogeneity+
geometry study as an addition to studying the baseline; a baseline-first talk flow (who
uses it / why it's the baseline, then how it works, under an "Our model / Goal / What are
we looking for" framing); and an overall linear arc (title → what exists → what we did),
which collapses to the same problem → why interesting → what's done → what we did shape
stated twice in the meeting.

**Rationale:** A poster's function is to hold attention and give the presenter something
to point at; the current draft argues its comparisons but never shows the model, and buries
its own motivation for studying fear across graph families. Both gaps were flagged directly
by the advisor as attention/clarity failures, not content failures — no result changes.

**Affects:** `okf/poster/poster.tex` (new figure + restructure), `okf/next-actions.md`
(new poster-queue items). Supersedes nothing; layered on top of D-038/D-039's poster scope.
Session: S-065.
