---
type: Decision
mutability: append-only
timestamp: 2026-06-02
---

# D-002: Fork F3: Beta(α,β) individual fear

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-002 | 2026-06-02 | Resolved fork F3: individual fear f_i ~ Beta(α,β) with α=μκ, β=(1−μ)κ, so E[f]=μ exactly; concentration κ tunes heterogeneity independently (var = μ(1−μ)/(κ+1)). Drop truncated-normal; keep two-point (immune/susceptible) as a robustness variant. | Truncated-normal's realized mean ≠ μ near 0/1 (nominal 0.1 → 0.164 at σ=0.15), silently mislabeling the sole sweep axis and the one quantity the dynamics depend on (§4: fear-failures ≈ μ·a_{t−1}). Beta is native to [0,1], sets the mean exactly, allows an independent κ-sweep for heterogeneity, and nests the degenerate limits (κ→∞ point mass, κ→0 two-point, μ=0 the Janson baseline). | §3.3, §3.5, §3.6, §7
