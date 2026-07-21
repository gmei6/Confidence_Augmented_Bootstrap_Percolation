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
3. **Task Z — widen the γ grid on the tilt experiment.** C-Q4(i) has only **three** γ points
   (−1, 0, +1) and they show a clearly **saturating** shape: at μ̄=0.4 the empirical critical
   seed runs 8.00 → 5.83 → 5.41, so γ=−1→0 buys 2.17 seeds while γ=0→+1 buys only 0.42.
   Three points cannot tell a saturating curve from a kink, a plateau, or an eventual reversal —
   **the same "too few grid points" trap that produced the retracted Θ(1) claim** (Task S/W).
   Proposed: γ ∈ {−2, −1.5, −1, −0.5, 0, +0.5, +1, +1.5, +2} at τ=2.5, n=10000, paired on
   `base_seed=42`, across the existing μ̄ rows. Config-only, no `src/` change, autonomous-safe.
   ⚠️ **Two things this task must check, not assume:** (a) at large **positive** γ the ε-cap
   becomes binding again — the very bug Task Q fixed; the water-filling path handles it, but every
   cell must report `stats["realized_mu_bar"]` against nominal and flag cap-affected rows before
   any comparison (see `okf/lessons.md` §1). (b) At large **negative** γ, any degree-0 node gives
   weight ∞; `d_min=2` prevents this for the *drawn* sequence, but erasure can realize degree 0,
   so confirm the fear sampler is fed drawn degrees, not realized ones.
4. **Task Y — largely invalidated 2026-07-21; rewrite or retire before running.** The queued
   discriminating test (front-loaded kernel `[1,0,0,0,0]` vs uniform `[0.2×5]`, predicting a ~5×
   change in multiplier−1) **does not discriminate.** Exploratory paired pilot, n=4000, μ̄=0.4,
   400 trials/arm: uniform **0.147**, front-loaded **0.110** — no 5× effect, if anything the
   opposite direction (Fisher p=0.14, so read as "no effect", not a reversal). Cause: both
   kernels have Σwₖ=1, so total fear offspring is identical (D-006 kernel-mass invariance); the
   transient w₁ argument does not survive a multi-round cascade with permanent failures and
   cumulative neighbour counts. ⚠️ `docs/queue/task_Y_fear_multiplier_mechanism.md` still carries
   the pre-registered 5× prediction and **needs an appended correction** before anyone picks it
   up. **What survives:** the n-cancellation `n·μ̄·(Σwₖa/n) = μ̄·Σwₖa` holds for *any* kernel, so
   "why is the multiplier flat in n" is answered by algebra and needs no experiment. **The one
   salvageable test:** the sketch predicts the multiplier is *linear* in μ̄ (`1 + 5.3·μ̄`, R²=0.98
   on four points) — extend the ignition μ̄-grid to 0.5/0.6/0.7 and see whether it stays linear or
   bends. Pilot is exploratory: nothing stamped, nothing committed, **not** a §5.6 result.
5. **Optional future — Task R Option B (supra-r_n cross-round test).** The *only* valid way
   to actually test C-Q5(i) cross-round spatial correlation is a supra-r_n cross-type statistic
   (pair-correlation g(d) / Ripley cross-K between early- and late-round remote-nucleus
   centroids at d ∈ (r_n, k·r_n]). Deferred (D-035); pick up only if the advisor wants a
   cross-round correlation probe. Task O's cross-round lower-bound caveat stays OPEN until then.
6. **Queue hygiene — the queue is empty; S/T/U/V/W all closed.** `d70dbd8`'s commit body
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
  cross-round question stays OPEN (Option B is the valid test — item 5). Supersedes the
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
