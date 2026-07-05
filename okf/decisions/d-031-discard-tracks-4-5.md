---
type: Decision
mutability: append-only
timestamp: 2026-07-04
tags: [scope, advisor-tracks, monotonicity]
---

# D-031: Discard Track 4 (SIR recovery); defer Track 5 (weighted edges) indefinitely

**Decision.** Of the five advisor extension tracks logged in [D-028](d-028-advisor-extension-tracks.md), Track 4 (an optional SIR-style recovery/healing phase, Q7) is **rejected** and will not be pursued. Track 5 (weighted edges / supply-capacity variant, Q8) is **deferred indefinitely** — not rejected in principle, but removed from the active queue; it returns only on an explicit advisor request.

**Rationale.**
- *Track 4 (rejected on structural grounds):* recovery breaks the monotone-failure property of bootstrap percolation. Monotonicity is what makes the final failed set well-defined independent of update order and underpins the entire Tier-1 analytical baseline — the Janson threshold mapping (§4), the a_c scaling law (Conjecture 2), and every cross-validation contract built on them. Adding recovery would invalidate the analytical anchor the project's validated results stand on, in exchange for a lower-priority direction the advisor himself marked secondary. This codifies the guardrail already recorded in the S-045 handoff ("Protect the MVP and maintain monotonicity") and the Q7 warning in §9.
- *Track 5 (deferred on priority grounds):* no structural objection — weighted thresholds preserve monotonicity — but the advisor marked it lower priority, and the active Q4/Q5/Q6 tracks (heavy tails, geometry, and their combination) already carry the July-15 deliverable. Splitting effort adds no near-term value.

**Affects.** §9 (open questions Q7, Q8 — closed/deferred accordingly), §10 (next actions — decision item resolved). Supersedes nothing; refines the scope set by D-028. Approved by Gary on 2026-07-04.
