---
type: Concept
title: "§10 — Next Actions"
description: "Live list of the next few concrete steps; overwritten each session."
mutability: live
---

# §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

**⏸️ PICKUP CHECKLIST (updated S-066, 2026-08-06 — context in `okf/changes/s-066-*.md`):**

P1. ✅ **DONE (S-065) — Meeting follow-through.** Captured into
    `okf/meeting-notes/2026-08-04-dhara.md`. Outcomes: 3-family config Q&A answered; four
    poster design directives received, recorded as **D-046** and folded into items 8–10
    below.
P2. ✅ **DONE (S-066, Gary-approved).** Pushed `d25f9f2..6699c10` (the five S-066
    commits). NOTE: the S-064 "origin at `8a40677`" claim was stale — origin already
    had the girg-cpp merge and the P3 arms; only the gate commits were unpushed.
    Local and origin in sync.
P3. ✅ **DONE (2026-08-04, committed `f30aef1`/`0e739a1`/`d25f9f2`) — GIRG densification
    arms** (μ̄ ∈ {0.1, 0.2, 0.3, 0.5, 0.6}, n=10000, cpp engine, matched w_min). Both
    poster figures now run full μ̄ grids; wired into both pipelines (P3b). Verified inside
    the S-066 gate (arm cells reproduced; n>65536 warning never fired).
P4. **Finish the post-merge smoke:** `pytest tests/test_cpp_girg_validation.py` (+ the
    other four files) against the fresh main-repo build (ctest already 2/2; the run was
    interrupted at the S-064 wrap). Then remove `cpp/build.stale-cache-20260804`.
P5. ✅ **DONE (S-066).** Gate component AUDIT PASS (item 3b below); all figures verified
    300 dpi; the zip's exact contents compile clean locally via tectonic (only
    font-substitution warnings + two ~7pt overfull boxes) with every panel/QR verified
    on-page in the rendered PDF. Residual (one-minute check, not a work item): open the
    zip in Overleaf itself once before sending to print — Overleaf runs TeX Live, not
    tectonic.
P6. **Queued behind:** N1–N4 + deferred-advisory hygiene (task list #10; N1/N2 are
    pre-existing CLI defects, N3/N4 validator/provenance minors); **S-066 gate-advisory
    hygiene batch** (per-cell trials check; a consumer for `reliable`; dead-code +
    stale-comment cleanup in both analysis scripts and poster.tex; famcompare bootstrap
    per-cell seeding; ER μ̄=0.7 crossing-estimator disclosure; `runner.py` metadata gap —
    `src/` change, own isolation + gate); branching-factor ER arm (approved, still
    unstarted); worktree cleanup (`tc-girg-cpp`, `tc-work`, `tc-work2`); SNAP teaser
    (item 6, untouched); optional presenter-sync layer for the QR demo.

**Poster queue (D-038, advisor meeting 2026-07-22 — items 1–7 are the deliverable).**
Review surface for this queue: `.lavish/poster-remaining-work.html` (2026-07-29, may itself
now be stale — items 1–3 below closed after that surface was last written).

1. ✅ **DONE — ER family in the runner + matched-degree baseline** (`68adadb`, `301d560`,
   `ba2bf6f`). ⟨k⟩=4.533 matched across ER and CM via
   `results/processed/matched_degree_calibration.json`.
2. ✅ **DONE — Comparison 1 (heterogeneity: ER vs configuration model), closed 2026-07-29
   (`d9edf19`).** The two queued commands (`analyze_poster_comparison.py`,
   `plot_scaling_law_departure.py`) ran; the D-012 departure claim is now a five-point
   monotone trend over $\bar\mu\in\{0.1,0.2,0.3,0.4\}$ (ratios 1.128/1.248/1.514/1.839), all
   clear of the $r=2$ structural floor, plus the excluded $\bar\mu=0.7$ point. Figure:
   `results/figures/scaling_law_departure.png` (generated, not just claimed — verified by
   mtime against its `source_raws` in this catch-up). ⚠️ Still **not** blind-`/verify`-gated
   — Antigravity-driven pilots, self-checked via byte-identity reproduction only.
