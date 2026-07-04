---
mutability: live
type: concept
---

# §9 — Open Questions & Blockers 🟢 *(overwrite each session)*

- **Blockers:** None.
- **Active Constraints & Warnings:** Cross-reference D-018 platform limitations (macOS Debug = UBSan only; ASan deferred to Linux/PACE).
- **Q1 (REMOVED 2026-07-04, Gary's call):** the decoupling proof is dropped from scope entirely for now — the advisor values simulated runs over proofs at this stage. Not pursued, not timeboxed; the Asymptotic Decoupling Conjecture stays formally open in the literature sense only. `docs/research/q1_decoupling_path_forward.md` (incl. the critical-seed falsification of the literal wording and the ADC' restatement) is retained as the record if this is ever revisited.
- **Q2 (advisor, RESOLVED 2026-07-01 → D-028):** advisor directed a move toward configuration-model graphs (power-law degree sequence), superseding the open "$G(n,p)$ vs. configuration model" framing. $G(n,p)$/Janson-baseline work stands as completed; new modeling work targets the configuration model.
- **Q3 (advisor):** critical-window width-exponent framing still of interest. Preliminary ν estimates available (Task A): μ=0.0 → ν≈8.39, μ=0.3 → ν≈5.33; fear accelerates sharpening. CIs wide at 3 n values; n=10000 on PACE would tighten.
- **Q4 (implemented, D-028 / S-044):** degree-dependent fear factor on a power-law configuration model — fully implemented, Phase 1 sweep raw data generated.
- **Q5 (implemented, D-028 / S-044):** geometric effects on cascade locality — infrastructure for RGG and localized fear merged.
- **Q6 (simulated, D-028 / S-044):** combine Q4 + Q5 — GIRG super-hub simulated. Found that an extreme hub failure is insufficient to trigger a cascade alone at $r=2$.
- **Q7 (new, D-028, lower priority):** optional recovery/healing phase (SIR-style). **Warning:** adding this breaks the monotonic cascade property, which invalidates the Tier 1 Janson baseline. Strongly recommended to reject.
- **Q8 (new, D-028, lower priority):** weighted-edge / supply-capacity variant.
- **Engineering (minor):** AppleClang 17 `-mcpu=native` build flag failure.
- **Logistics:** First advisor meeting held 2026-07-01 2:00pm. Next meeting **2026-07-15**. Advisor wants simulation results emailed for comment before that meeting. Two possible publication routes flagged: empirical (real network data, e.g. SNAP datasets, plus the fear channel, aiming for a counterintuitive finding) vs. theoretical (simplified model + proof) — either needs a genuinely novel result.
