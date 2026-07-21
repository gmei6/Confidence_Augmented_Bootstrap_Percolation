---
type: Concept
title: "§10 — Next Actions"
description: "Live list of the next few concrete steps; overwritten each session."
mutability: live
---

# §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

1. **Email Prof. Dhara before 2026-07-22** — the only remaining pre-meeting action. The site
   refresh it was gated on is **DONE** (see the Resolved block). The one genuinely open question
   to put to him is the **publication route: empirical (real network data + fear channel) vs.
   theoretical (simplified model + proof)** — every other item on the site's "open questions"
   chapter was closed by Tasks Q/W/X.
2. **Eyeball the refreshed site in a browser before sending.** Structure, hashes, and every
   cited number were verified programmatically, but the rendered layout never was. The two
   things to look at: the 5-panel Q4 figure (widest element on the page) and the 7-column ν
   table — both sit in `overflow-x: auto` and *should* scroll rather than break, but that is
   reasoning, not observation.
3. **Task Y — test the candidate mechanism for the fear multiplier.** Derived 2026-07-21:
   expected fear failures per round is `n·μ̄·(w₁a/n) = w₁·μ̄·a`, so **n cancels analytically** —
   a candidate explanation for why the multiplier is constant in n and grows in μ̄ (constrained
   fit `1 + 5.3·μ̄`, R²=0.98 on the four measured points). The discriminating test is that
   ignition should depend on **w₁**, the most recent-round weight, even though D-006 says the
   *boundary* is kernel-invariant. Queued as `docs/queue/task_Y_fear_multiplier_mechanism.md`.
   ⚠️ This is a mean-field sketch, **not** a derivation — it does not carry through to ignition
   *probability*, and a 4-point fit is weak. Present to Dhara as a hypothesis with a test
   attached, never as a found mechanism.
4. **Optional future — Task R Option B (supra-r_n cross-round test).** The *only* valid way
   to actually test C-Q5(i) cross-round spatial correlation is a supra-r_n cross-type statistic
   (pair-correlation g(d) / Ripley cross-K between early- and late-round remote-nucleus
   centroids at d ∈ (r_n, k·r_n]). Deferred (D-035); pick up only if the advisor wants a
   cross-round correlation probe. Task O's cross-round lower-bound caveat stays OPEN until then.
5. **Queue hygiene — the queue is empty; S/T/U/V/W all closed.** `d70dbd8`'s commit body
   records V, W, and U as having cleared `/verify` (reviewer sign-off, critic PASS, AUDIT PASS).
   S and T have no gate of their own but were **superseded** by W, which was gated: S's ignition
   series is now the 6-point run to n=160000, T's ν fit is now the 7-point fit above. Residual
   caveat: U's and W's task files asked for a *human* at the gate and got a blind one — a
   process gap, not an ungated result. ⚠️ Closure records for these tasks live in **commit
   bodies and `okf/changes/`**, not in `docs/queue/reports/` — a missing report file does not
   mean a task is open (this misread cost a session).

**Resolved 2026-07-21 (S-058) — advisor site refreshed (`2f61275`, pushed):**
- **All stale claims corrected.** The Θ(1) caveat replaced with the settled n-direction result;
  the ν table updated to the 7-point fit (5.61±0.18 / 4.82±0.15); the "shared n≈20000 crossover"
  framing kept off the site entirely (Task W refuted it); the site's own "open questions" chapter
  cut from 3 items to the 1 that is genuinely open.
- **Q4 μ̄×n ignition figure created and embedded** — `results/figures/q4_mumap_ignition.png` via
  the new `scripts/plot_q4_mumap.py` (byte-identical on regeneration). Faceted rather than
  overlaid: 5 single-hue lines failed the normal-vision adjacent-pair separation floor.
- **Multiplier claim qualified.** "Approximately constant ~3×" read as "always 3×" and was wrong
  at low μ̄ (1.5× at μ̄=0.1). The multiplier is constant **in n** at fixed μ̄, not across μ̄.
- **Replicate discrepancy documented** (page note + in-figure caption): the table's μ̄=0.4 row and
  the figure's μ̄=0.4 panel are independent replicates differing up to 27.6% at a cell, while the
  μ=0 row is trial-identical. Cause is the flat cell-major seed spawn, which predicts both.

**Resolved 2026-07-19 (S-056/S-057):**
- **Task Q (S-054): merged `c4ef634`.** ε-cap water-filling fix landed; unblocked Task X.
- **Task X (S-056): DONE, AUDIT PASS.** C-Q4(i) γ=0→+1 leg confirmed cap-free; C-Q4(ii)
  size-biased collapse REFUTED (μ̄ ≻ μ*, ratio 2.05). Report: `docs/queue/reports/task_x_report.md`.
- **Task R (S-057): DONE, AUDIT PASS.** Counting bug fixed (peeling, `e066fd8`); the strict-
  r_n-clique cross-round metric is structurally blind (D-035), z-test retired; C-Q5(i)
  cross-round question stays OPEN (Option B is the valid test — item 4). Supersedes the
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
