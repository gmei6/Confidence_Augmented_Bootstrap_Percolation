---
type: Decision
title: "D-006: Normalized memory-window persistence family"
description: "Normalized memory-window family adopted as the sanctioned persistence extension; X=1 is the decided model."
mutability: append-only
timestamp: 2026-06-03
---

# D-006: Normalized memory-window persistence family

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-006 | 2026-06-03 | Adopted the NORMALIZED memory-window family as the sanctioned persistence extension of the F1 field, replacing the dropped cumulative contrast: g_t = (1/n)·Σ_{k=1..X} w_k·a_{t-k} with Σw_k = 1 (exemplar X=4, w = 0.50/0.25/0.15/0.10); X=1 is exactly the decided model. For X>1 the halting rule generalizes to "halt when the window is empty" (X consecutive quiet rounds), keeping the absorbing state genuine. Study slotted Wk-9/stretch — NOT MVP; Wk-2 sweep runs at X=1. | Normalization is the safety property: per-failure total fear offspring = μ·Σw_k = μ, subcritical for every X (largest root of z^X = μ·Σw_k z^{X-k} is <1 for μ<1); cumulative is the un-normalized infinite-window endpoint. Pilot (n=2000, r=2, a=6=0.6a_c, 300–400 paired trials): P(systemic) invariant in X within ±0.03 (sign tests p≥0.40 at μ∈{0.3,0.5}, X∈{1,4,8}); cascade duration grows with X (≈13.5→31.5 rounds at μ=0.5). Frame the Wk-9 study as an invariance result (candidate robustness lemma for the Q1 extension) plus the duration effect. | §3.6, §6 (Wk-9 robustness line)
