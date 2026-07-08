---
type: Decision
title: "D-004: Fork F4: Janson regime p_n = β·n^-α"
description: "Fork F4: Janson p–n regime p_n = beta*n^(-alpha), alpha in (1/r,1); bounded-degree regime rejected."
mutability: append-only
timestamp: 2026-06-03
---

# D-004: Fork F4: Janson regime p_n = β·n^-α

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-004 | 2026-06-03 | Resolved fork F4: p–n regime = Janson regime (np→∞, np^r→0), scaling p_n = β·n^{-α} with α∈(1/r,1) (e.g. α=0.7 for r=2, per §4). Reject the bounded-mean-degree branching/configuration regime (np const, Watts / Amini–Cont–Minca threshold). | The project's μ=0 benchmark IS Janson (§4) and the Wk-1 validation is already built on it, so the growing-degree regime keeps that benchmark sharp and makes the finite-size scaling behind the critical-window interest (Q3) well-defined. Decisively, the advisor's steer is toward a theoretical result — extending Janson's theorems to the fear setup — which is only feasible while staying inside Janson's regime; the bounded-degree route builds on different theory (Watts/ACM) and would abandon the extension. Bounded-degree stays reserved for a possible configuration-model pivot (Q2). | §3.6, §4, §6, §8, §9, §10
