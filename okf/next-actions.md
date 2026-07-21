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
4. **Task AA — fear-only percolation: does the critical seed scale like θn(1−μ̄)?** Gary's design
   (2026-07-21), from the μ̄-sweep result. Disable solvency entirely (`r = n+1`, or `r = 10⁹` as
   the pilot used) so the fear channel runs alone, then sweep the **seed size a** against μ̄ and n.
   **This has a derivable prediction, so it is a test and not a fishing trip.**
   - With solvency off, fear is a branching process with reproduction number exactly
     `R_fear = μ̄·Σwₖ = μ̄` — subcritical for every μ̄ < 1. Expected **total** progeny from a
     ancestors is `a/(1−μ̄)`. Systemic needs θn, so
     **`a_c^fear ≈ θn(1−μ̄)`**, i.e. **`a_c/n ≈ θ(1−μ̄)`**.
   - **The claim that makes this worth running:** fear alone needs a seed that is a *fixed
     fraction of n* — macroscopic, never bounded — **unless `1−μ̄` shrinks like 1/n.** So fear
     alone can ignite from a bounded seed only if fear approaches certainty at a rate tied to
     network size. That is a much stronger form of "amplifier, not igniter": a statement about
     **scaling**, not a description. It sits directly against the headline — the heavy tail lets a
     bounded seed ignite; fear alone provably cannot at any fixed μ̄ < 1.
   - **Consistency check already available:** at μ̄=0.999, n=4000 the formula gives a_c ≈ 2, and
     the exploratory pilot got **0/1000** at exactly a=2. Not a contradiction — near criticality
     the total-progeny distribution is heavily skewed, so mean-at-threshold still implies low
     probability *of* threshold. Expect the measured a_c to sit **well above** θn(1−μ̄), with the
     gap set by fluctuation; quantifying that gap is part of the result.
   - **Design:** 2-D sweep of a × μ̄ at 2–3 values of n, measuring a_c^fear, testing whether
     `a_c/n` tracks `θ(1−μ̄)`. Config-only if `r` is settable per-config; check before assuming.
   - **Motivating application (Gary's):** with solvency off this is pure belief contagion — false
     news, no structural failure. ⚠️ **Own the limitation before offering it:** the fear channel is
     **mean-field, not network-structured** — every node sees the same global `g_t`, which models
     "everyone reads the same headline", not spread along social ties. Real misinformation is
     network-mediated, and structure mattering is the whole point of the model elsewhere. Card 1's
     local-vs-global result (local fear is statistically identical to no fear) is evidence the
     distinction matters, and localising the belief channel is the natural extension.
   - **Companion variant (Gary, 2026-07-21) — seed *fear* instead of failures, at a=0.** Find the
     lowest initial fear field that activates the network with **no failed banks at all**.
     ⚠️ **This cannot be run as a parameter sweep — it needs a model extension.** With `a=0` the
     current engine is inert: no failures ⇒ `g_t = 0` ⇒ `f_i·g_t = 0` ⇒ no fear failures, and
     solvency has nothing to count. There is **no spontaneous ignition path** in the model as
     written. The variant requires injecting an **exogenous initial fear field `g_0`** — a
     `src/twocascade/` change (baseline isolation + `/verify`), not a config. Do not queue it as
     config-only.
   - **The exogenous-`g_0` variant has its own, cleaner prediction.** Round 1 gives `n·μ̄·g_0`
     failures, then the same subcritical branching with `R = μ̄`, so total progeny
     `≈ n·μ̄·g_0/(1−μ̄)`. Systemic at θn requires
     **`g_0* ≈ θ(1−μ̄)/μ̄`** — **independent of n**, since `g_0` is already a fraction. Worked
     values at θ=0.5: μ̄=0.5 → g_0*≈0.50; μ̄=0.9 → ≈0.056; μ̄=0.999 → ≈0.0005. This is the same
     physics as the a-sweep above expressed as a fraction rather than a count (`g_0 ≈ a/n`), with
     the n scaled out — arguably the better-posed version of the experiment, and it is a plausible
     model of a pure news shock: everyone frightened, nobody actually failed.
   - ⚠️ **"Activate the whole graph" is not θn.** Cascades in this model stop well short of the
     structural ceiling — measured max 0.732 (μ=0) and 0.8975 (μ̄=0.4) against a ceiling of ~99.8%
     — so "whole" may be unreachable at any g_0. Decide up front whether the target is θ=0.5 or a
     Janson-style n−β, and see the open question in
     `okf/handoff-lavish-explainer-session.md` before designing against "whole".
   - **Not before the 2026-07-22 meeting.** The scaling prediction is derivable and reads better to
     Dhara as "here is a prediction I can test" than as a rushed pilot. It is also a strong
     candidate answer to the publication-route question (item 1): clean theoretical statement,
     obvious empirical hook.
5. **Task Y — largely invalidated 2026-07-21; rewrite or retire before running.** The queued
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
6. **Optional future — Task R Option B (supra-r_n cross-round test).** The *only* valid way
   to actually test C-Q5(i) cross-round spatial correlation is a supra-r_n cross-type statistic
   (pair-correlation g(d) / Ripley cross-K between early- and late-round remote-nucleus
   centroids at d ∈ (r_n, k·r_n]). Deferred (D-035); pick up only if the advisor wants a
   cross-round correlation probe. Task O's cross-round lower-bound caveat stays OPEN until then.
7. **Queue hygiene — the queue is empty; S/T/U/V/W all closed.** `d70dbd8`'s commit body
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
  cross-round question stays OPEN (Option B is the valid test — item 6). Supersedes the
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
