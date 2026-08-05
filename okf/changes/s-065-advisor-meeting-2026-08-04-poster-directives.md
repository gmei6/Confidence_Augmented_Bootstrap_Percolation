---
type: Session Change
title: "S-065 — Advisor meeting 2026-08-04: poster narrative/schematic directives"
mutability: append-only
timestamp: 2026-08-04
tags: [advisor, meeting, poster]
---

# S-065 — Third advisor meeting: poster design directives

Third advisor meeting (Prof. Dhara) held 2026-08-04. Captured live into
`okf/meeting-notes/2026-08-04-dhara.md`.

**Q&A:** advisor asked for the exact configuration behind the poster's 3-family hero
comparison. Answered from `configs/poster_{er,cm,girg}_mu{0,40,70}.json`: all three share
n=10000, r=2, fear concentration κ=50, θ=0.5, uniform 5-window fear kernel, and matched
mean degree ⟨k⟩=4.5336 (Janson scaling, alpha=0.6, n_ref=10000). They differ only in the
`graph` block — ER defaults to `gnp` (p from matched degree, C++ engine); configuration
model uses `configuration_model`, τ=2.5, d_min=2 (Python); GIRG uses `girg`, τ=2.5,
α_g=1.2, w_min=0.186377 calibrated (Python). Swept at μ̄∈{0,0.4,0.7}, 500 trials/cell,
base_seed=42.

**Design directives received (D-046):** (1) add a small model schematic — network diagram,
red nodes = infected/failed, a distinct visual encoding for fear, consistent color-coding;
(2) add an explicit sentence motivating the fear+heterogeneity+geometry study as an
addition to studying the baseline; (3) restructure the talk baseline-first (who uses it /
why it's the baseline, then how it works) under an "Our model / Goal / What are we looking
for" framing; (4) adopt a linear title→what-exists→what-we-did poster arc (the same shape
stated twice, as problem→why-interesting→what's-done→what-we-did).

No `src/`, `configs/`, or `results/` changes this session. P1 of the S-064 pickup checklist
(capture meeting notes) is now closed. The 4 untracked poster pilot raw files
(`poster_{cm,er}_mu{50,60}_pilot_raw.json`) predate this session (S-064) and are unrelated.

**Validation:** n/a — no code/result change to validate; this session is a notes-capture
and scoping session only.
