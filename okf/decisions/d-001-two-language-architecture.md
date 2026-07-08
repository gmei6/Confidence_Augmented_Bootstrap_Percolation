---
type: Decision
title: "D-001: C++ core + Python orchestration"
description: "Two-language architecture: C++ performance core + Python orchestration, with a pure-Python oracle."
mutability: append-only
timestamp: 2026-06-01
---

# D-001: C++ core + Python orchestration

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-001 | 2026-06-01 | Two-language architecture: C++ for the performance-critical core (G(n,p) generation + cascade engine + realization loop), Python for orchestration / analysis / plotting. Keep a pure-Python reference engine as the validation oracle for the C++ port. Prototype in Python first (Wk 1–2), port the locked hot path to C++ in Wk 3–4. | Hot path is integer/memory-bound and embarrassingly parallel — C++ gives a real, defensible speedup that enables the 10^6–10^7-run critical-window study; also satisfies the C++ learning/résumé goal; the split mirrors numpy/scipy. NOT required for the MVP, so it must not delay the Wk 1–2 go/no-go. Boundary mechanism left open as fork E1. | §5, §6
