---
type: Decision
title: "D-037: Task P's super-hub negative is demoted to a sanity check; Q6 reopens as unanswered"
mutability: append-only
timestamp: 2026-07-21
tags: [q6, task-p, girg, demotion, advisor-prep, tautology]
---

# D-037: Task P is demoted from a negative result to a sanity check; Q6 reopens

## Decision
Task **P** (Q6, S-044) is **DEMOTED**. Its recorded finding — "a single extreme super-hub
failing is insufficient to cause a cascade at r=2; heavy tails alone don't bypass the
multi-path structural requirement" — **must no longer be cited as a result.** It is a
demonstration that the implementation obeys its own threshold rule.

**Q6 is returned to OPEN.** It has no empirical answer.

## Rationale
1. **The outcome is forced by arithmetic, not produced by the simulation.** The seed is a
   single node. With $a=1$, every neighbour has exactly one failed neighbour against $r=2$,
   so **zero solvency failures are possible in round 1 — deterministically, for a single seed
   of any degree.** The hub's degree (1555 of n=2000) never enters the calculation; a
   degree-2 leaf returns the identical answer. The run could not have returned anything else.
2. **The fear channel cannot bridge it, for the same reason.** The field every other node
   feels is $g = a/n = 1/2000$, small *because* $a=1$. Expected fear failures that round are
   $n \cdot E[f] \cdot g = E[f] < 1$ — subcritical, exactly as $R_{\text{fear}} \approx \bar\mu$
   predicts. The recorded `hub fear = 1.0` is the hub's *own* $f_i$; since the hub is the seed
   and has already failed, that value is causally inert and was never an experimental condition.
3. **It reached outward-facing material as a finding.** The claim was carried in
   `okf/status.md`, `okf/open-questions.md` (Q6), and the 2026-07-22 advisor explainer, where
   it was framed as "a real result, not a failed experiment" with the additional and incorrect
   gloss "even with panic concentrated on it." Caught 2026-07-21 during Gary's card-by-card
   walkthrough, the day before the advisor meeting.
4. **Provenance was never sufficient for a result in any case.** Single demonstration run,
   n=2000, on a **GIRG** — a different graph family from the rest of the project — with no
   trial count and no ensemble. It does not satisfy §5.6.

## What survives
$r \ge 2$ is what makes this model bootstrap percolation rather than ordinary contagion: at
$r=1$ a single hub failing *would* sweep the graph (the SIR/epidemic case). The multi-path
requirement is a genuine structural property that degree heterogeneity cannot buy around.
**This is a property of the rule and must be stated as one, never as an empirical finding.**

## What is now open
S-044's own recorded next step — "extend the GIRG simulation with larger seed sets and higher
fear fractions to locate the percolation threshold" — was never carried out. Where the GIRG
ignition threshold sits as seed size and fear rise is **unanswered**, and is a more interesting
question than the demoted claim. Not queued here; queue it only if the advisor wants Q6 pursued.

## Relationship to D-035
D-035 retired a metric that was **selection-forced** (the cross-round nucleus rule made
`round_gap=0` impossible to violate). This is the **parameter-forced** sibling: nothing about
the measurement is wrong, but the parameter choice ($a=1$) determines the answer before the
simulation runs. Both are the same error — a result that could not have come out otherwise —
and D-035's lesson did not prevent this one because it was written narrowly about selection
rules. The generalized check is recorded in `okf/lessons.md` §5.

## Affects
`okf/status.md` §8 (Task P line); `okf/open-questions.md` (Q6); `okf/lessons.md` §5;
`okf/changes/s-044-analysis-of-extension-tracks.md` (append-only — **not** edited; superseded
by this decision); `docs/queue/reports/task_p_report.md`; `.lavish/advisor-explainer.html`
card 6; session `s-059`.
