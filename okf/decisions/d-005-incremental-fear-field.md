---
type: Decision
mutability: append-only
timestamp: 2026-06-03
---

# D-005: Fork F1: incremental fear field

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-005 | 2026-06-03 | Resolved fork F1: fear field = INCREMENTAL, g_t = a_{t-1}/n. Cumulative (g_t = A(t-1)/n) rejected outright and NOT retained as a reported contrast (explicitly supersedes §3.6\'s prior "ideally report both"); survivor-hazard kept solely as the §7 fallback if the Wk-2 μ-sweep shows μ inert. | Incremental preserves the frozen analytical core: R_fear≈μ (subcritical, §3.3), all-solvent state linearly stable (critical-seed barrier and §4 saddle-node tangency intact), §3.4 absorbing state genuine, continuous μ=0 Janson limit — keeping the Q1 Janson-extension route tractable. Cumulative makes the empty state linearly unstable for any μ>0 (linearized growth 1+μ): fear becomes an autonomous ignition channel, systemic region degenerates to {a ≳ a_c(r)} ∪ {μa ≳ O(1)} with r demoted (paired sims, n=2000, a=6: at r=4 where a=0.047·a_c, cumulative reaches P(systemic)=0.95 at μ=0.5 vs 0.000 incremental), μ controls speed/odds not size, halting rule becomes load-bearing (g > 0 after a quiet round, contradicting §3.4). Economically: transient news-flow panic (incremental) vs ratcheting panic predicting universal collapse (cumulative). | §3.6 (F1 marked DECIDED; §3.3/§3.4 already written incrementally — no text change)
