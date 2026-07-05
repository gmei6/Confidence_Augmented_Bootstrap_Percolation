# Task N Phase 2 (Q4) Report — Tilt Monotonicity at $n = 10000$ + $\tau=3.5$ Gate (C-Q4(i))

**Session:** S-048 (2026-07-05, S-047 overnight batch, sandbox copy). **Conjecture under test:** C-Q4(i) tilt monotonicity — at fixed $\bar\mu$ and $\tau$, the empirical critical seed $a_c^{emp}$ is strictly decreasing in the tilt $\gamma$. Phase 2 turns the S-046 one-$n$ (Phase 1b, $n=4000$) result into a scaling statement and gates it by tail heaviness.

## Setup

- Configuration model $\tau=2.5$, $d_{\min}=2$, $n=10000$, $r=2$, $\kappa=50$, $\theta=0.5$; $\gamma \in \{-1, 0, +1\}$ paired on `base_seed=42` (identical SeedSequence spawn order → paired trials), $\bar\mu \in \{0.0,\dots,0.7\}$, seed grid $a \in \{2..48\}$ (multiples), 200 trials/cell.
- Plus one $\tau=3.5$, $\gamma=0$ slice on the identical grid (the tail gate).
- Four stamped raws `results/q4_phase2_n10000_*_raw.json` (commit `fb0ac42`); analysis via the Task N machinery with `PHASE1B_CONFIGS` repointed at the three `configs/q4_phase2_n10000_gamma*.json` (`scripts/analyze_task_n_phase2.py`, per the S-047 handoff).

## Findings

- **The S-046 ordering REPRODUCES at $n=10000$: the cap-free pair $\gamma=-1\to0$ PASSES 7/7 $\bar\mu$ rows** ($a_c^{emp}$ strictly decreasing at every $\bar\mu \in \{0.1..0.7\}$, zero significant paired violations). C-Q4(i) now holds at two system sizes ($n=4000$ S-046, $n=10000$ here) — a scaling statement, no longer a one-$n$ observation.
- **The $\gamma=0\to+1$ cap caveat PERSISTS:** `cap_diagnostics` realized $\bar\mu$ (checked first, per lessons) shows the $\gamma=+1$ slice cap-affected at every $\bar\mu \ge 0.1$ (shortfall 7% at $\bar\mu=0.1$ → 28% at $\bar\mu=0.7$). 0 cap-free rows; the 9 significant reversals all sit in cap-affected cells — artifact-suspect, not refutations. The pair remains untestable until the post-cap renormalization fix (next-actions item).
- **$\tau=3.5$ gate is total on this grid:** zero systemic outcomes in all 16,000 trials ($a$ up to 48, all $\bar\mu$), vs $\tau=2.5$ thresholds $a_c^{emp} \approx 3.9$–11.0. Tail heaviness gates the entire small-seed ignition regime at $n=10000$, consistent with (and stronger than) the bounded-seed C-Q4(iii) gate result.
- $a_c^{emp}(\bar\mu)$ decreases in $\bar\mu$ for every $\gamma$ (10.98 at $\bar\mu=0$ → ~3.9–4.7 at $\bar\mu=0.7$), as at $n=4000$.

## Artifacts

- Raw: `results/q4_phase2_n10000_{gammaneg1,gamma0,gammapos1,tau35_gamma0}_raw.json` (runner-stamped, base_seed 42).
- Analysis: `results/processed/task_n_phase2_n10000_analysis.json` (`scripts/analyze_task_n_phase2.py`).
- Figure: `results/figures/q4_tilt_monotonicity_r2_n10000.png` (`scripts/plot_task_n_phase2.py`).
