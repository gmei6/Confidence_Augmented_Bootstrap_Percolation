---
type: Cache
title: "Advisor-explainer walkthrough outcomes (2026-07-21) — per-card corrections"
description: "TEMPORARY. What each card of .lavish/advisor-explainer.html actually says after Gary's card-by-card walkthrough; the source of truth for restructuring the HTML. Delete once the restructure is done."
mutability: live
resource: "file:///Users/garymei/Downloads/projects/CABP/.lavish/advisor-explainer.html"
tags: [advisor-prep, temporary, explainer, walkthrough]
---

# Advisor-explainer walkthrough outcomes (2026-07-21)

**⚠️ TEMPORARY — delete once the HTML restructure is done.** This exists so the restructure
preserves what the walkthrough established. It is not a permanent knowledge artifact; the durable
lessons live in `okf/lessons.md`, the durable decision in `okf/decisions/d-037-*.md`.

**Update 2026-07-22:** a SECOND, unrelated handoff section was appended at the bottom of this file —
the advisor-update *site* diagram work (`advisor-update-2026-07-22/index.html`), a different deliverable
from the explainer. **Do not delete this file until that pickup point is also resolved.**

Gary read the explainer card by card, restating his understanding; each card was corrected against
committed data. Cards 1–3 were covered in a prior session (per the handoff). Cards 4–9 + foundations
were done 2026-07-21. Every correction below is already applied in the HTML.

## Per-card state after the walkthrough

- **Card 4 — clock-collapse shortcut.** Gary read it as "a_k=o(n) is validated." Corrected: the
  card validates the *implication* (if generations are small, the geometric clock ≈ the generational
  clock), **not** the assumption — and the same data shows a_k=o(n) is *false* at the macroscopic
  generations (bias 0.028–0.049 at a/n≈0.5–0.66). Added: which form is the shortcut (the **power**
  form (1−f/n)^a = Janson geometric clock, theory only; the **product** form 1−f·a/n = generational
  clock = what the sim runs, `reference.py:162-164`), and that the substitution buys **independence**
  (not speed — runtime identical). ΔP is a **derived** algebraic gap, not a measured quantity.

- **Card 5 — ν / transition width.** Gary read it as "fear narrows the window." Corrected: ν is a
  claim about the **slope** (rate of narrowing in n), not the width at any fixed n. Per-n table added
  from committed JSON: at n=1000 fear makes the window **16% wider (4.4σ)**; sign flips across n;
  the only robust signal is the slope (ν 5.61→4.82, 3.4σ). Also flagged: **ν is inverted** (larger ν
  = slower narrowing) and is **not** lattice ν (fit against node count n, no length scale).

- **Card 6 — single super-hub. DEMOTED (D-037).** Was "One super-hub is not enough / Negative." The
  outcome is **forced by arithmetic**: single seed → every neighbour has exactly one failed neighbour
  vs r=2 → zero solvency failures possible in round 1 for a seed of *any* degree. Hub degree (1555)
  never enters. `hub fear=1.0` is the seed's own f_i, causally inert. Retitled "Single-seed sanity
  check," tag → "Demoted 2026-07-21," red do-not-present banner. Survives: r≥2 = bootstrap vs
  contagion (one sentence, a property of the rule). Q6 reopened as unanswered.

- **Card 7 — sub-ballistic decay.** Gary first read the slope as "probability of a cascade." Corrected:
  it is cascade **duration** (ballistic ratio T_θ/√(n/log n)); all trials cascaded (600/600). Slope
  runs in **n at fixed μ̄**, not in μ. "Slope decreased" is a sign-trap (−0.291 is *steeper* than
  −0.277). Gary's revised reading ("fear speeds up the collapse") is **correct** and is the sentence to
  carry (≈37 rounds field-free vs ≈12–15 global). Distinction pinned: the *slope* is the decay of the
  duration in n, not the speed itself; needed only for the artifact-ruling-out argument.

