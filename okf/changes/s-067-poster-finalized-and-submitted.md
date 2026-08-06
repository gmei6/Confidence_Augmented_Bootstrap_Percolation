---
type: Session Change
title: "S-067 — Poster finalized and SUBMITTED; ext2 arms; probability panel; demo-site schematic"
mutability: append-only
timestamp: 2026-08-06T16:30:00-04:00
tags: [poster, submission, famcompare, ext2, demo-site, d-046, d-047]
---

# S-067 — Poster finalized and SUBMITTED (2026-08-06, same-day deadline)

Continuation of the S-066 session (same conversation, post-gate). Commits
`0a3330d`, `e54eec5`, `2bc712c`, `eb8d174`, pushed.

## Arc

1. **D-046 items 8-10 implemented** (`0a3330d`): model schematic
   (deterministic hand-placed drawing, new `scripts/plot_model_schematic.py`),
   motivating sentence, baseline-first restructure — then iterated under
   Gary's live direction:
   - Schematic moved OFF the poster to the **demo site's landing screen**
     ("I'd rather have it on people's phones") — site variant in the site's
     own state vocabulary (teal standing / rust failed-by-neighbours / plum
     failed-by-fear, no rings), deployed via Pages on push (`eb8d174`).
   - Gary rewrote the poster in Overleaf (new headline; Existing Work /
     My contribution / How is fear defined? / What We Look For; big stacked
     QR bottom-right; How To Intervene + Next Steps cut from print).
     Reconciled with fixes: `famcompare_probability` figure wired in, ER
     legend entry restored, "Bubs" typo, honest windowed g_t definition,
     Erd\H{o}s--R\'enyi macro-form glyph fix (bold sans drops precomposed
     ő/en-dash), stale comments swept.
2. **ext2 experiment** (`e54eec5`, Gary/Antigravity-driven, reviewed in
   session): famcompare μ̄ ∈ {0.8, 0.9, 1.0} at a=2 for CM-matched, GIRG,
   ER-bounded; own base_seeds 20260806/07/08 (RNG-collision-safe);
   provenance guards extended per the S-066 architecture; μ̄=1.0 safe via
   reference.py's mean_fear==1.0 guard. Headline: **ER-bounded first
   ignites at μ̄=0.8 (9/500), 7.6% at 0.9, 25.6% at 1.0** — "fear cannot
   start what structure forbids" now has a measured boundary. New
   `plot_famcompare_probability.py` panel replaced the famcompare_ratio
   multiplier panel on the poster (the ≥26×/6.6×/8.3× claims move to the
   spoken script).
3. **D-047**: printed §5.4 engine-split disclosure deliberately omitted
   (audience legibility, Gary) — overrules the S-066 audit's carried
   condition by recorded decision; disclosure lives in poster.tex comments
   + the presentation script; papers must restore it.
4. **Presentation script** (`okf/poster/presentation-script.md`, new):
   full talk in the D-046 arc, mechanism stated honestly (per-round
   Bernoulli f_i·g_t, windowed g_t), panel beats synced to the final
   layout, spoken-only material marked (intervene anchors, ν, disclosure,
   multiplier numbers, SNAP next-step).
5. **SUBMITTED**: Gary compiled in Overleaf and submitted
   (`twocascade_poster_overleaf__17_.pdf`); the exact submission PDF passed
   the text-presence gates in-session (ligature-aware).

## Layout-fitting war (methodology notes, see lessons)

Five compile-measure-verify rounds, Sonnet-delegated per Gary's standing
delegation rule. Two failure modes found and named: (a) a clean pixel
margin can be inter-line leading before a line that fell off-page —
pdftotext on the compiled PDF is the ground truth for "did it fit";
(b) a two-child box's height is max(children) — dialing the shorter child
is a dead dial; identify the tall side first.

## Evidentiary map after this session

- Hero + Fear-and-Structure pipelines: S-066 AUDIT PASS, still printed.
- famcompare ratio pipeline: AUDIT PASS but no longer printed.
- Probability panel + ext2: script-level self-checked, guard-protected,
  NOT blind-gated — disclosed in poster.tex comments. If this panel is
  ever pre-printed/published, run it through a verify gate first.

## Open threads for next session

P4 pytest smoke + stale cpp build-cache removal; worktree cleanup;
gate-advisory hygiene batch; runner.py metadata gap (own gated session);
SNAP teaser; ext2/probability panel verify gate if it outlives the poster.
