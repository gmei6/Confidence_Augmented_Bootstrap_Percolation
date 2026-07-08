---
type: Decision
title: "D-014: Sweep seeding & optimization protocol"
description: "Sweep seeding protocol: seed sizes scaled to a_c(0), SeedSequence + multiprocessing, histories omitted."
mutability: append-only
timestamp: 2026-06-06
---

# D-014: Sweep seeding & optimization protocol

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-014 | 2026-06-06 | Sweep Seeding & Optimization Protocol | Run 1-D mu sweeps by scaling seed size relative to a_c(0) (clamped to >= r) instead of a_c(mu) to demonstrate amplification; use SeedSequence and multiprocessing for speed and safety; omit round histories by default to prevent large JSON bloat. | §3.5, §5.2, §5.4
