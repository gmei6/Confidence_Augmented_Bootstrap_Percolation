---
mutability: live
type: concept
---

# §9 — Open Questions & Blockers 🟢 *(overwrite each session)*

- **Blockers:** None.
- **Active Constraints & Warnings:** Cross-reference D-018 platform limitations (macOS Debug = UBSan only; ASan deferred to Linux/PACE).
- **Q1 follow-up:** Asymptotic Decoupling Conjecture remains open (S-029). Whether to pursue a direct fear-field-concentration proof or scope it out in the write-up is still open.
- **Q2 (advisor, RESOLVED 2026-07-01 → D-028):** advisor directed a move toward configuration-model graphs (power-law degree sequence), superseding the open "$G(n,p)$ vs. configuration model" framing. $G(n,p)$/Janson-baseline work stands as completed; new modeling work targets the configuration model.
- **Q3 (advisor):** critical-window width-exponent framing still of interest. Preliminary ν estimates available (Task A): μ=0.0 → ν≈8.39, μ=0.3 → ν≈5.33; fear accelerates sharpening. CIs wide at 3 n values; n=10000 on PACE would tighten.
- **Q4 (new, D-028):** degree-dependent fear factor on a power-law configuration model — advisor explicitly requested this simulation.
- **Q5 (new, D-028):** geometric effects on cascade locality — random geometric graphs first, then the more general geometric inhomogeneous random graphs (GIRGs); does the panic field stay spatially local, or does the cascade still percolate across "continents"?
- **Q6 (new, D-028):** combine Q4 + Q5 — degree heterogeneity on a geometric (GIRG) graph.
- **Q7 (new, D-028, lower priority):** optional recovery/healing phase (SIR-style) as a model variant, vs. the current permanent-activation assumption.
- **Q8 (new, D-028, lower priority):** weighted-edge / supply-capacity variant (edges as economic "supply," nodes need a threshold amount) — cascade behavior depends on edge weight, not just topology.
- **Engineering (minor):** AppleClang 17 `-mcpu=native` build flag failure.
- **Logistics:** First advisor meeting held 2026-07-01 2:00pm. Next meeting **2026-07-15**. Advisor wants simulation results emailed for comment before that meeting. Two possible publication routes flagged: empirical (real network data, e.g. SNAP datasets, plus the fear channel, aiming for a counterintuitive finding) vs. theoretical (simplified model + proof) — either needs a genuinely novel result.
