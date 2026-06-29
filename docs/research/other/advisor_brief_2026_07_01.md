# Advisor Briefing: Two-Channel Bootstrap Percolation
**Date:** July 1, 2026

**Author:** Gary Mei

**Advisor:** Prof. Souvik Dhara

---

## 1. Status Against North Star and Roadmap

The project's goal — a clean two-channel cascade (Janson solvency + self-referential fear
field) characterized by a (r,μ) phase diagram with a validated mean-field threshold — is on
track through Week 5. Three additions since the June 16 brief:

1. **Task B (θ/κ robustness) — complete.** The cascade boundary is stable across
   θ ∈ [0.2, 0.8] (shift < 0.05 in μ) and responds weakly to fear heterogeneity κ
   across {2, 10, 50, 200}, consistent with σ entering at second order (§3.5).

2. **Tier 1 mathematical result (D-025).** Using a leave-m-out construction, we
   established exact conditional independence of activation times Y'_i given the
   leave-m-out fear field at finite n. This sharpens the Asymptotic Decoupling
   Conjecture into two sub-questions: fear-field concentration and leave-out field
   equivalence. The empirical pairwise test (n ∈ {1000,…,8000}) found pairwise
   covariances consistent with zero but variance-ratio excess not clearly vanishing;
   the conjecture remains open.

3. **Interactive teaching visualization — live.** A GitHub Pages site mirrors the
   research talk with a FIFO step-trace walkthrough: Part A (μ=0, Janson baseline,
   seed={1,4}) and Part B (μ=0.85, fear-driven systemic collapse from a single seed).
   URL: https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/

We are now at the Wk 5/6 boundary, ready to begin the finite-size analysis (Wk 6–7)
pending your input on scope.

---

## 2. Core Empirical Results

### 2.1 Phase Diagrams
The (r,μ) phase diagrams for r ∈ {2,3,4} confirm the two-channel structure: as μ
increases, the systemic-event boundary shifts toward smaller seeds, and the fear channel
visibly amplifies cascades. The analytical threshold $a_c(\mu) = a_c(0)(1-\mu)^{r/(r-1)}$
overlays the empirical boundary.

Figures: results/figures/wk3_4_phase_diagram_overlay_r{2,3,4}.png

### 2.2 Scaling Validation of $a_c(\mu) = a_c(0)(1-\mu)^{r/(r-1)}$
Empirical ratio $a_\text{emp}(\mu)/a_\text{emp}(0)$ vs. theoretical $(1-\mu)^{r/(r-1)}$
at N=1000, np=8:

| r | MAE  | Max deviation | At μ | Status |
|---|------|---------------|------|--------|
| 3 | 2.6% | 0.069         | 0.80 | ✓ tight fit |
| 4 | 2.0% | 0.048         | 0.85 | ✓ tight fit |
| 2 | 11.4%| 0.189         | 0.65 | systematic positive bias (see §2.3) |

Figures: results/figures/wk3_4_scaling_validation_r{2,3,4}.png

### 2.3 r=2 Systematic Bias
The r=2 positive bias is present from low μ (diff=+0.071 at μ=0.15, $a_\text{emp}$≈9.2)
and peaks in mid-range (μ=0.65, $a_\text{emp}$≈3.6). Attribution: because $a_c(0)$ is
small for r=2 (7.81 at N=1000), the finite-size inflation factor K(μ,n) becomes
μ-dependent as the threshold drops, breaking the K-cancellation that makes r=3/4 tight.
This is a finite-size convergence issue, not a model failure. Convergence check at
N=5000/10000 is the proposed next step (§4).

---

## 3. Open Questions for This Meeting

### Q1 — Scope of the Asymptotic Decoupling Conjecture
The Tier 1 leave-m-out result (D-025) establishes exact conditional i.i.d. structure at
finite n. The Tier 2 asymptotic conjecture reduces to: (a) fear-field concentration
(does $g_t$ concentrate around its mean?), and (b) leave-out field equivalence (does
the leave-m-out field converge to the full field as n→∞?).

**Our lean:** Scope the conjecture as an open problem with the Tier 1 structure theorem
as the rigorous anchor. A full proof of concentration would need martingale bounds on
the fear field — tractable given $R_\text{fear} \approx \mu < 1$, but a substantial
investment for the remaining timeline.

**Decision from you:** Is this framing sufficient for the write-up, or should we
prioritize the concentration proof?

### Q2 — Network Structure: G(n,p) vs. Configuration Model
Current results are on G(n,p) in the Janson regime. A configuration model with
power-law degrees would make degree heterogeneity and targeted seeding meaningful,
and connects to your critical percolation work (Dhara–van der Hofstad–van Leeuwaarden,
2021).

**Our lean:** Complete Wk 6–7 finite-size analysis on G(n,p) first (it directly
supports the write-up), then introduce the configuration model as a Week 8 stretch
if time allows.

**Decision from you:** Is the G(n,p) finite-size result sufficient for the write-up
scope, or is the configuration model extension important enough to prioritize?

### Q3 — Critical-Window Width Exponent ν
Under the rescaled Janson mapping, transition-width scaling predicts ν_abs = 1.25 and
ν_rel = 5.0 for r=2, both μ-invariant (away from the crossover boundary). This is
cheap to test: 4–5 values of n, curve fitting to the width vs. n log-log plot.

**Decision from you:** Is this framing of interest for the final write-up? Should we
also probe cascade size distribution at the boundary (n^{2/3}-type scaling)?

---

## 4. Compute and Logistics

- **r=2 convergence check (Wk 6):** Sweeps at N ∈ {1000, 2000, 3000, 5000} with
  D-004 p-scaling (β fixed at N_ref=1000). Manageable on laptop through N=3000;
  N=5000 benefits from PACE.
- **PACE access:** The critical-window sweeps ($10^6$–$10^7$ realizations) exceed
  laptop capacity. Would appreciate your input on the access request process.
- **Write-up scope:** Wk 10 target. Guidance appreciated on venue (SURS poster /
  short research note / arXiv preprint).
