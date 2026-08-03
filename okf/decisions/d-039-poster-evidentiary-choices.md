---
type: Decision
title: "D-039 — Poster evidentiary choices: engine asymmetry closed by §5.4 disclosure, not re-run; 9-curve single-axis hero figure"
mutability: append-only
timestamp: 2026-08-03
tags: [poster, provenance, comparison-1, comparison-2, backfilled]
---

# D-039 — Poster evidentiary choices (backfilled 2026-08-03, Gary-approved)

Two choices made during the 2026-07-27–08-02 poster sprint were recorded only in commit
bodies and LaTeX comments; this entry backfills them so future sessions do not relitigate
either. Both were implicitly authorized under D-038's greenlight; Gary explicitly approved
recording them here on 2026-08-03.

**Decision 1 — Comparison 1's engine asymmetry is closed by disclosure, not by re-running
(next-actions item 2c).** Every ER curve ran on the C++ engine, every configuration-model
and GIRG curve on the Python reference (`engine_resolved` fields in
`results/processed/poster_comparison.json`; the C++ engine has no CM or GIRG path).
Rather than re-running a matching cell on both engines, `okf/poster/poster.tex` carries an
explicit §5.4 cross-engine disclosure (landed in `2024c23`): the poster's headline
comparison is cited as a cross-implementation one under §5.4's statistical-agreement
license, not left unstated. Re-running on matched engines remains available if a reviewer
ever objects, but is not queued.

**Decision 2 — the poster hero is the 9-curve single-axis figure.** Gary accepted the
single-axis design (3 families × $\bar\mu\in\{0,0.4,0.7\}$, exactly 9 series per
`scripts/plot_poster_comparison.py`'s `series_config`) over splitting into per-family
panels, on 2026-08-02 — previously recorded only as an inline comment at
`okf/poster/poster.tex:78-82`. The remaining 6 curves in the processed JSON (ER/CM at
$\bar\mu\in\{0.1,0.2,0.3\}$) feed `results/figures/scaling_law_departure.png` instead.

**Rationale:** the disclosure route was the alternative next-actions item 2c itself
offered, and §5.4 explicitly licenses cross-engine statistical agreement; the 9-curve
hero was a deliberate design acceptance by the project owner, not an agent default.
Neither is discoverable from the live bundle without this entry.

**Affects:** §10 (items 2c, 5, and the new 3b gate item), `okf/changes/s-061-*.md`,
`okf/changes/s-062-*.md`, `okf/poster/poster.tex`. Extends D-038; supersedes nothing.
Session: catch-up of 2026-08-03.
