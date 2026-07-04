# Task L Report: Q1 Decoupling — Path Forward

**Date:** 2026-07-04 (fable overnight run) · **Research question affected:** Q1 follow-up (open since S-029) — new `docs/research/` document; no existing doc revised (per AGENTS.md §III).

## What was produced

`docs/research/q1_decoupling_path_forward.md`. All four plan steps, plus one finding the task didn't ask for but that changes the picture:

1. **One-page state of the art** distinguishing precisely (DoD item) between D-025's *exact conditional independence given the leave-out field* (a finite-$n$ factorisation of a conditional law, proven) and the conjecture's *concentration of the field itself* (a concentration-of-measure claim about the conditioning object, open) — with the one-sentence statement of why the first does not imply unconditional independence without the second.
2. **A genuine direct-route attempt:** a variance-propagation sketch (law of total variance + the exact conditional-Bernoulli structure of generations + a linearised AR recursion for fluctuations). It goes far enough to yield: (a) fear adds no new divergence mechanism — it multiplies baseline branching noise by a bounded $1/(1-\mu)^2$ factor; (b) a concretely provable **Lemma C1** (fear-field concentration for strictly subcritical seeds, $O(1/a_c(n))$ relative variance, using only the already-sanctioned Tier-1 lemmas); and (c) the **exact obstruction** at criticality, stated as what it is (saddle-node tangency makes fluctuation propagation neutral; noise accumulates over a diverging bottleneck; this is critical slowing down, not a missing estimate).
3. **New ground (not in the three existing q1_* docs):** the conjecture *as currently worded* is **false at the critical seed** — outcome bimodality (the project's own verified result) contradicts concentration around any single deterministic trajectory. The doc supplies the cheap rigorous argument and a repaired conditional restatement (**ADC′**, three parts, with part (i) = Lemma C1's target and parts (ii)/(iii) genuinely open). It also explains why the withdrawn discrepancy-bound approach (D-025's logged failure) is *not* re-derived, and what its salvageable strictly-subcritical remnant is (watch-out honored).
4. **Scope-out assessment:** the honest write-up package under D-009's Tiered Stance (Tier-1 theorems incl. optional C1; ADC′ as the stated conjecture with the bimodality rationale — which preempts the adversary-review Scenario-C referee attack; S-029 reported as underpowered-but-consistent, now with a *quantitative* prediction the sketch supplies: excess should decay as $n^{-0.4}$, ≈2.3× over the tested range). Links queue Task E (currently BLOCKED on the sandbox environment) as the right empirical instrument, with the $n\gtrsim10^5$ power requirement.
5. **Recommendation, explicitly flagged as Gary's call:** scope out the full proof; timebox one day for Lemma C1 + the ADC′ restatement (via the gated research-cycle since it edits an auditable research doc); spend the freed time on the advisor-requested Q4–Q6 simulations before 2026-07-15. Alternatives (B: full scope-out, C: proof push) are laid out with reasoning; C is recommended against with the withdrawn-approach episode as the cautionary pattern.

## Definition of Done check

- [x] Doc exists, self-contained, and adds new ground beyond the three existing `q1_*` docs (cited, not restated): the propagation sketch with its named obstruction, the bimodality falsification of the literal wording + ADC′ restatement, the quantitative $n^{-0.4}$ empirical prediction, and the timeline-aware recommendation.
- [x] Conditional-independence vs. field-concentration gap stated precisely, not conflated (dedicated paragraph, §1).
- [x] Clear recommendation with explicit "this is a direction call for the human" framing and enumerated alternatives.
- [x] No file outside `docs/research/` modified (the proposed ADC′ edit to `janson_reformulation_with_fear.md` is deliberately *not* applied — flagged for the gated pipeline).

## Notes for the reviewer

- Timebox honored: the direct-route attempt (§2 of the doc) was carried to the point of a provable off-criticality lemma and a structural obstruction at criticality, then stopped — no unbounded pure-math excursion.
- `/verify` gate unavailable in this sandbox; substituted a self-audit re-reading the sketch against D-025's §5.1 formalism (the conditional-Bernoulli structure claim rests on the reformulation doc's own Uniform Coupling: private edge indicators and private uniforms per node) and against the D-025 log's withdrawn-approach description.