2b. ✅ **DONE — poster working tree committed.** `git status --short` now shows only
   `.gitignore`/`pytest.ini` (unrelated, orthogonal `overnight`-skill fix). Raw layout landed
   as poster-prefixed files at `results/` top level (`results/poster_*_raw.json`), not
   `results/raw/`; `_part`/`_part2`/`_chunk0` intermediates stayed gitignored, as intended.
2c. ✅ **DONE — engine asymmetry named, not eliminated (`2024c23`).** `okf/poster/poster.tex`
   now carries the §5.4 disclosure: ER ran on the C++ engine, configuration model **and**
   GIRG on the Python reference. No cell was re-run on both engines; the poster cites §5.4
   instead, which is the alternative the item itself offered.
3. ✅ **DONE — Comparison 2 (geometry: configuration model vs GIRG), closed 2026-08-02
   (arc C1–C3b: `6c5491a`, `c1dcd84`, `8956d75`, `0179110`, `2024c23`).** All three planned
   steps landed:
   (a) **GIRG sampler ported to block-vectorized numpy** (`6c5491a`, ~44× at n=10000,
   worktree `c1-girg-fast-sampler`, blind reviewer→critic→auditor AUDIT PASS);
   (b) **GIRG calibrated to ⟨k⟩=4.533 at τ=2.5** ($w_{\min}=0.186377$, `c1dcd84`; own test
   suite 4/4, not blind-gated — a config/script change, not `src/`);
   (c) **sweeps + figure delivered** (`8956d75` fear wiring AUDIT PASS, `0179110` progress
   instrumentation AUDIT PASS, `2024c23` production sweep + analysis + 9-curve poster
   figure — **this last step is UNGATED**, see `okf/status.md` and `EVIDENCE.md`). ER vs
   GIRG at matched ⟨k⟩ is included for free: all three families share ⟨k⟩=4.53.
   **Result: geometry barely moves ignition** (GIRG ~11.7% above CM at $\bar\mu=0$, vs a
   ~30× gap to ER from heterogeneity alone) — see `okf/open-questions.md` Q6.
   ⚠️ **Housekeeping left open:** the isolation worktree for C3b-obs is still checked out at
   `/Users/garymei/Downloads/projects/tc-work` (branch `c3b-sweep-progress`) — clean, but
   never removed. Run `git worktree remove` (or archive it) once nothing depends on it.
3b. ✅ **DONE (S-066, 2026-08-06) — AUDIT PASS.** Blind reviewer (×3) → critic (×3) →
   auditor gate run on all three poster analysis pipelines; record in
   `walkthrough-s066-preprint-gate.md` (`d90493f`), narrative in
   `okf/changes/s-066-*.md`. Comparison 2, the famcompare interleave (D-042), and the
   percentage-decrease panel (D-040) are now VERIFIED — the "cite as strong preliminary"
   restriction is lifted; Q9's fourth hook (hubs-not-distance) may now carry weight
   alongside the original three AUDIT-PASS hooks.
4. **Frame Q9 — the ISyE recommendation component.** Still open; independent of compute, so
   it can proceed **immediately** now that items 2 and 3 are both done rather than only one.
   Three candidate hooks, each an existing AUDIT-PASS result restated as an intervention: the
   **ignition gate** (τ=3.5 → 0/3000 trials, i.e. structural immunity to bounded shocks),
   **tilt monotonicity** (calming the hubs beats calming the leaves), and the **local-vs-global
   fear dichotomy** (localizing panic removes its systemic effect entirely). A fourth,
   lower-confidence candidate is now available from Comparison 2 (`2024c23`, UNGATED): *hubs,
   not distance, set the threshold* — degree heterogeneity moves ignition ~30×, geometry only
   ~12%, which argues policy attention belongs on high-degree nodes regardless of their
   physical/network position. Build the panel from AUDIT-PASS results first; treat the fourth
   hook as supporting color, not the load-bearing claim, until C3b clears a gate.
