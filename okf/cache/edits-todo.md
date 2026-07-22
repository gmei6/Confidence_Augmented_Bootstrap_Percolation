---
type: Cache
title: "Edits TODO — deferred until experiments/runs finish"
description: "Pending edits Gary queued that depend on a running experiment or subagent. Apply only AFTER the named blocker completes. Remove each item once applied."
mutability: live
tags: [todo, deferred, advisor-update, experiments-redesign]
---

# Edits TODO — deferred until experiments/runs finish

Queued edits that must NOT be applied yet because they depend on an experiment/subagent
still running. Each item names its blocker. Delete the item once it is applied. Delete the
whole file once it is empty.

## 1. Experiments redesign — Card 1 (Config model, experiment #2 "shock snowballs on unequal net")

**Blocker:** the P(systemic) = f(τ, μ) equation-fitting subagent (τ = power-law degree-tail
exponent; μ = mean fear). Apply these to `advisor-update-2026-07-22/index.html` §experiments
(and/or the mock `.lavish/experiments-redesign.html`) once that run is done.

Source: Gary's Lavish annotations on `.lavish/experiments-redesign.html` (2026-07-22).

- **Rewrite the hypothesis in general terms.** Current text pins specific values (bounded seed
  a=r=2; τ=2.5<3 heavy tail → ignites; τ=3.5>3 light tail → never). Gary will restate it
  generally: **heavier tails (smaller τ) are more likely to cause a cascade; lighter tails
  (larger τ) less likely.** — *Gary will write the final wording himself after the run.*
- **Remove the table.** The "SERIES …" data table on this card goes away entirely once the new
  experiment is run.
- **Replace it with one large plot.** Single figure: **x-axis = mean fear (μ), y-axis = τ,
  colors = different values of n.** Then fit an equation to all datapoints (the subagent is
  producing the (μ, τ, n) critical-boundary points for exactly this).
- **Additional notes:** Gary will edit the "Additional notes" block later, after the run.

**Subagent result (2026-07-22) — equation DELIVERED, preliminary/uncommitted.** The
P(systemic)=f(τ,μ,n) subagent produced exactly the card-1 target plot (x=μ, y=τ_c critical
boundary, one curve per n, fitted). Plots + data in scratchpad
(`boundary_fitted.png`, `heatmap_psys.png`, `p_surface_table.csv`, `boundary_p50.csv`,
`fit_summary.txt`). Fitted equation:
`τ_c(μ,n) = 2.63 − 0.096·log₂(n/2000) + 0.96·μ²` (R²=0.97; boundary rises quadratically in μ,
linear term ≈0; each n-doubling lowers τ_c ~0.10). Full-surface logistic collapse
`P=1/(1+exp((τ−τ_c)/w))`, w≈0.11, R²≈0.91–0.93.
- **NOT a contradiction (checked 2026-07-22): the equation (a=8) and card 1 (a=2) are different
  seed regimes.** Card 1's "ignites" = P(systemic) being *nonzero* (status.md: "τ=3.5 never
  ignites 0/3000; τ=2.5 ignites in every cell"; figure = small declining ignition probabilities).
  So card 1 is a nonzero-vs-exactly-zero GATE at a sub-critical seed a=2 — the subagent's a=2
  P≈0.03 (heavy τ=2.5) vs 0 (light τ=3.5) CONFIRMS it. a_c≈5–8 (γ-tilt card) is consistent
  (a=2 is below critical). The equation lives at a=8 (near-critical, full 0→1 transition).
