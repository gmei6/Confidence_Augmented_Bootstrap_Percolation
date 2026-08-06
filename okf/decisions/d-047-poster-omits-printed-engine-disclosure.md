---
type: Decision
title: "D-047 — Poster omits the printed §5.4 engine disclosure"
mutability: append-only
timestamp: 2026-08-06T15:30:00-04:00
tags: [poster, disclosure, cross-engine, s-066]
---

# D-047 — Poster omits the printed §5.4 engine disclosure

**Decision (Gary, 2026-08-06, submission day):** the printed engine-split
disclosure sentence ("ER simulated on C++; power-law and GIRG on Python;
cross-engine agreement verified") is deliberately omitted from the SURS
poster. Rationale: audience legibility — "other people in the audience
won't get it"; the sentence is jargon to the poster's general audience and
costs caption space.

**What this overrules:** the S-066 pre-print gate's AUDIT PASS carried the
condition "the poster's engine-split disclosure sentence must survive any
further poster edit" (see `walkthrough-s066-preprint-gate.md`, auditor
verdict), which itself descended from queue item 2c (S-061/S-063: the
headline comparison crosses engines and must say so).

**Where the disclosure lives instead:** (a) a prominent comment block in
`okf/poster/poster.tex` directly above the hero caption; (b) the presenter
script `okf/poster/presentation-script.md`, as spoken material if a
technical viewer asks; (c) the §5.4 record itself (cross-engine agreement
verified; girg-cpp-port AUDIT PASS D-045). The disclosure obligation is
thus met in the research record and the conversation layer, not in print.

**Scope:** applies to the printed poster only. Any paper/pre-print derived
from these results MUST restore the printed disclosure — this decision
does not extend to archival documents.

Affects: §5.4 presentation policy; okf/poster/poster.tex; S-066 gate
record interpretation. Supersedes nothing structurally; narrows the S-066
carried condition's application to non-poster artifacts.