5. **Poster draft.** `okf/poster/poster.tex` (11KB as of `2024c23`, 2026-08-02) now has the
   Better Poster template, the 9-curve hero figure, the §5.4 engine disclosure, and both
   comparisons narrated. Blocked only on item 4 (Q9 panel) for the closing section — items 2
   and 3 that used to block the figures are done.
6. **SNAP teaser.** Download one SNAP dataset, apply the framework, check qualitative match
   against the inhomogeneous with/without-geometry expectations. No evidence of work started
   on this in the 2026-07-27–08-02 sprint. Independent of everything above; also the empirical
   leg of the post-poster frontier push.
7. **Optional — hard RGG dimension sweep.** Keep increasing dimension D and see whether the
   results change. Advisor's nice-to-add, not core. No evidence of work started.
8. ✅ **DONE (S-066) — model schematic added (D-046).** New
   `scripts/plot_model_schematic.py` → `results/figures/model_schematic.png`
   (deterministic hand-placed drawing, no RNG; wide-short ~2.9:1 so it fits the left
   column). Red = failed (advisor's directive), rust ring ∝ fear level $f_i$ (distinct
   encoding), teal = healthy — palette identical to poster.tex's tcRust/tcTeal/tcCream.
   Placed under "Our Model", annotating both activation routes.
9. ✅ **DONE (S-066) — motivating sentence added (D-046).** New "Goal" section states it
   explicitly: real networks have hubs and locality, the baseline has neither; in addition
   to the baseline we need to model fear's effect on networks *with* heterogeneity and
   geometry.
10. ✅ **DONE (S-066) — baseline-first narrative restructure (D-046).** Left column now
    runs The Baseline (who uses it, why it IS the baseline) → Our Model (+ schematic) →
    Goal → What We Look For — the advisor's linear arc. **Layout consequence flagged for
    Gary:** the giant QR box could not coexist with the schematic + Goal section in the
    left column (verified by tectonic compile — it fell off the page); the QR box moved to
    the bottom-right corner under Next Steps at 0.30 column width (~2.7 in printed, still
    conversation-distance scannable). Restore the left-column giant QR only by cutting
    something else. Full-bleed hero untouched.

**Carried over (deprioritized under the poster):**

