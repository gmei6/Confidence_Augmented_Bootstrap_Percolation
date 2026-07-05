# Task O Follow-up (Q5) Simulation Report — Duration Dichotomy $n$-Sweep (C-Q5(ii))

**Session:** S-048 (2026-07-05, S-047 overnight batch, sandbox copy). **Conjecture under test:** C-Q5 clause (ii) — the deferred duration-dichotomy clause from the S-046 Task O readout. With (i) and (iii) already read out, this completes the C-Q5 record for the July-15 advisor email.

## Setup

- Hard RGG on the unit torus, $\bar D = 2\log n$, $r=2$, $\kappa=50$, $\theta=0.5$, window 5 × weights 0.2, disc seeding ($a=30$).
- $n \in \{4000, 8000, 16000, 32000\}$; fields: global vs $\ell = r_n$ local at $\bar\mu \in \{0.2, 0.4\}$, plus the shared $\mu=0$ control (field type provably irrelevant at $\mu=0$).
- 20 cells × 30 trials, `base_seed=2027`, durations only (D-014 JSON-bloat rule). Runner: `scripts/run_task_o_duration.py` (stamped, commit `fb0ac42`).

## Findings

**C-Q5(ii) SUPPORTED.** Ballistic ratio $T_\theta / \sqrt{n/\log n}$, mean over systemic trials (all 600 trials went systemic):

| $n$ | control $\mu=0$ | global $\bar\mu=0.2$ | global $\bar\mu=0.4$ | local $\ell=r_n$ $\bar\mu=0.2$ | local $\ell=r_n$ $\bar\mu=0.4$ |
|---|---|---|---|---|---|
| 4000  | 0.685 | 0.461 | 0.389 | 0.686 | 0.678 |
| 8000  | 0.682 | 0.393 | 0.325 | 0.679 | 0.680 |
| 16000 | 0.676 | 0.325 | 0.270 | 0.674 | 0.675 |
| 32000 | 0.669 | 0.273 | 0.219 | 0.666 | 0.667 |

- **Local field is ballistic:** the $\ell=r_n$ ratio is flat and indistinguishable from the field-free control — log-ratio-vs-log-$n$ slope $-0.014/-0.011$ vs the control's $-0.011$ (paired drift; $t$ vs control $=-1.2/+0.3$). The control's own small negative slope is the finite-size drift of the ballistic constant, which is why regimes are judged **against the control slope**, not against zero.
- **Global field is sub-ballistic:** ratio falls monotonically (slope $-0.255/-0.280$, $t$ vs control $=-46/-48$) — secondary nucleation short-circuits the front, exactly the C-Q5(ii) prediction. At $n=32000$, global $T_\theta \approx 12$–15 rounds vs the local/control $\approx 37$.
- Figure deferred (optional per the handoff); the table and fits are in the processed artifact.

## Artifacts

- Raw: `results/q5_duration_raw.json` (`scripts/run_task_o_duration.py`, stamped: git_commit `fb0ac42`, base_seed 2027).
- Analysis: `results/processed/task_o_duration_analysis.json` (`scripts/analyze_task_o_duration.py`).
