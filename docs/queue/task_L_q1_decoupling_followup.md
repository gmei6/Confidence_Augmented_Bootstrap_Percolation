# Task L — Q1 follow-up: chart a path for the Asymptotic Decoupling Conjecture

**One-line task.** The Asymptotic Decoupling Conjecture (open since S-029) needs a decision: attempt a direct fear-field-concentration proof, or scope it out of the write-up as a stated-but-unproven conjecture. Produce a document that makes this decision defensible either way.

**Touches:** new `docs/research/q1_decoupling_path_forward.md`. Read-only against everything else.

## Environment note (read first)

No git access in this container, on purpose — do not attempt `git commit`/`push`/`branch`/`worktree`. This task only writes one new file under `docs/research/`; edit in place, no isolation needed. This is a mathematical-exploration and recommendation document, not code — do not modify `src/`, `cpp/`, or `results/`.

## Why this is low-human-input

A literature/derivation exercise building on work already done in this repo (D-025's leave-m-out exact conditional-i.i.d. proof, S-029's empirical finding). No simulation runs required, though you may cite existing figures/results already in `results/` if relevant — do not regenerate them.

## Context to read first

- `docs/PROJECT_TRACKER.md` §9 Q1 follow-up, D-009 (Tiered Stance, §11), D-025, D-026, S-028, S-029 (§11/§12).
- `docs/research/other/f2_theoretical_analysis.md`, `docs/research/other/pairwise_decoupling_walkthrough_s029.md`, `docs/research/janson_reformulation_with_fear.md`, `docs/research/other/janson_reformulation_with_fear.md` if distinct from the above — check which exists.
- `docs/research/other/q1_rigor_assessment.md` and `docs/research/other/q1_adversary_review.md` and `docs/research/other/q1_simulation_feasibility.md` — these look like they already assess this exact question; read them first so this task adds new ground rather than repeating them.
- If `okf/` exists by the time this task runs (Task I may have completed), read the equivalent `okf/` files instead of the tracker sections above.

## Plan

1. **Summarize the state of the art in one page**: what D-025's leave-m-out construction proved exactly (conditional independence of activation times given the leave-m-out fear field, at finite $n$), and what S-029's empirical result found (variance-ratio excess $R(\mu>0) - R(\mu=0)$ does not clearly vanish over $n \in \{1000,\dots,8000\}$) — and be precise about the gap between them: conditional independence given the field is not the same as the field itself concentrating.
2. **Attempt the direct route.** Sketch what a fear-field-concentration proof would need (e.g. a concentration inequality for $g_t = a_{t-1}/n$ around its mean, using the branching-process-like structure from the Tiered Stance's rigorous auxiliary lemmas, D-009). Go as far as you can; if you hit a genuine obstruction, state exactly what it is and why (not just "this seems hard").
3. **Assess the empirical-scope-out route.** What would the write-up honestly say if the conjecture is left open: is the empirical non-vanishing result (S-029) itself publishable as a finding (e.g. "decoupling holds conditionally but the field's own fluctuations do not vanish at these system sizes, an open question for future work"), consistent with §2's honest-novelty framing (Tiered Stance already sanctions Tier-2 conjecture-with-mean-field-analysis rather than full rigor here).
4. **Recommend, with reasoning**, which path to take given the timeline (§6 — Wk 9 of 10, one advisor meeting left on 2026-07-15) and the Tiered Stance (D-009). Do not silently decide for the project — this is exactly the kind of direction question that gets surfaced, not resolved unilaterally (per the tracker's own "guard the direction" rule).

## Definition of Done

- [ ] `docs/research/q1_decoupling_path_forward.md` exists, self-contained, and does not merely restate the three existing `q1_*` docs — cite them and add the concentration attempt and the timeline-aware recommendation.
- [ ] The gap between "conditional independence given the field" and "field concentration" is stated precisely, not conflated.
- [ ] A clear recommendation is given, with an explicit acknowledgment that this is a direction call for the human to make, not a fait accompli.
- [ ] No file outside `docs/research/` is modified.

## Watch-outs

- D-025's own log entry notes an earlier discrepancy-bound approach to the same goal was found false and withdrawn pre-commit — don't re-derive that same false approach; read the existing docs first specifically to avoid this.
- Per the tracker's Tiered Stance (D-009): this project explicitly does not aim for full rigor on the combined model. Don't let this task drift into an unbounded pure-math side-quest — timebox the direct-proof attempt (step 2) and move to the recommendation (step 4) once you've made a genuine attempt.
