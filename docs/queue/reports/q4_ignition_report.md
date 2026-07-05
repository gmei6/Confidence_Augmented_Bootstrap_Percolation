# Q4 Ignition Gates Report — Bounded-Seed Tail Gating (C-Q4(iii))

**Session:** S-048 (2026-07-05, S-047 overnight batch, sandbox copy). **Conjecture under test:** C-Q4 clause (iii) — the tail-gating clause: on a power-law configuration model a *bounded* seed ($a = r = 2$) ignites systemic cascades when the tail is heavy ($\tau = 2.5 < 3$), and must NOT ignite when the tail is light ($\tau = 3.5 > 3$).

## Setup

- Configuration model, $d_{\min}=2$, $r=2$, $\kappa=50$, $\theta=0.5$, window 5 × weights 0.2, $\gamma=0$ (untilted fears).
- $\tau \in \{2.5, 3.5\}$ × $n \in \{4000, 10000, 20000\}$ × $\bar\mu \in \{0.0, 0.4\}$, seed $a=2$, 500 trials/cell, `base_seed=42`. Six stamped raws `results/q4_ignition_{tau25,tau35}_n{...}_raw.json` (commit `fb0ac42`).

## Findings

**Gate HOLDS.** $P(\text{systemic})$ per cell (`twocascade.analysis.analyze_sweep`):

| series | $n=4000$ | $n=10000$ | $n=20000$ | direction |
|---|---|---|---|---|
| $\tau=2.5$, $\mu=0.0$ | 0.038 | 0.024 | 0.028 | ~flat (non-monotone) |
| $\tau=2.5$, $\mu=0.4$ | 0.134 | 0.116 | 0.062 | decreasing |
| $\tau=3.5$, $\mu=0.0$ | 0.000 | 0.000 | 0.000 | all-zero |
| $\tau=3.5$, $\mu=0.4$ | 0.000 | 0.000 | 0.000 | all-zero |

- **$\tau=3.5$ never ignites:** 0 systemic outcomes in 3000 trials (Wilson 95% upper bound $\approx 0.008$ per cell). The light-tail side of the gate is clean.
- **$\tau=2.5$ ignites at a bounded seed** in every cell — the dichotomy vs $\tau=3.5$ is stark and is the gate itself.
- **Caveat for morning triage (n-direction):** the handoff's expected shape was "$\tau=2.5$ ignition stays $\Theta(1)$ or grows with $n$". At $\mu=0$ the branch is consistent with $\Theta(1)$ (~0.03 flat across a 5× range of $n$), but at $\bar\mu=0.4$ it *decreases* (0.134 → 0.062). Three $n$ points cannot separate slow decay from a positive limit; if the $\Theta(1)$ claim at $\bar\mu>0$ matters for the C-Q4 readout, extend the $n$-grid before citing it.

## Artifacts

- Raw: `results/q4_ignition_{tau25,tau35}_n{4000,10000,20000}_raw.json` (runner-stamped, base_seed 42).
- Analysis: `results/processed/q4_ignition_analysis.json` (`scripts/analyze_q4_ignition.py`, Wilson intervals + per-series directions).