- **PLAN (pending Gary's ok): keep card 1 as the a=2 gate with generalized wording; put the
  a=8 equation on its OWN new card** ("Where the cascade boundary sits"), tagged preliminary /
  a-specific / pending §5.6 gate. Do NOT fold the a=8 equation into the a=2 card.
  - Proposed card-1 hypothesis rewrite: "Heavier degree tails make a network more prone to
    systemic collapse; lighter tails make it more resistant. At a bounded seed (a=r=2, below
    the critical seed size), this appears as a sharp gate: a heavy tail (τ<3, infinite-variance
    degrees / big hubs) leaves a nonzero probability of a systemic cascade, while a light tail
    (τ>3, finite variance) shuts it to exactly zero."
- **⚠ Not yet a result:** ran from scratchpad, git `dirty-or-unknown`, not in `results/`; the
  constant-width collapse underfits (χ²/dof≈34–37 — near-step at μ=0, broad at high μ). To
  promote: commit the 28 configs, run from repo root, land raw+figures via the runner, clear
  the reviewer→critic→auditor gate (§5.6/§IV).

## 2. Experiments redesign — Card 2 (Config, γ-tilt, experiment #3) — review notes

Apply when the experiments-redesign mock is ported to
`advisor-update-2026-07-22/index.html` §experiments. Source: Gary's Lavish annotations on
`.lavish/experiments-redesign.html` (2026-07-22).

- **✅ DONE in mock 2026-07-22 (carries to index.html on port).** Moved the "Interpretation:"
  sentence out of the Hypothesis paragraph and into the "Additional notes" details block (its
  own callout, above the Update). Applied to `.lavish/experiments-redesign.html`.
- **Separate the two-panel figure into two graphs; link the ε-compression graph to the
  water-filling explanation in `index.html`.** Gary's idea (2026-07-22): the right "ε-cap
  compression" panel is really an illustration of the clipping bug, not part of the tilt
  result — split it off. Give the ε-compression graph an in-page link to the bug diagram in
  the `#implementation` section; its `<figcaption>` at `index.html:921` is the exact relevant
  spot: "Under a positive tilt the hubs exceed the 1−ε fear ceiling; single-pass clipping
  discards that excess and drives the realized average up to 28% below target, whereas
  iterative water-filling pours the overflow onto the remaining nodes so total fear — and the
  average μ̄ — is conserved." Linking needs a new anchor `id` added to that `<figure>`
  (none today; nearest is `id="implementation"` at line 556). Dovetails with the stale-figure
  item below — the left "boundary vs tilt" panel still wants the post-fix n=10000 regen.
- **⚠ Stale figure — needs a regenerated run.** The card's figure is the **n=4000,
  PRE-water-filling-fix** version (left subplot titled `n=4000`; right "ε-cap compression"
  panel shows γ=+1 compressed / "artifact-suspect", which is why γ=−1 and γ=0 coincide on the
  identity line there while γ=+1 sags). But the card TEXT describes the **n=10000 POST-fix**
  result where γ=+1 is now cap-free and holds — and the img alt-text falsely says "at n=10000".
  The figure contradicts its own narrative. Regenerate a post-fix n=10000 figure (γ=+1 should
  now sit on the identity line in the right panel) before this card ships. [Gary to decide
  whether to regenerate.]

## 3. Experiments redesign — Card 4 (Config, ν / transition width, experiment #5) — figure unclear

Gary (Lavish 2026-07-22): "this graph can be significantly improved; it's unclear exactly
what's going on here." Needs a **figure regen** (matplotlib PNG from `finite_size_r2_*`
results via the runner/analysis script), not just an HTML tweak.

Why it's unclear (log-log w vs n; μ=0 blue ν=5.61±0.18, μ=0.3 orange ν=4.82±0.15):
- The claim (fear narrows the window FASTER with n) is a SLOPE difference, but the two fit
  lines nearly overlap and CROSS at ~n=5000 — the effect is visually invisible; only legible
  from ν in the legend.
- The raw data crosses over: at small n (1000–2000) μ=0.3 sits ABOVE μ=0 (fear WIDENS the
  window — the sign flip), contradicting the headline until you know only the slope is robust.
- ν is inverted (smaller = faster narrowing) — counterintuitive, unlabeled.
- x-tick labels (1000 2000 5000 …) are crowded/overlapping.

Proposed improvements for the regen:
- Lead with a plain-language verdict line, number second (per lessons.md habit): "fear makes
  the tipping window narrow FASTER as the network grows — the effect is in the slope, not the
  width at any single size."
- Make the slope difference legible: e.g. a compensated plot w·n^(1/ν), or slope triangles /
  ν annotated on the lines; annotate the ~n=5000 crossover and state the small-n sign flip.
- Caption that ν is inverted (smaller = faster) and is fit against node count n (no length scale).
- Fix x-tick crowding.

## Open item (not an edit) — no Hard-RGG / Soft-RGG / GIRG comparison experiment exists

Gary asked (Lavish 2026-07-22) whether there's a general experiment comparing Hard RGG, Soft
RGG, and GIRG. There is not. `configs/` and `results/` contain only config-model runs
(`q4_*`, `finite_size_*`, `fear_concentration_*`, `kappa_*`) and the Q5 duration/localized-fear
runs. **No `soft_rgg` or `girg` config/result exists** — Soft RGG is only an implementation-
section diagram (never run); GIRG appears only as the demoted Task P. A controlled model-
comparison (vary only the graph model, hold μ̄/τ/θ/seed grid fixed) is a genuine gap. Gary to
decide whether to formalize it as an open question / new experiment.

## Reference — τ definition (established 2026-07-22)

τ = **power-law degree-tail exponent** of the config-model degree distribution (NOT a threshold).
τ < 3 → heavy tail / infinite-variance degrees → cascades; τ > 3 → light tail / finite variance
→ no cascade for a bounded seed. "Inverted": larger τ = harder to cascade.
