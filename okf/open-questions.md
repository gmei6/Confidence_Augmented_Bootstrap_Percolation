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
- **Q4 (analyzed, D-028 / S-046):** C-Q4(i) tilt monotonicity SUPPORTED on the cap-free pair (γ=−1→0: 7/7 μ̄ rows); γ=0→+1 untestable until the fear sampler is cap-aware (ε-cap compresses realized μ̄ at τ=2.5 for any γ>0 — §7 early-warning confirmed empirically). Open: cap-aware sampler, then (0,+1) re-test and C-Q4(ii) size-biased collapse.
- **Q5 (analyzed, D-028 / S-046):** C-Q5(iii) homogenization supported (relative to μ=0 control); ℓ=r_n locality fully preserved (zero remote nuclei). C-Q5(i) nucleation law NOT supported as pre-registered (slope ~1.2–1.5, constant leak, not g²) — pending the cross-round ignition tracker before final. C-Q5(ii) duration dichotomy deferred to an n-sweep (C++/PACE).
- **Q6 (simulated, D-028 / S-044):** combine Q4 + Q5 — GIRG super-hub simulated. Found that an extreme hub failure is insufficient to trigger a cascade alone at $r=2$.
- **Q7 (REJECTED 2026-07-04 → D-031):** optional recovery/healing phase (SIR-style). Rejected: it breaks the monotonic cascade property, which invalidates the Tier 1 Janson baseline. Not pursued; see `okf/decisions/d-031-discard-tracks-4-5.md`.
- **Q8 (DEFERRED 2026-07-04 → D-031):** weighted-edge / supply-capacity variant. No structural objection, but removed from the active queue on priority grounds; returns only on explicit advisor request.
- **Engineering (minor):** AppleClang 17 `-mcpu=native` build flag failure.
- **Logistics:** First advisor meeting held 2026-07-01 2:00pm. Next meeting **2026-07-15**. Advisor wants simulation results emailed for comment before that meeting. Two possible publication routes flagged: empirical (real network data, e.g. SNAP datasets, plus the fear channel, aiming for a counterintuitive finding) vs. theoretical (simplified model + proof) — either needs a genuinely novel result.