- **Card 8 — size-biased rescaling. REFUTED (genuine negative).** Built out in full. μ* = size-biased
  (edge-endpoint) mean fear; conjecture was that matching μ* collapses the γ curves. It **inverts**:
  spread 1.51 (matched μ̄) → 3.11 (matched μ*), ratio 2.05; at matched μ* the tilt ordering flips.
  Caveat: μ* ranges barely overlap, so **magnitude is grid-limited, sign is robust** — lead with sign.
  Value (Gary asked "I don't see the value"): μ* is **what the analytic edge-map forces**
  (`q4_config_model_scoping.md` §5, vdH Vol II / size-biased offspring = Dhara's toolkit), so the
  negative closes the natural one-scalar reduction. Conditional insurance aimed at Dhara; back pocket,
  not a slide.

- **Card 9 — tautological instrument (D-035).** Not yet walked through at time of writing (was next).
  Best card for showing research judgment (Gary caught it). Tie to the D-035 *selection-forced* /
  D-037 *parameter-forced* tautology pair.

## The through-line (for the restructure, and already in lessons.md §5)

Cards 4, 5, 6, 7 were all the **same failure**: a conditional or derived statement presented as a
flat empirical one (implication-for-assumption; slope-for-level; arithmetic-for-finding;
slope-for-speed). And **four inverted quantities** now live on the page — τ, ν, and the two decay
slopes — enough that the durable habit (state the effect in plain words first, let the signed number
follow) is worth making structural in the restructure, e.g. every such card leads with a plain-language
verdict line and only then shows the number.

---

# 2026-07-22 session — advisor-update SITE diagrams (separate deliverable, NOT the explainer)

**Scope note:** everything above is about `.lavish/advisor-explainer.html` (the internal card-by-card
explainer). This section is a *different* file — the professor-facing site
`advisor-update-2026-07-22/index.html` — worked on in the 2026-07-22 session. Kept here at Gary's
request as the pick-up point for a future session.

## ⚠️ OPEN QUESTION to resolve next session — GIRG "circle of range"

Gary's question, looking at the GIRG diagram (Card 3): **does each node have a circle of range within
which it can potentially connect to other nodes?** Deliberately NOT answered in-chat — recorded here to
pick up later. The honest answer needs care, so don't just bolt a hard radius onto the diagram:

- **GIRG has no hard connection radius.** Unlike a Random Geometric Graph (RGG), where a node connects
  to everything inside a fixed radius rₙ, GIRG connects i,j with a *soft, continuous* probability
  `P(i~j) = min(1, (wᵢwⱼ/(n·dist²))^α)` — decays with distance², rises with the weight product.
- **Effective reach scales with weight.** A high-weight hub has a large *effective* range; a low-weight
  node a small one. The closest honest visual is a *soft halo per node whose radius ∝ its weight*
  (≈ the P=½ contour), NOT a uniform hard circle.
- **Confusion risk:** the project's OTHER geometric experiments (Task O / Task U duration runs) DO use
  a "Hard RGG on the unit torus" with a real radius rₙ. A reader could wrongly assume the GIRG diagram
  uses the same hard cutoff. Make the GIRG↔RGG distinction explicit if any range visual is added.
- **Decision to make:** (a) add per-node soft "effective range" halos (radius ∝ weight) with a caption
  saying it's a soft probability falloff, not a hard cutoff; or (b) leave the diagram and add one caption
  line — "no hard radius: a node's reach grows with its weight." Lean (b) for meeting brevity unless
  Gary wants the halo.

## Diagram-building session state (`advisor-update-2026-07-22/index.html`)

**Done & applied to the live `index.html`:**
- Hero simplified (Gary's own edit): eyebrow "Advisor Update", h1 "Changes Since July 1, 2026"; the
  "What has changed" nav moved OUT of the sidebar INTO the hero as a relocated vertical list; page is
  now single-column (no left rail).
- Assumptions hidden by default — every idea-card's Assumptions callout is a collapsed
  `<details class="assumptions">`.
- Three implementation diagrams, hand-authored inline SVG, theme-aware via the site's CSS variables
  (`--accent-cool/-warm`, `--ink`, `--line`, `--bad`, `--good`); reviewed via Lavish
  (`.lavish/impl-diagrams.html`) then copied in:
  - **Diagram 1 — config model** (Card 1, stacked/full-width): 4-stage pipeline — degree-sequence RANK
    plot (heavy tail: one hub bar + long tail; "each bar = one node, ranked by degree") → stubs →
    random pairing → erased graph.
  - **Diagram 2 — degree-tilted fear** (Card 2, stacked): same 7-node net at γ=−1/0/+1; node SIZE =
    degree, node COLOUR intensity = fear; "high" fear fully opaque.
  - **Diagram 3 — GIRG** (Card 3, **two-column card**): unit-torus square, local grey edges + one
    super-hub's warm long-range edges; slim SQUARE SVG on the right, description + Assumptions on the
    left, View-code full-width below.
  - **Bug diagram** (inside Card 2's "Assumptions — and a bug this surfaced, now fixed", hidden by
    default): two-panel before/after of the ε-cap clip → water-filling fix. Drafted by a subagent.
- **Design conventions:** `dg-*` SVG classes driven by CSS vars; **aspect-ratio rule** — square diagrams
  get the two-column card, wide diagrams stay stacked; SVG markers use UNIQUE ids (`dgarrow` for
  Diagram 1, `capArrow` for the bug diagram) to avoid collisions on one page.

**Still open / not yet done:**
- The GIRG "circle of range" question above.
- Subagent flagged: check in a browser whether the green "on target" line reads distinctly from the cool
  "redistributed mass" caps in the bug diagram's right panel (they sit close; may need `--good` bolder
  or a check-tick).
- **Gary is doing a top-to-bottom pass of the site.** Reached & done: hero, implementation-ideas section
  (all 3 diagrams). **NOT yet reviewed:** experiments (9 cards), scope decisions, open questions.
- **Precision findings raised at the START of the session but deferred** (Gary chose to go
  top-to-bottom): (1) hero completeness overclaim — SUPERSEDED, Gary rewrote the hero. (2) **Single-hub
  card (Task P) is still presented as a substantive "Negative" finding on the site, contradicting its
  D-037 demotion to an arithmetic artifact** — decision pending; comes up when the pass reaches that
  card. (3) Task O table needs a "what the number is" caption (values = ballistic *duration* ratio, not
  a probability). (4) ν card: flag that ν is inverted (smaller = faster) and "faster as it grows" is a
  *slope* claim, not a level claim. (5) Task X size-biased: the ratio 2.05 is grid-limited — lead with
  the sign, caveat the magnitude.

**Lavish review file:** `.lavish/impl-diagrams.html` (session was still open at time of writing).

---

# 2026-07-22 (continued) — implementation section DONE; experiments section redesign IN PROGRESS

## Resolved since the section above
- **GIRG "circle of range" → RESOLVED.** Took option (a) but it evolved: soft halo → (Gary: "hard to
  see") → **discrete two-band rings** (firm inner core w/ solid outline + faint outer band w/ dotted
  outline, radius ∝ weight) → **solid-filled nodes** so node vs range is unambiguous. Caption: banding
  is illustrative, true falloff is smooth, **no hard radius**.
- **Implementation section restructured & APPLIED to `index.html`.** Gary's insight: GIRG = geometry ×
  power law. Deleted BOTH the standalone "Geometry" card and the old "GIRG geometry" card; replaced with
  ONE **"GIRG Model: Geometry × Power Law"** build-up card = 3 sub-cards (1. Geometry — continuous
  distance, no rₙ; 2. Power Law — heavy-tailed weights; 3. Combine — soft P(i~j) gradient fields) +
  collapsed **Assumptions** + **View code (`girg.py`)** + **"Previous geometry models"** (Hard RGG
  pipeline, enlarged ~1.5×, with a blocked-connection + X on an out-of-radius node; + Soft RGG).
  CSS added: `.sub-card/.sub-headline/.formula-block/.dg-onode-fill/.dg-hub-fill`/generic `.split`;
  `dg-localedge/longedge` → dashed. Also **fixed a pre-existing unclosed `<details>`** in the tilted-fear card.
- **Task P / single-hub (D-037): APPROVED to REFRAME, not remove.** Retitle "single-seed sanity check",
  tag Negative→**Demoted/artifact**, add the arithmetic reason (single seed + r=2 → every neighbour has
  exactly one failed neighbour < threshold → zero round-1 failures for ANY degree; hub deg 1555 never
  enters), state the hub question is **open**. Keep the card (it's the only GIRG experiment).

## Workflow (to conserve Gary's 5-hr usage) — memory `feedback_antigravity_diagram_division`
1 discuss → 2 Claude writes an Antigravity prompt → 3 Gary workshops it with Antigravity → 4 Gary pastes
the Lavish link, **Claude READS the `.lavish/*.html` file directly** (not the 127.0.0.1 URL) → 5 Claude
reviews → 6 Claude applies to `index.html`.

## Experiments section redesign — IN PROGRESS (Antigravity mock built, NOT yet reviewed/applied)
Four changes: (1) group by graph-model (2×2), (2) uniform card template, (3) Task P reframe, (4) filter-
by-model. **Antigravity mock:** Lavish session `http://127.0.0.1:4387/session/40b713f5e659dfea`
(file: likely `.lavish/experiments-redesign.html`). The full Antigravity prompt was written in chat.

### The 2×2 grouping (two independent knobs: power-law degree? × geometry?)
- **ER / p-edge:** no runs — baseline, mention only.
- **Config model** (power-law, no geometry) — 5 cards: 2, 3, 4, 5, 8.
- **Geometric Hard RGG torus** (geometry, no power-law) — 3 cards: 1, 7, 9.
- **GIRG** (both) — 1 card: 6.

### Experiment → model → status MAP (verbatim content must be preserved on apply)
| # | Question (short) | Model | Status |
|---|---|---|---|
| 1 | Global panic speeds collapse; local doesn't | RGG torus | Confirmed |
| 2 | Shock snowballs on unequal net, not even one | Config | Confirmed |
| 3 | Concentrate panic on hubs eases ignition (γ-tilt) | Config | Confirmed |
| 4 | Clock-collapse shortcut = negligible error | Config* (analytic shortcut) | Confirmed |
| 5 | Panic sharpens tipping point faster w/ n (ν) | Config | Confirmed (ν inverted; slope not level) |
| 6 | Super-hub alone not enough (Task P) | GIRG | REFRAME → Demoted (D-037) |
| 7 | Global panic outruns collapse front (sub-ballistic) | RGG torus | Confirmed |
| 8 | Size-biased μ* doesn't unify tilt curves | Config | Negative (sign robust, magnitude grid-limited) |
| 9 | Re-ignition test structurally incapable | RGG torus | Open (D-035, retired) |

### Card template & filter
- Template: `[title/question] → [status tag] → [description + graph/table]` (two-col if square figure,
  stacked if wide) `→ [View code, collapsed] → [Additional notes, optional]`.
- Filter: pills at section top — **All / Config model / Geometric (RGG) / GIRG** — vanilla self-contained
  JS, `data-model` attr on each card.

## ▶ PICK UP HERE next session
1. **Gary has a NEW idea to discuss with Antigravity** (unstated at cutoff — capture it first).
2. **Review the Antigravity experiments-redesign mock** (session above): check (a) content is VERBATIM
   from `index.html` (stats / figures / base64 / View-code byte-for-byte — no drift), (b) Task P reframe
   is correct, (c) the filter actually works, (d) grouping matches the map. Then **apply to
   `index.html` section#experiments**.
3. Cosmetic backlog: enlarged RGG pipeline titles clip ~8–17px at narrow width (fix = 1.3× if real);
   plus site-wide pre-existing diagram overflow (config-model diagram, bug diagram, header h1) — optional
   cleanup pass, Gary's call.

---

# 2026-07-22 (SESSION 2) — equation subagent, new boundary card, Hard/Soft/GIRG comparison

**This section supersedes the "PICK UP HERE" list above where they overlap.** The "new idea to
discuss" from item 1 above turned out to be the P(systemic)=f(τ,μ) fit — now done (see below).
Per-card edit detail lives in **`okf/cache/edits-todo.md`** (§1–§3 + open items); this section is
the session narrative + the promotion plan + subagent state.

## What got done this session
1. **Equation subagent — COMPLETE (preliminary).** Fit P(systemic)=f(τ,μ,n) on the config model.
   - τ = **power-law degree-tail exponent** (`graphs.py:3-20 sample_powerlaw_degrees`; NOT a
     threshold, NOT in `reference.py`). μ = mean fear (`reference.py:287-325`, E[f]=μ).
   - **Result:** `τ_c(μ,n) = 2.63 − 0.096·log₂(n/2000) + 0.96·μ²` (R²=0.97; boundary rises
     quadratically in μ, linear term ≈0; each n-doubling lowers τ_c ~0.10). Full 196-cell surface
     collapses onto one logistic `P=1/(1+exp((τ−τ_c)/w))`, w≈0.11.
   - **Artifacts (persist on disk):** scratchpad
     `/private/tmp/claude-501/-Users-garymei-Downloads-projects-CABP/63dbc345-fc33-474c-b9a8-fb607398b31d/scratchpad/`
     — `boundary_fitted.png` (x=μ, y=τ, colored by n), `heatmap_psys.png`, `p_surface_table.csv`,
     `boundary_p50.csv`, `fit_summary.txt`; regen scripts `gen_and_run.py`, `analyze.py`,
     `boundary_fit.py`, `final_plots.py`; **28 configs** + **28 raws** in that scratchpad.
   - **Why PRELIMINARY (not a result):** seed a=8 (NOT a=2); ran from scratchpad, git stamped
     `dirty-or-unknown`, nothing in `results/`; constant-width collapse underfits (χ²/dof≈34 —
     near-step at μ=0, broad at high μ); n spans only ×8; no §IV gate.
   - **NOT a contradiction with card 1:** card 1's "ignites" = *nonzero* P(systemic) (an a=2 gate:
     τ=2.5 nonzero, τ=3.5 exactly 0). The equation is at a=8 (near-critical, full 0→1 transition).
     a_c≈5–8 (γ-tilt card) is consistent (a=2 is sub-critical).

2. **NEW card "Where the cascade boundary sits"** built + inserted into
   `.lavish/experiments-redesign.html` **right below card 1**, tagged **Preliminary** (neutral
   badge), carrying the a=8 equation + `boundary_fitted.png`. Order verified: card1 (a=2 gate) →
   new card → card2 (γ-tilt). Gary approved keeping card 1 as the a=2 gate and putting the
   equation on its own card (do NOT fold a=8 into the a=2 card).

3. **Card 2 (γ-tilt):** Interpretation sentence moved out of the Hypothesis into Additional notes
   (applied to the mock).

4. **`advisor-update-2026-07-22/index.html`:** added `id="water-filling-fig"` to the ε-cap /
   water-filling bug `<figure>` (line 845) so the ε-compression graph can link to it.

5. **Hard/Soft/GIRG comparison subagent — COMPLETE (preliminary; genuine model-difference result).**
   **Headline (matched ⟨k⟩≈10):** `a_c(GIRG) < a_c(Soft) < a_c(Hard)` at every n, gap widening
   (n=2000: 3.1 vs 9.7, ~3×). **GIRG critical seed is n-independent O(1)≈3 (δ=0.06); Hard grows
   ~n^0.45.** The heavy-tailed HUBS drive it (GIRG−Soft large), NOT long-range edges (Soft−Hard
   modest). Fear lowers a_c for all + compresses the curves; geometric locality resists fear more
   than mean-field (1−μ)². Calibration within ~4% of ⟨k⟩=10.
   **Artifacts:** scratchpad `girg-compare/` — `fig2_ac_vs_n.png` (headline), `fig1_psys_curves.png`,
   `fig3_pvsn.png`, `fig4_fear_shift.png`, `ac_table.json`, `scaling_fits.json`, `STATUS.txt`
   (resume-handoff). **GIRG runner diff (+14 lines, `reference.py` untouched) is in an isolated
   worktree `/Users/garymei/Downloads/projects/tc-work-girg`, branch `girg-compare`, UNCOMMITTED.**
   **Caveats:** 40–60 trials only (err ~0.07); **Soft n=2000 skipped** (its far-field loop is O(n²),
   ~110 min — Soft has only a 2-pt trend, needs a vectorized build); GIRG τ=2.5 fixed (not swept);
   μ>0 a_c clamps at the a=2 floor (lower bounds). Design locked with Gary:
   - Models kept as-is: Hard RGG & Soft RGG = homogeneous p-edge (non-power-law); GIRG = the
     power-law member. Generators all exist (`geometry.py build_rgg_adjacency` /
     `build_soft_rgg_adjacency`; `girg.py sample_girg_adjacency`).
   - **GIRG is NOT wired into `runner.py`** → subagent is wiring it in a **git worktree**
     (`../tc-work-girg`). **You must APPROVE that `src/` diff before it lands.**
   - 2×2: {P(cascade)-vs-n, critical seed a_c} × {no fear μ̄=0, with fear}. Seed ∝ each model's
     own a_c; matched mean degree ⟨k⟩ as the fairness control. Output to scratchpad
     `girg-compare/`, no commits, no `results/` writes, no `reference.py` touch.

## ▶ PICK UP HERE (session 3)

### A. PROMOTE the equation to a committed EMPIRICAL result — run WITH A SUBAGENT (Gary approved)
Gary's call: present as an **empirical boundary fit, NOT a law** — skip the μ-dependent-width /
a-sweep / larger-n extra work (not enough time). Spawn a fresh subagent (the scratchpad artifacts
above persist, so point it there) to:
1. Move the 28 scratchpad configs into `configs/` (descriptive names, e.g.
   `q4_psys_boundary_n{2000,4000,8000,16000}_tau{...}.json`).
2. On a **clean git tree**, commit the configs — **locally only; NEVER push, NEVER force**.
3. Re-run the full sweep via the **sanctioned runner FROM REPO ROOT** so each raw is stamped with
   the real git commit hash; the runner writes `results/raw/` (**runner OWNS `results/` — never
   hand-write it**).
4. Regenerate boundary + collapse figures into `results/figures/` via a committed analysis/plotting
   script.
5. Commit raw + figures + script (locally).
6. Write `walkthrough.md` (provenance + result), then run the **§IV gate**: reviewer → critic →
   auditor, each spawned **BLIND and fed only the walkthrough**. Auditor returns AUDIT PASS/FAIL;
   a FAIL blocks. Report the verdict verbatim — do NOT self-certify.
7. Present as an empirical boundary fit with caveats stated (constant-width underfit, a=8-specific,
   finite-n). Do NOT claim a law. Do NOT edit `okf/` (PI records §8/§11 after the gate passes).
   Guardrails: never touch `reference.py`; config model is Python-path only (C++ parity =
   engine-logic identity at μ=0 if the C++ path supports it, else N/A per §5.4).

### B. Hard/Soft/GIRG comparison — DONE (preliminary); decide what to do with it
1. **Review + approve the GIRG `runner.py` diff** in worktree `../tc-work-girg` (branch
   `girg-compare`, uncommitted, +14 lines, `reference.py` untouched). It adds `graph_type=="girg"`
   with Pareto weights (τ=2.5, 2<τ<3 regime). Either commit it (locally, then it's reusable) or
   discard the worktree (`git worktree remove ../tc-work-girg`).
2. **To promote the result to a committed §5.6 experiment:** tighten trials to 200–500 (currently
   40–60); **vectorize `build_soft_rgg_adjacency`** (O(n²) far-field loop caps Soft at n≤1000) to
   get Soft n≥2000; optionally sweep GIRG τ ∈ {2.1, 2.5, 2.9}; raise/relax the a=2 seed floor so the
   μ>0 a_c values stop clamping; run via the runner into `results/raw`+`results/figures`; then the
   reviewer→critic→auditor gate. **Parity note: GIRG is python-engine-only by design — `reference.py`
   and C++ have no GIRG — so §5.4 cross-validation does NOT apply to GIRG cells** (it still applies to
   any gnp baseline). PI records §8/§11 after the gate.
3. The headline (GIRG O(1) seed vs Hard n^0.45; hubs not long-range edges) is a strong candidate for
   the empty "both knobs" GIRG cell of the 2×2 site framing — but keep it flagged preliminary until
   promoted.

### C. Apply the queued experiments-redesign edits — see `okf/cache/edits-todo.md`
- §1 card-1 hypothesis generalization (proposed text ready; equation card already in the mock).
- §2 card-2: separate the two-panel figure; link ε-compression graph → `index.html`
  `#water-filling-fig` (anchor already added).
- §3 ν card (#5): figure regen (diagnosis recorded).
- Then port the reviewed mock → `index.html` `section#experiments`.

### D. Lavish mock state
- `.lavish/experiments-redesign.html` holds the applied changes (new card + card-2 interp move).
  Reopen with `lavish-axi .lavish/experiments-redesign.html` to keep reviewing. No active poll
  left running at session end.

---

# 2026-07-22 (SESSION 3) — Q6 GIRG promotion engine work; STOPPED MID-FLIGHT for a meeting

**Session ended by Gary ("stop everything") with under an hour to an advisor meeting. Nothing was
merged; two long-running jobs were killed deliberately, not because they failed.** Everything below
is the pick-up state.

## Status at the stop

| Thread | State |
|---|---|
| `girg-runner` (GIRG + `seed_sizes`) | **MERGED** to `antigravity` (`bde73a5`, merge `3bfcb9a`). Done. |
| `girg-q6` (Q6 promotion engine work) | Built + verified in worktree, **UNCOMMITTED, NOT merged.** Gary approved the promotion. |
| Q6 full sweep (~19 core-hours) | **Never started.** |
| Boundary-card promotion subagent | **KILLED mid-run.** Last line: "All 22 claim checks pass. Let me look at the figure." Gate NOT completed. |
| `girg-q6` full test suite | **KILLED at 24 min**, no verdict. Re-run before merging. |
| Preliminary badges (boundary card, Q6 card) | Still in place in BOTH `index.html` and the mock. Correct — do not flip without an AUDIT PASS. |

## A. Q6 / D-037 promotion — the engine work (worktree `../tc-work-girg-q6`, branch `girg-q6`)

**Uncommitted.** `git -C ../tc-work-girg-q6 status` shows 2 modified + 13 untracked.

**Three real gaps were found blocking promotion — the middle one matters most:**

1. **The arms were NOT paired through the runner.** `choose_seed` draws from `rng_casc` when seeding
   at random and draws *nothing* when seeding the hub, so a hub arm and a random arm sharing a base
   seed got the same graph and fears but **different cascade noise**. The Q6 card's claim "paired on
   common random numbers" would have been **false** if run through the unmodified runner.
   Fix: new opt-in `sweep.independent_seed_stream` routes seed selection to a 5th RNG stream.
   `SeedSequence.spawn(5)` yields children 0–3 identical to `spawn(4)`, so existing results are
   untouched. **Defaults OFF** — turning it on changes cascade draws for every random-seeded config.
   *Verified:* cascade-stream state matches across arms **6/6** with the flag, **0/6** without.
2. **The primary endpoint was not recorded.** `run_single_trial` returned `(ff, rounds)`; the
   dose–response needs the seeded node's degree. Now returns a 3-tuple; raws gain `seed_degrees`.
3. **⟨k⟩ calibration had no provenance** (pilot solved `w_min` in a scratchpad).

**Files in the worktree:**
- `src/twocascade/girg.py` (+49) — `sample_girg_adjacency_fast`, a vectorised drop-in. Bit-identical
  edges **and** identical stream position vs the reference; 26× faster at n=2000; n=8000 in 1.02 s
  (reference ~33 s). The reference double-loop is untouched and remains the definition.
- `src/twocascade/runner.py` (+42/−12) — the three changes above.
- `tests/test_girg_fast_identity.py` — 22 tests (bit-identity, stream position, `row_block`
  invariance, plus a guard against passing vacuously on two empty graphs). **22 passed.**
- `scripts/calibrate_girg_wmin.py` — `solve` derives `w_min`; `check` re-verifies a committed config.
- `scripts/make_q6_configs.py` — generates the 10 configs; `--check` diffs against disk.
- `scripts/analyze_q6_dose_response.py` — the analysis + figure.
- `configs/q6_girg_n2000_k{5,10,20,40,80}_{hub,random}.json` — 10 configs.

**Verification already done (do not redo):**
- Regression: `fear_concentration_n1000` through old vs new runner → **results identical**, 4 cells /
  4000 trials; only additions are `seed_degrees` and `sweep_parameters.independent_seed_stream`.
- Static validation of all 10 configs against every runner + oracle contract → **zero issues**
  (`p_n = 0.00492458`, `janson a_c0 = 10.3087`, 5 distinct base seeds across 10 configs).
- End-to-end smoke through the real `run_sweep` at 200 trials, ⟨k⟩ ∈ {5,20,80}:
  **0 hub<random violations in 1,800 paired trials** (shared graph ⇒ hub degree ≥ random degree in
  every trial; one violation would falsify the pairing).
- Smoke reproduces the pilot's shape: gap **+0.200 → +0.165 → +0.020** across ⟨k⟩ = 5 → 20 → 80 at
  μ̄=0.5; first two CIs exclude zero, third does not.

**Calibration method was changed mid-session (Gary approved).** Matching the cheap pair-MC estimate of
E[k] left realized ⟨k⟩ ~4% low under τ=2.5, so the bisection now runs on the realized ⟨k⟩ of built
graphs and re-measures on a held-out seed. The acceptance criterion was also changed: a flat 5%
tolerance produced a meaningless **4.949% pass**; it now judges deviation in **standard errors**
(fails above 4σ, default 24 graphs). Spot checks: 1.60σ / 1.17σ / 0.94σ.
Realized ⟨k⟩ runs 1–4% above nominal (5.18, 10.26, 20.38, 40.72, 80.74) — recorded in each config's
provenance. **Quote realized ⟨k⟩ in the write-up, not the target labels.**

### ▶ Q6 pick-up steps, in order
1. `cd ../tc-work-girg-q6 && PYTHONPATH=src python3 -m pytest tests/ -q` — **~25 min**, must be green.
2. Commit the worktree (explicit pathspecs — concurrent git activity has wiped a staged index before)
   and merge `girg-q6` → `antigravity` with `--no-ff`. Gary has already approved the merge.
3. Run the 10 configs through the runner **from repo root** (~1.9 core-hours each, ~19 total).
4. `python3 scripts/analyze_q6_dose_response.py` — it refuses to print numbers if the integrity gate
   fails, so a clean run is itself evidence.
5. §5.4 = **N/A with reason** (C++ has no GIRG). Then the §IV gate. Then §8/§11 (PI only).

### ⚠ Two substantive issues to resolve BEFORE the write-up
- **The "hub" is not a bank.** At ⟨k⟩=80, n=2000 the max-degree node has median degree **1623 — 81% of
  the network**; at ⟨k⟩=20 it is 707 (35%). This is a finite-size property that **grows with n**, and it
  is very likely the real mechanism behind the card's "the effect grows with n" claim (hub arm flat in
  n because hub degree tracks n; random arm decays). Frame the hub arm explicitly as *"the maximum-degree
  endpoint at this n"*, not as a bank, and lead with the pre-registered dose–response. Capping the seeded
  degree so the intervention is comparable across n is a **different experiment** — needs Gary's call.
- **The dose–response may not be monotone at the top**, which would contradict the live card's
  "climbs smoothly with the seeded bank's degree." Smoke run at ⟨k⟩=20: P = 0.588 (deg 256–512) →
  0.382 (512–1024) → 0.357 (1024+). CIs overlap at 200 trials so it is probably noise, but the full run
  must settle it. The analysis script **reports** monotonicity violations rather than asserting
  monotonicity, so it cannot hide this.
- Also structural: the pooled curve's **middle rests entirely on the random arm's upper tail** (the hub
  arm only ever contributes top-end degrees). State this rather than letting the figure imply uniform
  coverage.

**Pre-registration (already in every config's `provenance.pre_registration`):** PRIMARY = P(systemic)
vs seeded-node degree, pooled across arms. SECONDARY = the hub-vs-random contrast. Registering the
contrast as primary would have allowed the stronger dose–response claim to be made post hoc.

**Figure palette (validated with the dataviz validator, do not eyeball):** ⟨k⟩ is ordered → ordinal
blue ramp `#86b6ef,#5598e7,#2a78d6,#1c5cab,#0d366b` (passes monotone L, adjacent ΔL, light-end
contrast, single hue). Hub accent `#eb6834` vs `#2a78d6` passes all-pairs (CVD ΔE 24.7 protan,
normal-vision 33.6).

## B. Boundary card (τ_c(μ,n) at a=8) — promotion INCOMPLETE, agent killed

- **Configs and scripts were already committed** before this session (all 28
  `configs/q4_psys_boundary_*.json` + `scripts/{run,analyze}_q4_psys_boundary.py`, commit `dce2bbb`) —
  §A step 1–2 of the session-2 plan is **done**; that plan is stale on this point.
- The killed agent left **untracked** `walkthrough-q4-boundary.md` and
  `scripts/verify_q4_psys_boundary_figure.py`, and reported *"All 22 claim checks pass"* before being
  stopped. **Unreviewed — treat as a draft, verify independently.**
- Also untracked and unexplained at the stop: `gen_svgs.py`, `parse_cards.py` (repo root). Identify
  before committing anything broadly; **never `git add -A`**.
- **Still to do:** regeneration check from repo root, figure via committed script, §5.4 recorded N/A
  with reason, then critic → auditor (an earlier blind **reviewer pass already completed**).
- **Do not claim a μ-dependence.** The linear-in-μ term is **−0.030 ± 0.119**, consistent with zero.
  Reproduced fit: a₀ 2.6295, c −0.09607, D 0.96039, R² 0.96964, χ²/dof 33.70.
- `.gitignore` excludes **all** of `results/`. A previous agent force-added 34 files and it had to be
  undone. Raws + figures stay on disk, regenerable from committed configs + seeds. **Never `git add -f`
  under `results/`.**

## C. Repo hygiene at the stop
- Worktrees alive: `../tc-work-girg-q6` (girg-q6, **keep**), `../tc-work-girg-runner` (girg-runner,
  **merged — safe to remove**), `../tc-work-girg` (girg-compare, from session 2, still undecided),
  `../CABP-phase3-restructure`.
- `okf/cache/edits-todo.md` is **stale**: its §2 and §3 are both done. §1 (card-1 hypothesis
  generalisation) is still open — **Gary said he would write that wording himself.**
- The site `advisor-update-2026-07-22/index.html` is **committed and clean** at `a1e256e`, 11 cards,
  Q6 card present in the GIRG group badged Preliminary. Meeting-ready as-is.
