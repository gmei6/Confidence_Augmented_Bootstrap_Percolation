# Task P (Q6) Simulation Report

> **⚠️ SUPERSEDED / DEMOTED 2026-07-21 by `okf/decisions/d-037-demote-task-p-super-hub.md`.**
> This report's conclusion — that a single super-hub failure is "insufficient" to cascade at r=2 —
> **must no longer be cited as a result.** The outcome is forced by arithmetic, not produced by the
> simulation: the seed is a single node, so every neighbour has exactly one failed neighbour against
> r=2, making zero solvency failures possible in round 1 *for a single seed of any degree*. The hub's
> degree (1555) never enters; a degree-2 leaf gives the identical result. The recorded `Hub fear = 1.0`
> is the hub's own f_i and is causally inert (the hub is the seed). Q6 is reopened as unanswered. The
> body below is preserved verbatim as the record of what was run; see D-037 for what survives (r≥2 =
> bootstrap-vs-contagion, a property of the rule) and the open GIRG-threshold question.

Tested whether a highly central hub can cause a global cascade when the fear field is local but highly tilted.

- $n = 2000$
- Hub weight = 216.27
- Hub degree = 1555
- Hub fear = 1.0000
- Local Fear Fraction = 0.0005 (1 rounds)
- Global Fear Fraction = 0.0005 (1 rounds)

Result: With only a single hub as the seed, the cascade does not propagate globally (or even locally) because a single failure only provides $r=1$ failed neighbor to its neighbors, which is less than the solvency threshold $r=2$. The fear failure probability is also too low to trigger fear-based secondary failures. A larger seed set is required to initiate a global cascade.
