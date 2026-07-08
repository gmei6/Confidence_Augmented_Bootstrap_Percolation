---
type: Decision
title: "D-024: Cross-language parity thresholds by p-value"
description: "Cross-language parity thresholds moved to scale-invariant p-values (z-test and KS, p > 0.005); seed 12345."
mutability: append-only
timestamp: 2026-06-24
---

# D-024: Cross-language parity thresholds by p-value

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-024 | 2026-06-24 | Cross-language validation (§5.4 Prong B) now thresholds on a scale-invariant p-value (both z-test and KS require p > 0.005) instead of a fixed KS distance (< 0.05); standardize on seed 12345 for both engines. | The fixed KS-distance threshold sat below the two-sample 5% critical value (≈0.061 at N=1000/engine), giving ≈16% per-test false rejection (≈50% family-wise across the 4 KS cells) under a correct implementation — which had forced ad-hoc seed-shopping. A p-value threshold matching the z-test significance bounds the per-cell false-alarm rate to 0.5% while preserving power. §5.4 frozen spec text is unchanged (test implementation only). | §5.4 (test impl), §8, §11
