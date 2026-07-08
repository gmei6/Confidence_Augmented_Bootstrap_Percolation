---
type: Decision
title: "D-010: window_len/weights exposed in reference engine"
description: "window_len/weights exposed in the reference engine; X=1 default preserves the core model exactly."
mutability: append-only
timestamp: 2026-06-04
---

# D-010: window_len/weights exposed in reference engine

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-010 | 2026-06-04 | Expose `window_len: int = 1` and `weights: list[float] | None = None` in the reference engine (`run_cascade` and `estimate_systemic_probability`). Update the fear channel to compute the normalized memory-window global fear field $g_t = (1/n)\sum_{k=1}^X w_k a_{t-k}$ and generalize the stopping condition to $X$ consecutive quiet rounds. | Enables execution of the Week 9 memory-window invariance robustness study (D-006) while guaranteeing that the default parameter ($X=1$) exactly preserves the core theoretical model ($g_t = a_{t-1}/n$) for all standard sweeps and validations. | §3.6, §8, §10
