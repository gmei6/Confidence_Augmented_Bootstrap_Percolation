---
type: Cache
title: "van der Hofstad — Random Graphs and Complex Networks, Vol. 1: Tier 1–2 reading map"
description: "Verified PDF page map (Tiers 1–2, Ch. 1/3/4/5/7) cross-referenced to src/twocascade/ code; generated 2026-07-08 for okf/next-actions.md #7-#8."
mutability: live
resource: "file:///Users/garymei/Downloads/Summer 2026/Research/Papers to Read/RANDOM GRAPHS AND COMPLEX NETWORKS.pdf"
tags: [reading-guide, branching-processes, configuration-model, power-law]
---

# van der Hofstad — Random Graphs and Complex Networks, Vol. 1: Tier 1–2 reading map

Companion to `references/van-der-hofstad-rgcn.md` (the §13 citation stub). This file holds the
derived content: section-level page numbers verified against Gary's own PDF, plus exact code
cross-references, tied to `okf/next-actions.md` #7 (Study the Math) and #8 (prerequisite reading,
Tiers 1–2).

**Page offset (verified against this PDF):** PDF page = printed page + 18 (printed p.1 = PDF p.19).

## Tier 1 — Erdős–Rényi + branching processes (Ch. 3–5)

### Chapter 3 — Branching Processes (printed 85–111 / PDF 103–129)

| § | Title | PDF p. | Why it matters |
|---|---|---|---|
| 3.1 | Survival versus Extinction | 105 | Extinction fixed point `q = G(q)`; the base case for "subcritical ⇒ dies out." |
| 3.5 | Hitting-Time Theorem & the Total Progeny | 115 | Derives `E[total progeny] = 1/(1-μ)` for subcritical GW processes — this is the literal proof of the "bounded gain ≈ 1/(1-μ)" claimed in `okf/model/forks.md` F1 (D-005/D-006). |
| 3.6 | Properties of Poisson Branching Processes | 117 | Survival probability vs. mean offspring — grounds `okf/model/network-and-channels.md` §3.3's "`R_fear ≈ μ < 1`, fear is a subcritical amplifier"; the Bernoulli draw it describes is `reference.py:161-166`. |

### Chapter 4 — Phase Transition for the Erdős–Rényi Random Graph (printed 115–147 / PDF 133–165)

| § | Title | PDF p. | Why it matters |
|---|---|---|---|
| 4.1 | Introduction | 135 | Formal `G(n,p)` + monotonicity coupling — the object built by `sample_gnp_adjacency` (`reference.py:212`). |
| 4.2 | Comparisons to Branching Processes | 138 | Couples ER-cluster exploration to a Poisson branching process — the rigorous backbone under §3.2's "Janson local rule" (Channel 1). |
| 4.3 | The Subcritical Regime | 140 | Largest component `O(log n)` when `np<1`. |
| 4.4 | The Supercritical Regime | 147 | LLN for the giant component when `np>1` — the `r=1` special case that `model.py:janson_t_c` (`((r-1)!/(n·p^r))^(1/(r-1))`) generalizes to `r≥2` (Tier 3, JŁTV). |
| 4.5 | CLT for the Giant Component | 155 | Optional first pass — fluctuation-level, not needed for the threshold-level claims in §3.2–§3.3. |

### Chapter 5 — Erdős–Rényi Random Graph Revisited (printed 149–172 / PDF 167–190) — lighter pass

5.1–5.3 (critical behavior, connectivity threshold), PDF 167–181: background for why small-`n`
finite-size effects (the τ=2.5 non-monotonicity in `okf/next-actions.md` #1) can look strange before
the asymptotic regime kicks in. Not required to follow §3.2–§3.3.

## Tier 2 — Power laws & the configuration model (Ch. 1 §1.7, Ch. 7)

### Chapter 1, §1.7 — Tales of Tails (printed 40–44 / PDF 58–62)

| § | Title | PDF p. | Why it matters |
|---|---|---|---|
| 1.7.1 | Old Tales of Tails | 58 | Defines `N_k ∝ k^(-τ)`; τ>1 forced by `ΣN_k=n`. |
| 1.7.3 | Power laws, Their Estimation, and Criticism | 61 | τ>2 ⇒ finite mean; τ>3 ⇒ finite variance. τ=2.5 sits in finite-mean/infinite-variance — this is the mechanism behind the τ=2.5-ignites/τ=3.5-gates result in `okf/next-actions.md` #2. Also explains why `sample_powerlaw_degrees` (`graphs.py:3`) needs a hard `k_max` cap: for τ≤3 the theoretical variance is infinite. |

### Chapter 7 — Configuration Model (printed 213–250 / PDF 231–268)

| § | Title | PDF p. | Why it matters |
|---|---|---|---|
| 7.2 | Introduction to the Model | 233 | Stub-matching: `d_i` half-edges per vertex, paired uniformly at random. |
| 7.3 | Erased Configuration Model | 242 | Delete self-loops, collapse multi-edges. Matches `sample_configuration_model` (`graphs.py:20-44`) exactly — it drops `u==v` and stores neighbors in a Python `set`, which silently collapses multi-edges too. §7.4-7.5's discussion of how erasure distorts the realized degree sequence is the mechanism behind the cap-shortfall issue in `okf/next-actions.md` #4. |
| 7.6 | Configuration Model with I.I.D. Degrees | 257 | The two-step pipeline `sample_powerlaw_degrees` → `sample_configuration_model` in `graphs.py`. |

## Not covered by this volume

Tiers 0, 3, 4 (probability refresher; JŁTV bootstrap percolation; GIRG/spatial graphs) need separate
sources — see `okf/next-actions.md` #8.
