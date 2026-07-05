# Task N (Q4) Analysis Report — C-Q4(i) Tilt Monotonicity

**Session:** S-046 (2026-07-04). **Conjecture under test:** C-Q4(i) — at fixed $\bar\mu\in(0,1)$ and fixed $\tau$, the empirical critical seed $a_c^{\mathrm{emp}}$ is strictly decreasing in the fear–degree tilt $\gamma$.

## Setup

- Erased configuration model, $\tau=2.5$, $d_{\min}=2$, $n=4000$, $r=2$, $\kappa=50$, $\theta=0.5$, window 5 × weights 0.2.
- Three paired tilt slices $\gamma\in\{-1,0,+1\}$, shared `base_seed=42` (identical `SeedSequence` spawn order ⇒ trial $k$ of cell $(i,j)$ has the identical degree/pairing streams across slices — paired trials on shared graphs, per the scoping doc §7).
- Python engine via `twocascade.runner.run_sweep`; raw outputs runner-stamped.

## Finding 1 — Phase 1 grid was entirely supercritical (methodological)

The S-044 Phase 1 seed grid (multiples 1.0–3.0 of the **G(n,p) Janson** $a_c\approx260$) gives $P(\text{systemic})\approx1$ in **all 40 cells of all three $\gamma$ slices**: the Janson seed scaling does not transfer to the $\tau=2.5$ heavy-tailed CM, whose ignition transition sits at $a\in[2,32]$ — two orders below the grid floor. (Consistent with C-Q4(iii)'s tail-gated small-seed ignition.) Phase 1b re-swept $a\in\{2,3,4,6,8,12,16,24,32\}$ at 200 trials/cell.

## Finding 2 — C-Q4(i) readout (Phase 1b)

- **Clean pair $\gamma=-1\to0$ (zero cap hits, equal total fear exact): PASS 7/7** $\bar\mu$ rows with $a_c^{\mathrm{emp}}$ strictly decreasing; 19 paired cells significantly more systemic at higher $\gamma$ ($z>2$), 0 significant violations.
- **Pair $\gamma=0\to+1$: not cleanly testable on this grid.** At $\tau=2.5$ the $\varepsilon$-cap fires for $\gamma=+1$ at every $\bar\mu\ge0.1$ (realized $\bar\mu$ shortfall 6%→28%; at nominal $\bar\mu=0.7$ the realized mean fear is 0.504 with 475/4000 nodes capped). All 8 significant "violations" ($\gamma=+1$ less systemic) sit at $\bar\mu\in\{0.6,0.7\}$ — the equal-total-fear premise is broken there, so they are artifact-suspect, not refutations (this is exactly the scoping doc §7 pre-registered early-warning). Notably $\gamma=+1$ still *wins* at $\bar\mu\le0.3$ despite carrying less realized fear — conservative support.

## Cross-validation & tests

- `tests/test_q4_config_model.py`, `tests/test_q4_prong_a.py`: **4/4 pass** (Prong A exercised the real C++ binary; exact $\mu=0$ failed-fraction match on a shared CM graph).
- Test-semantics note: `test_q4_prong_a.py` was broken as committed (called the oracle without the required `record_history` arg — case (a): the test was wrong; corrected minimally; no engine change involved).

## Artifacts

- Raw: `results/q4_phase1_gamma0_raw.json`, `results/q4_phase1_gamma_neg1_raw.json`, `results/q4_phase1b_gamma{neg1,0,pos1}_raw.json` (runner-stamped).
- Configs: `configs/q4_phase1_gamma0.json`, `configs/q4_phase1_gamma_neg1.json`, `configs/q4_phase1b_gamma{neg1,0,pos1}.json`.
- Analysis: `results/processed/task_n_tilt_analysis.json` (`scripts/analyze_task_n.py`).
- Figure: `results/figures/q4_tilt_monotonicity_r2.png` (`scripts/plot_task_n.py`).

## Follow-up

Phase 2 needs a cap-aware sampler before $\gamma>0$ is testable at moderate-to-high $\bar\mu$: renormalize post-cap (iterate $Z_n$ with the cap applied) or restrict to $\bar\mu$ where cap hits are nil; then re-test the (0, +1) pair and clause (ii) size-biased collapse.
