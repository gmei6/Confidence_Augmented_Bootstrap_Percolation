---
type: Decision
title: "D-007: Survivor-hazard normalization removed"
description: "Survivor-hazard normalization removed entirely; the mu-inert fallback becomes the heterogeneous-graph pivot."
mutability: append-only
timestamp: 2026-06-03
---

# D-007: Survivor-hazard normalization removed

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-007 | 2026-06-03 | Removed the survivor-hazard normalization (g_t = a_{t-1}/solvent_t) from the project entirely — dropped as the μ-inert fallback, given no code path, and struck from §3.6 (the F1 "retained as §7 fallback" line), §6 (Wk-2 note), and §7 (μ-inert pivot list, which also shed the already-rejected cumulative per D-005). If the Wk-2 μ-sweep shows μ inert, the pivot is now to a heterogeneous graph (configuration model, Q2), not a normalization swap. | The project is committed to the incremental fear model (D-005) and its normalized memory-window extension (D-006); survivor-hazard normalizes by the shrinking solvent set, inflating g_t late in a cascade, which breaks the clean R_fear≈μ subcritical structure (§3.3) and diverges from the Janson-extension route (Q1/D-004) the project now targets. Supersedes the survivor-hazard retention recorded in D-005. | §3.6, §6, §7