C1. **Restructure `.lavish/advisor-explainer.html` (Gary's plan, 2026-07-21).** Unchanged since
   S-059 — no evidence this was touched during the poster sprint. The card-by-card walkthrough
   is complete; corrections are applied but stacked as annotation blocks, hard to read. Source
   of truth: `okf/cache/advisor-explainer-walkthrough-2026-07-21.md` (temporary — delete after).
   Design cue: four inverted quantities (τ, ν, two decay slopes), lead each card with a
   plain-language verdict line (see `okf/lessons.md` §5, S-059). The site's known cosmetic issue
   (hero `<h1>` ~5px clip; fix `line-height: 1.12 → 1.24`) can be folded in if the site is ever
   rebuilt — it served its meeting purpose 2026-07-22.
C2. **Task Z — widen the γ grid on the tilt experiment.** Unchanged since S-059. C-Q4(i) has
   only **three** γ points (−1, 0, +1) and they show a clearly **saturating** shape: at μ̄=0.4
   the empirical critical seed runs 8.00 → 5.83 → 5.41, so γ=−1→0 buys 2.17 seeds while γ=0→+1
   buys only 0.42. Three points cannot tell a saturating curve from a kink, a plateau, or an
   eventual reversal — **the same "too few grid points" trap that produced the retracted Θ(1)
   claim** (Task S/W; also the trap Comparison 1's pilot #5 explicitly avoided by going to five
   points). Proposed: γ ∈ {−2, −1.5, −1, −0.5, 0, +0.5, +1, +1.5, +2} at τ=2.5, n=10000, paired
   on `base_seed=42`, across the existing μ̄ rows. Config-only, no `src/` change, autonomous-safe.
   ⚠️ **Two things this task must check, not assume:** (a) at large **positive** γ the ε-cap
   becomes binding again — the very bug Task Q fixed; the water-filling path handles it, but every
   cell must report `stats["realized_mu_bar"]` against nominal and flag cap-affected rows before
   any comparison (see `okf/lessons.md` §1). (b) At large **negative** γ, any degree-0 node gives
   weight ∞; `d_min=2` prevents this for the *drawn* sequence, but erasure can realize degree 0,
   so confirm the fear sampler is fed drawn degrees, not realized ones.
C3. **Task AA — fear-only percolation: does the critical seed scale like θn(1−μ̄)?** Unchanged
   since S-059. Gary's design (2026-07-21), from the μ̄-sweep result. Disable solvency entirely
   (`r = n+1`, or `r = 10⁹` as the pilot used) so the fear channel runs alone, then sweep the
   **seed size a** against μ̄ and n. **This has a derivable prediction, so it is a test and not a
   fishing trip.**
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
   - **The exogenous-`g_0` variant has its own, cleaner prediction. Full derivation, so it is not
     re-derived next session:**
     - Round 1: nobody has failed; each bank fails w.p. `f_i·g_0`, and `E[f_i] = μ̄`, so
       `A₁ = n·μ̄·g_0`.
     - Round 2: the field is now `g₁ = A₁/n`, giving `n·μ̄·(A₁/n) = μ̄·A₁`.
     - Round k: `μ̄^(k−1)·A₁`. Each round is `μ̄` times the last — a shrinking geometric series
       because `μ̄ < 1`.
     - Total over the cascade: `A₁/(1−μ̄) = n·μ̄·g_0/(1−μ̄)`.
     - Systemic at θn ⇒ cancel the n ⇒ **`g_0* = θ(1−μ̄)/μ̄`**, **independent of n** (g_0 is
       already a fraction).
     - **Reading it:** `1/(1−μ̄)` is the **amplification factor** — one initial failure ultimately
       causes that many in total (μ̄=0.5 → 2, μ̄=0.9 → 10, μ̄=0.999 → 1000). `g_0*` is just "how big
       a push, given the push gets amplified this much." The `(1−μ̄)` on top is the amplifier
       inverted; the `μ̄` underneath is round 1 being weaker when banks are less afraid.
     - Same physics as the a-sweep expressed as a fraction not a count (`g_0 ≈ a/n`), with n scaled
       out — the better-posed version, and a plausible model of a pure news shock: everyone
       frightened, nobody actually failed.
   - **Suggested `g_0` grid — bracket the prediction, don't use a fixed grid** (it moves with μ̄, so
     a fixed grid wastes most cells). Roughly 0.25× to 4× of `g_0*` per row:

     | μ̄ | predicted `g_0*` | sweep range |
     |---|---|---|
     | 0.5 | 0.500 | 0.12 – 1.0 |
     | 0.7 | 0.214 | 0.05 – 0.86 |
     | 0.9 | 0.056 | 0.014 – 0.22 |
     | 0.99 | 0.0051 | 0.0013 – 0.020 |
     | 0.999 | 0.0005 | 0.00013 – 0.0020 |

   - ⚠️ **`g_0*` is a lower bound and a scaling prediction, NOT a point forecast.** Expect the
     measured value to land **above** it, for two reasons: (a) **depletion** — the derivation
     assumes an unlimited pool of banks to frighten, but once half have failed the remaining pool
     is halved and effective amplification drops; θ=0.5 is exactly where this bites hardest, so the
     formula is optimistic. (b) **skew** — near threshold the outcome distribution is heavily
     skewed (most runs die early, a few run away), so mean-at-threshold still implies a low
     *probability* of threshold; this is the same effect that produced 0/1000 at μ̄=0.999, a=2.
     **The result is not whether the number matches** — it is whether measured `g_0*` tracks
     `(1−μ̄)/μ̄` as μ̄ varies, and whether it is genuinely independent of n. Do not record a
     measured value above the formula as a failed prediction.
   - ⚠️ **"Activate the whole graph" is not θn.** Cascades in this model stop well short of the
     structural ceiling — measured max 0.732 (μ=0) and 0.8975 (μ̄=0.4) against a ceiling of ~99.8%
     — so "whole" may be unreachable at any g_0. Decide up front whether the target is θ=0.5 or a
     Janson-style n−β, and see the open question in
     `okf/handoff-lavish-explainer-session.md` before designing against "whole".
   - **Post-meeting status (2026-07-22):** the meeting resolved the publication route without
     needing this card played (D-038). Task AA is now the leading candidate for the
     **theoretical leg** of the frontier push — clean derivable prediction, obvious empirical
     hook — but it sits *behind* the poster queue (items 1–7). No evidence it moved during the
     poster sprint.
