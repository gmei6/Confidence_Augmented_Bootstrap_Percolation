---
type: Concept
title: "§10 — Next Actions"
description: "Live list of the next few concrete steps; overwritten each session."
mutability: live
---

# §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

1. **Morning triage of the S-047 batch (done in sandbox, S-048):** the batch ran 5/5 OK — reconcile this sandbox copy's results/OKF into the primary checkout (Gary). Two flags for triage: (a) the τ=2.5 ignition branch at $\bar\mu=0.4$ *decreases* with $n$ (0.134→0.062) — extend the $n$-grid before citing $\Theta(1)$ at $\bar\mu>0$; (b) `plot_fear_field_concentration` in `src/twocascade/plotting.py` is missing `savefig`/`close` (Task E's relvar figure silently never regenerates) — one-line fix, but it touches `src/`, so it was out of scope overnight.
2. **Email Prof. Dhara before 2026-07-15** — the C-Q5 readout is now COMPLETE for the email: (i) honest negative, (ii) duration dichotomy SUPPORTED (S-048 n-sweep, `task_o_duration_report.md`), (iii) homogenization supported. Also in hand: Q6 super-hub negative, Q4 tilt monotonicity at two system sizes + the τ=3.5 total gate, tightened ν (μ=0.3: 4.54±0.26).
3. **Review and commit the S-046/S-047 primary-checkout working tree** (unchanged item — that tree's work is separate from this sandbox branch).
4. **Q4 Phase 2 sampler fix:** make `sample_degree_dependent_fears` cap-aware (renormalize $Z_n$ post-cap) so the γ>0 tilt is testable — the S-048 n=10000 run reconfirms every γ=+1 cell at $\bar\mu\ge0.1$ is cap-affected (shortfall up to 28%). Then re-test the (0,+1) pair and C-Q4(ii).
5. **Q5 follow-up:** remote-ignited-growth tracker (cross-round pair ignition) before treating the C-Q5(i) refutation as final.
6. TODO (machine setup, not research): install the assistant tooling Gary deferred on 2026-07-04 — `npm install -g gh-axi && gh-axi setup hooks`, `npm install -g tasks-axi`, `npm install -g chrome-devtools-axi && chrome-devtools-axi setup hooks`. Environment note: run simulations with `arch -arm64 python3` (Rosetta/numpy mismatch).
7. **Study the Math (Gary):** Deep dive into the mathematical formulations behind the modified fear factors, the Geometric Local fields, and the Power-Law (Configuration) models to fully grasp how they integrate mechanically.
8. **Prerequisite reading — random graphs & complex networks (Gary; gates #7).** Read
   these *before* the Study-the-Math explanation, in order. Each tier grounds a piece of the
   power-law / geometric machinery actually coded in `src/twocascade/`.
   - **Tier 0 — Probability refresher (skip if fluent):** expectation/variance, moments &
     tail behavior, conditional expectation, and **inverse-transform sampling**; the
     Bernoulli, Binomial, Poisson, **Beta**, **Geometric**, and **Pareto** distributions.
     (Beta → individual fear $f_i$; Geometric → the Task-H survival clock; Pareto →
     `girg.sample_powerlaw_weights`.)
   - **Tier 1 — Erdős–Rényi $G(n,p)$ + branching processes:** van der Hofstad, *Random
     Graphs and Complex Networks* Vol 1, Ch. 3–5 (free PDF). Poisson degree, giant
     component & the phase transition; subcritical/critical/supercritical branching,
     extinction probability, mean offspring — this is what makes $R_{\text{fear}}\approx\mu<1$
     rigorous (the subcritical-amplifier claim, §3.3).
   - **Tier 2 — Power laws & the configuration model:** van der Hofstad Vol 1, Ch. 1
     (power-law tails & moments) and Ch. 7 (configuration model, stub matching, erased vs.
     simple, Molloy–Reed criterion); Barabási, *Network Science*, Ch. 4 (free online). Nail
     down why $\tau>2$ ⇒ finite mean and $\tau>3$ ⇒ finite variance, so $\tau=2.5$ =
     finite-mean/infinite-variance hubs — the mechanism behind the $\tau=2.5$-ignites /
     $\tau=3.5$-gate result. Maps to `graphs.py`.
   - **Tier 3 — Bootstrap percolation / threshold cascades:** Janson–Łuczak–Turova–Vallier
     (2012), *Bootstrap percolation on $G(n,p)$* — the JŁTV baseline this project extends;
     Watts (2002), *A simple model of global cascades*; Amini–Cont–Minca for the
     config-model threshold. Grounds the absolute-$r$ solvency channel and the
     $(np^r)^{-1/(r-1)}$ threshold form (§3.2).
   - **Tier 4 — Spatial / geometric graphs:** Penrose, *Random Geometric Graphs* (RGG on the
     torus, connection radius, degree); Bringmann–Keusch–Lengler, *Geometric Inhomogeneous
     Random Graphs* (GIRG — weights × distance kernel). Grounds the torus, radius $r_n$, the
     local fear ball $B(x_i,\ell)$, and the GIRG connection probability. Maps to `geometry.py`
     / `girg.py`.
