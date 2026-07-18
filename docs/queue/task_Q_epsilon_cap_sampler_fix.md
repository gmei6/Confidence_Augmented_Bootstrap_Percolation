# Task Q — Make `sample_degree_dependent_fears` cap-aware (Q4 Phase 2 unblock)

**Queued:** 2026-07-17. **Conjecture under test:** C-Q4(ii) — size-biased collapse of the
degree-fear tilt — plus completing the γ=0→+1 leg of C-Q4(i) tilt monotonicity.

**Autonomous-safe: NO.** This touches `src/twocascade/graphs.py`, a shared simulation module
(not the frozen oracle `reference.py`, but still core engine code). Per `AGENTS.md` §III
("Propose, don't write") and the `docs/queue/README.md` baseline-isolation rule, any change
here must go through `/research-cycle` in **New Worktree Mode**, with the diff presented for
Gary's approval before it touches disk — it must not be applied unattended. Queued as a fully
scoped proposal so a future session can execute the Plan→Execute→Verify cycle without needing
to re-derive the problem, not as something to run blind overnight.

## Problem

`sample_degree_dependent_fears` (`src/twocascade/graphs.py:47-97`) computes
`mu(d) = min(mu_bar * (d/⟨D⟩)^gamma / Z_n(gamma), 1 - epsilon)`, where `Z_n` is the mean of
`(d_i/⟨D⟩)^gamma` over **all** nodes, including ones whose `mu(d)` will end up clipped by the
`1-epsilon` cap. For γ>0 at τ=2.5 (heavy tail), high-degree nodes push `Z_n` up, and the clip
then compresses the realized population mean fear below `mu_bar` — confirmed at every
`mu_bar ≥ 0.1` in both the n=4000 (S-046) and n=10000 (S-048) runs, shortfall 7%→28%
(`docs/queue/reports/task_n_phase2_report.md`). Every γ=0→+1 reversal test to date is
cap-affected and therefore artifact-suspect, not a real refutation or confirmation.

## Proposed fix (design sketch, not implementation)

Renormalize `Z_n` using only the **uncapped** nodes, iteratively:

1. Compute `mu_d` as today; find the cap mask (`mu_d > 1-epsilon`).
2. Recompute `Z_n` as the mean of `(d_i/⟨D⟩)^gamma` over only the *uncapped* nodes, rescale
   the uncapped nodes' `mu_d` against this narrower `Z_n` so the **population mean** (capped
   nodes pinned at `1-epsilon`, uncapped nodes rescaled) lands back on `mu_bar`.
3. Repeat until the cap mask stabilizes (a node just pulled under the cap by step 2 could still
   need reclassifying) — this is the standard "iterative water-filling" fix for a mean-preserving
   cap, typically converges in a handful of iterations for realistic degree tails.
4. `stats["realized_mu_bar"]` should land within numerical tolerance of `mu_bar` for every
   γ>0 cell that isn't degenerately cap-saturated (e.g. `mu_bar` so high that even uncapped
   nodes can't absorb the redistribution — flag that edge case rather than silently returning
   a still-short mean).

## Scope after the fix lands

- Re-run the γ=0→+1 reversal pair (the mirror of `configs/q4_phase2_n10000_gamma0.json` /
  `q4_phase2_n10000_gammapos1.json`) — same grid, same `base_seed=42` paired-trial design.
- Re-test C-Q4(ii) (size-biased collapse), which was gated on the same sampler defect.
- Cross-validate: confirm `stats["cap_hits"]` drops to ~0 for the same cells that showed 7–28%
  shortfall before, and that `realized_mu_bar` tracks `mu_bar` within tolerance.

## Reports / context

`docs/queue/reports/task_n_phase2_report.md`, `okf/next-actions.md` item #4 (superseded by
this task file — see the `okf/next-actions.md` update in S-051).
