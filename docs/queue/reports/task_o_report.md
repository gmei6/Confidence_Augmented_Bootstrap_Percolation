# Task O (Q5) Simulation Report — Localized Fear: Nucleation Law & Coverage Entropy

**Session:** S-046 (2026-07-04). **Conjecture under test:** C-Q5 clauses (i) nucleation law and (iii) homogenization. Clause (ii) duration dichotomy is **deferred** (needs an $n$-sweep of $T_\theta(n)$ exponents; single $n$ here — flagged for the C++/PACE phase).

## Setup

- Hard RGG on the unit torus, $\bar D = 2\log n\approx16.6$ ($n=4000$), $r=2$, $\kappa=50$, $\theta=0.5$, window 5 × weights 0.2.
- Disc seeding (localized droplet, $a=30$; goes systemic 5/5 at $\mu=0$ in pilot).
- Fields: global (`fear_adjacency=None`), local $\ell/r_n\in\{1,4\}$. ($\ell/r_n=16$ omitted at $n=4000$: $16r_n=0.58>$ half-torus, indistinguishable from global.)
- 12 cells × 40 trials, `base_seed=2026`, per-round locality statistics recorded up to cumulative fraction 0.75.

## Engine changes (validated, additive)

`run_cascade_local_fear` gained: (1) `round_log` out-parameter (per-round new-failure sets, inert by default); (2) `fear_adjacency=None` global-field fast path (provably identical to a full-torus ball); (3) per-round scattered fear counts replacing the per-node ball scan (exact algebraic identity over the symmetric fear adjacency, ~40× faster). Oracle `reference.py` untouched. New tests `tests/test_q5_local_fear.py` (5/5): full-torus ≡ global fast path (same-seed exact match), $\mu=0$ exact match vs the reference oracle (prong A analogue), round-log consistency, instrumentation inertness, scatter ≡ brute-force scan.

## Findings

- **C-Q5(iii) homogenization: SUPPORTED (relative form).** At the $\theta$-crossing, global-field entropy rises from the $\mu=0$ control (0.687) to 0.85/0.89/**0.91** at $\bar\mu=0.2/0.4/0.6$ (crossing the pre-registered 0.9 at $\bar\mu=0.6$); the $\ell=r_n$ local field stays **pinned to the control** (max elevation 0.004); $\ell=4r_n$ rises mildly (≤0.045). Pre-registration note: the $\mu=0$ control itself sits at 0.687 > the pre-registered 0.6 local ceiling, so absolute thresholds were re-baselined against the control — the sanity-tuning the scoping doc pre-committed to.
- **Locality preservation is total at $\ell=r_n$:** zero remote nuclei in 160 trials (vs 195–628 per cell for the global field).
- **C-Q5(i) nucleation law: NOT SUPPORTED as pre-registered (honest negative).** Global-field log-log slope of $\mathbb E[N_{\mathrm{nuc}}]$ vs $g_t$ is 1.21/1.22/1.48 at $\bar\mu=0.2/0.4/0.6$ — a constant leak, not the predicted $g^{r}=g^2$ barrier. A mechanism-faithful refit against the windowed fear drive $\varphi_t$ (what the engine actually multiplies fear by) gives 0.96/1.36/1.35 — still ≪ 2. Caveat for follow-up: the same-round cluster counter misses cross-round pair ignition (`failed_neighbor_count` is cumulative, so two lone remote failures in the same ball in *different* rounds also ignite at $r=2$), and front-adjacent remotes may dominate counts; a remote-ignited-growth tracker is the cleaner instrument before treating the refutation as final.

## Artifacts

- Raw: `results/q5_localized_fear_raw.json` (`scripts/run_task_o.py`, stamped).
- Analysis: `results/processed/task_o_locality_analysis.json` (`scripts/analyze_task_o.py`).
- Figure: `results/figures/q5_locality_r2.png` (`scripts/plot_task_o.py`).
