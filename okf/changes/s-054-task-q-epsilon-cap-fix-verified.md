---
type: Session Change
title: "S-054: Task Q — epsilon-cap sampler fix, verified"
description: "Fixed sample_degree_dependent_fears's Z_n normalization shortfall via iterative water-filling; cleared 4 reviewer rounds, 1 critic round, and AUDIT PASS. Not yet merged."
mutability: append-only
timestamp: 2026-07-18
tags: [q4, bugfix, sampler, verify-gate]
---

# S-054: Task Q — epsilon-cap sampler fix, verified

Fixed the shortfall bug in `sample_degree_dependent_fears` (`src/twocascade/graphs.py`) flagged
by `docs/queue/task_Q_epsilon_cap_sampler_fix.md`: the single-pass `Z_n` normalization included
soon-to-be-capped nodes, silently undershooting `mu_bar` by 7-28% for gamma>0 on heavy-tailed
(tau=2.5) degree sequences — every prior gamma=0→+1 reversal test was cap-affected and
artifact-suspect. Replaced with iterative water-filling (capped nodes pinned at `1-epsilon`,
uncapped nodes' weights rescaled each round so the population mean lands back on `mu_bar`;
capped-set membership is provably monotone non-decreasing in the rescale factor, giving a
proven `n+1`-iteration bound rather than a guessed one).

Developed in worktree `../tc-work-taskq` (branch `task-q-epsilon-cap-fix`), per baseline
isolation. Cleared `/verify`: **4 reviewer rounds** (each found and fixed a real issue — a
non-finite-weight node mishandling that inverted degree-fear direction for isolated nodes
under gamma<0; a `degenerate` flag conflating two guarantees, split into `infeasible` vs.
`non_finite_weight_count`; a `mu_bar==0.0` stats/output contract mismatch; two cosmetic nits),
**1 critic round** (adversarial stress across extreme n/gamma/kappa, RNG determinism, and
multiprocessing seeding safety — PASS, one production-unreachable `n=0` gap fixed), and
**AUDIT PASS** (worktree isolation, oracle protection, results integrity, and diff-fidelity all
independently verified). No C++ analog of this function exists anywhere in the repo (confirmed
via grep) — §5.4 cross-language parity is correctly out of scope.

**Not yet merged into `antigravity`** — merge is Gary's call. Scope explicitly deferred (per
the task file's own "after fix lands" section, out of scope for a code-fix `/verify` pass):
re-running the γ=0→+1 reversal pair (`configs/q4_phase2_n10000_gamma{0,pos1}.json`) and
re-testing C-Q4(ii) size-biased collapse with the fixed sampler.
