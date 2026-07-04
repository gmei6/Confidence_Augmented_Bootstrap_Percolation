# Task M Report: Q7 Scoping Doc — Optional Recovery/Healing Phase

**Date:** 2026-07-04 (fable overnight run) · **Research question affected:** Q7 (D-028 track 4, lower priority) — new `docs/research/` document; nothing revised (per AGENTS.md §III).

## What was produced

`docs/research/q7_recovery_phase_scoping.md`:

1. **Precise change specification, split into the fork the task wording hides:** R1 = SIR-immune (recovered banks immune and no longer counted by neighbors' thresholds; recommended first, matches D-028's "SIR-style") vs. R2 = SIS-resusceptible (re-eligible; second phase only). Counter semantics (decrement on recovery), fear-field semantics ($g_t$ keeps counting new failure events; recoveries never subtract), same-round simultaneity discipline, and $f_i$ persistence are all pinned down.
2. **Halting worked out, not glossed (DoD item):** R1 has a genuine absorbing state (empty failed set) with the §3.4 argument surviving intact, but forces the order parameter to change to the **ever-failed** fraction (plus peak prevalence as a new observable). R2's oscillation risk is named honestly: only absorbing state all-solvent, expected extinction time can be exponential (quasi-stationary endemic regime) — fully specified stopping rule (extinction OR hard horizon $T_{\max}=10n$ with trailing-window endemic classification), and a three-outcome phase structure that is the stated reason R2 is deferred.
3. **$R_\text{fear}<1$ under recovery explicitly derived (DoD item):** expected fear events $= g_t\sum_{i\in\text{solvent}}f_i \le \mu\,a_{t-1}$, with recovery pushing toward but never past the ceiling; R1's immunity makes it strictly smaller. Conclusion: fear alone can neither ignite nor sustain an endemic state in either variant; what recovery changes is the **solvency** race (cascade vs. healing), which is the physics the conjecture targets.
4. **North Star statement (DoD item):** plainly pure stretch, not MVP-adjacent — a $\rho$-axis extension whose $\rho=0$ boundary is the frozen model; with one named promotion trigger (a discontinuous $\rho\to0$ limit would reflect on the frozen model's robustness and goes straight to Gary).
5. **Falsifiable conjecture C-Q7:** four clauses — monotone boundary shift, finite closing threshold $\rho^\ast(\mu,np)$ (with the bottleneck-rate heuristic anchor), a pre-registered divergence ansatz $(1-\rho/\rho^\ast)^{-\xi}$ to fit or refute, and the two-channel-specific interaction clause ($\rho^\ast$ increasing in $\mu$; no re-entrant region). All readable off $P(\text{systemic-ever})$ grids with existing analysis machinery.
6. **Implementation plan (§IV convention):** new `src/twocascade/recovery.py` variant engine — **zero `reference.py` changes, flagged per the oracle rule** (DoD item) with D-026 cited as the how-approval-works precedent; the **split-RNG-stream design that makes the $\rho=0$ limit a bit-identical regression test against the oracle** (the design's key validation idea — a single-stream design would desynchronize draw order and lose exactness); additive runner config; explicit `ever_failed` schema naming to prevent metric conflation; C++ parity explicitly scoped out until Python results exist, with its own adapted validation prongs sketched.
7. **Risks** incl. pre-committed handling of the trivial/first-order outcome, metric-confusion prevention (citing the S-006/S-007 errata pattern), baseline-comparability, and R2 rabbit-hole guardrails.

## Definition of Done check

- [x] Doc exists, self-contained.
- [x] New stopping rule fully specified for both variants (R1: empty-failed-set absorbing; R2: extinction-or-horizon with endemic classification — the non-halting risk named, per the watch-out).
- [x] $R_\text{fear}<1$ under recovery explicitly worked out (inequality derivation in §2 of the doc), not assumed.
- [x] MVP-adjacent vs. stretch stated plainly (pure stretch, scheduled behind Q4/Q5); `reference.py` implication flagged as requiring separate explicit approval, and the design removes the need for it entirely.
- [x] No file outside `docs/research/` modified.

## Notes for the reviewer

- `/verify` gate unavailable in this sandbox; substituted a self-audit against the DoD (above) and a consistency pass against §3.4's absorbing-state argument and D-005's incremental-field definition (both preserved or explicitly re-derived under the variant).
- Task marked lower-priority/backup in the queue — completed last among the doable tasks, after I, J, K, L, consistent with that framing.
