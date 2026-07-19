---
type: Concept
title: "§10 — Next Actions"
description: "Live list of the next few concrete steps; overwritten each session."
mutability: live
---

# §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

1. **Refresh `advisor-update-2026-07-22/index.html` with this session's results (NEW, 2026-07-18)
   — not yet done.** The site (built via Ultraplan, S-051-era) predates all of this session's
   work and needs updating before the meeting:
   - Task S: Q4(iii) ignition gate extended to n∈{40000,80000}. Gate still holds; the μ̄=0.4
     decline (0.134→0.116→0.062→0.050→0.044) looks like a finite-size transient flattening after
     n=20000 (χ²=1.70, p≈0.43 homogeneity test on the n≥20000 triple) rather than true decay to
     zero — worth a card of its own.
   - Task T: Q3 ν re-fit at n=20000. ν(μ=0) dropped more than expected (8.65±1.04 → 6.29±0.39);
     ν(μ=0.3) barely moved (4.54±0.26 → 4.90±0.22) and its raw width nearly flattened between
     n=10000 and n=20000 — the **same flattening pattern as the Q4 series above**, which is
     itself a notable cross-experiment observation worth surfacing to the advisor, not just
     folding into a table.
   - The `plot_fear_field_concentration` savefig/close bug is now fixed (`df0575d`) — can drop
     from any "known defects" list if the site has one.
   - Tasks Q (ε-cap sampler fix) and Task R (cross-round remote-ignition tracker) are queued but
     **not started** — still open items needing the advisor's awareness, not new results.
   - `gh-axi` was installed (session tooling, not research) — not meeting-relevant, don't
     include.
   Figures to (re)embed as base64, same convention as the original 3: an updated
   `finite_size_scaling_r2_n10000.png` (regenerated, now 5-point) and, if a Q4-gate figure gets
   made, that too — check `results/figures/` after regenerating.
2. **Email Prof. Dhara before 2026-07-22** — send once item 1's site refresh is done, so the
   email and the leave-behind site tell the same story.
3. **Optional future — Task R Option B (supra-r_n cross-round test).** The *only* valid way
   to actually test C-Q5(i) cross-round spatial correlation is a supra-r_n cross-type statistic
   (pair-correlation g(d) / Ripley cross-K between early- and late-round remote-nucleus
   centroids at d ∈ (r_n, k·r_n]). Deferred (D-035); pick up only if the advisor wants a
   cross-round correlation probe. Task O's cross-round lower-bound caveat stays OPEN until then.
4. **Queue hygiene — U/W still need a human at their verify gate.** Tasks U (Q5 duration
   asymptotic form) and W (finite-size crossover) were committed (`d70dbd8`) but their task
   files flag they need a human at `/verify`, not blind overnight. Not yet gate-cleared.

**Resolved 2026-07-19 (S-056/S-057):**
- **Task Q (S-054): merged `c4ef634`.** ε-cap water-filling fix landed; unblocked Task X.
- **Task X (S-056): DONE, AUDIT PASS.** C-Q4(i) γ=0→+1 leg confirmed cap-free; C-Q4(ii)
  size-biased collapse REFUTED (μ̄ ≻ μ*, ratio 2.05). Report: `docs/queue/reports/task_x_report.md`.
- **Task R (S-057): DONE, AUDIT PASS.** Counting bug fixed (peeling, `e066fd8`); the strict-
  r_n-clique cross-round metric is structurally blind (D-035), z-test retired; C-Q5(i)
  cross-round question stays OPEN (Option B is the valid test — item 3). Supersedes the
  S-055 block. Report: `docs/queue/reports/task_r_cross_round_report.md`.

**Resolved 2026-07-18:** item 3 ("review and commit the S-046/S-047 primary-checkout working
tree") was already committed as `fb0ac42` before this session started — removed as stale, no PR
needed. Npm-install proposal came back: installed `gh-axi` (low-risk, real token savings);
skipped `chrome-devtools-axi` (defer until browser-automation work starts) and `tasks-axi`
(doesn't appear to exist under that name in the AXI ecosystem — flagged, not installed).
Environment note: run simulations with `arch -arm64 python3` (Rosetta/numpy mismatch).

**Cleared 2026-07-18 (Gary's call):** the "Study the Math" deep-dive and its gating prerequisite
reading queue, and the `graphs.py` configuration-model vectorization perf item — Gary will pick
up the modeling intuition via the `advisor-update-2026-07-22/` site instead. If the perf item
matters again later, it's still recorded in `EXPLAINER.md` §12 and `graphs.py:30-45`.
