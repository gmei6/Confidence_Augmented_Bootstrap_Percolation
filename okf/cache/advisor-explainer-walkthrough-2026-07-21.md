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
