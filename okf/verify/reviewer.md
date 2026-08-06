---
type: Concept
title: "Verify — Reviewer"
description: "Design and interface-contract criteria for the verify skill's blind reviewer subagent."
mutability: live
---

# Verify — Reviewer

Read `okf/north-star.md` (§2), `okf/architecture/reproducibility.md` (§5.4, §5.6), plus
`okf/model/` (§3) and `okf/architecture/` (§5) relevant to the change under review; also review
`okf/lessons.md` for known modeling pitfalls. Restate the change in one line and name the
Q#/F#/D# it touches before reviewing.

The reviewer returns ranked design/contract/edge-case issues, or signs off:
- Does the change match the design it claims to implement (against §2's contribution claim and
  the relevant `okf/model/` notation/parameters)?
- Are interface contracts between the Python reference engine and the C++ engine (or between any
  two components touched) correct and consistent?
- Are edge cases specific to this project's model (e.g. $\mu=0$ boundary behavior, empirical
  threshold clamping, finite-size effects) actually handled?

Material design issues route back to the owning agent (`python-simulation` / `cpp-engine`) for a
fix; do not let the change proceed to the critic on a design that is known-wrong.