C4. **Task Y — largely invalidated 2026-07-21; rewrite or retire before running.** Unchanged
   since S-059. The queued discriminating test (front-loaded kernel `[1,0,0,0,0]` vs uniform
   `[0.2×5]`, predicting a ~5× change in multiplier−1) **does not discriminate.** Exploratory
   paired pilot, n=4000, μ̄=0.4, 400 trials/arm: uniform **0.147**, front-loaded **0.110** — no 5×
   effect, if anything the opposite direction (Fisher p=0.14, so read as "no effect", not a
   reversal). Cause: both kernels have Σwₖ=1, so total fear offspring is identical (D-006
   kernel-mass invariance); the transient w₁ argument does not survive a multi-round cascade with
   permanent failures and cumulative neighbour counts. ⚠️ `docs/queue/task_Y_fear_multiplier_mechanism.md`
   still carries the pre-registered 5× prediction and **needs an appended correction** before
   anyone picks it up. **What survives:** the n-cancellation `n·μ̄·(Σwₖa/n) = μ̄·Σwₖa` holds for
   *any* kernel, so "why is the multiplier flat in n" is answered by algebra and needs no
   experiment. **The one salvageable test:** the sketch predicts the multiplier is *linear* in μ̄
   (`1 + 5.3·μ̄`, R²=0.98 on four points) — extend the ignition μ̄-grid to 0.5/0.6/0.7 and see
   whether it stays linear or bends. Pilot is exploratory: nothing stamped, nothing committed,
   **not** a §5.6 result.
C5. **Optional future — Task R Option B (supra-r_n cross-round test).** Unchanged since S-059.
   The *only* valid way to actually test C-Q5(i) cross-round spatial correlation is a supra-r_n
   cross-type statistic (pair-correlation g(d) / Ripley cross-K between early- and late-round
   remote-nucleus centroids at d ∈ (r_n, k·r_n]). Deferred (D-035); pick up only if the advisor
   wants a cross-round correlation probe. Task O's cross-round lower-bound caveat stays OPEN
   until then.
C6. **Queue hygiene — the queue is empty; S/T/U/V/W all closed.** Unchanged since S-058/S-059.
   `d70dbd8`'s commit body records V, W, and U as having cleared `/verify` (reviewer sign-off,
   critic PASS, AUDIT PASS). S and T have no gate of their own but were **superseded** by W,
   which was gated: S's ignition series is now the 6-point run to n=160000, T's ν fit is now the
   7-point fit above. Residual caveat: U's and W's task files asked for a *human* at the gate and
   got a blind one — a process gap, not an ungated result. ⚠️ Closure records for these tasks
   live in **commit bodies and `okf/changes/`**, not in `docs/queue/reports/` — a missing report
   file does not mean a task is open (this misread cost a session).

**Resolved 2026-07-27–2026-08-02 (this catch-up; see `okf/changes/s-061-*.md`, `s-062-*.md`):**
- Items 1, 2, 2b, 2c, 3 above (Comparison 1 and Comparison 2, both matched-degree poster
  comparisons) — full detail in the items themselves, not repeated here.

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
  cross-round question stays OPEN (Option B is the valid test — item C5). Supersedes the
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
