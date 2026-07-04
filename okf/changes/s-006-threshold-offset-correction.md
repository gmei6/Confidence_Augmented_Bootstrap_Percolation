---
type: Session Change
mutability: append-only
timestamp: 2026-06-03
---

# S-006: Threshold-offset wording corrected

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §12 (Session Changelog) on 2026-07-04:

> S-006 | 2026-06-03 | v1.4 | Corrected misleading wording in §8/§10: the ~28% threshold offset at n=4000 is a finite-size effect set by the magnitude of a_c (present in any p–n regime), NOT an "np correction" removed by the Janson form — a multi-n check showed both the bounded-degree and Janson p-forms tighten toward 1 as n grows, and the two forms are numerically identical at n=4000. Recorded that the Janson p_n scaling (D-004) is now applied in the test (validation re-confirmed 4/4) and is adopted for theorem validity / clean scaling exponents, not a finite-n ratio gain. §10 drops the now-done p-scaling action and promotes the Wk-2 μ-sweep. Live-only; no frozen edits; version unchanged at v1.4.
