---
type: Session Change
title: "S-061: Comparison 1 (heterogeneity: ER vs configuration model) delivered end to end — five poster pilots, D-012 departure now a five-point trend"
description: "Reconstructed catch-up entry (backfilled 2026-08-03) for the 2026-07-27 through 2026-07-29 poster-sprint work on D-038 Comparison 1: ER wired into the runner, matched-degree calibration, five Antigravity-driven pilots, and pilot #5's closure of the previously half-finished analysis. D-012 reproduces on ER and the configuration model's departure from it is now a monotone five-point trend, not one point."
mutability: append-only
timestamp: 2026-07-29
tags: [poster, comparison-1, heterogeneity, d-012, d-038, antigravity, backfilled]
---

# S-061: Comparison 1 (heterogeneity) delivered — backfilled catch-up entry

**This entry is a reconstruction, not a same-day record.** It was written 2026-08-03 from
commit bodies and `.agy/` artifacts, per the S-058/S-059 lesson that closure is recorded in
commit bodies and not reliably surfaced elsewhere. The work itself happened 2026-07-27–07-29.

## What happened, in commit order
- `9f3cc17` (2026-07-27): Better Poster LaTeX template landed (`okf/poster/`); Task T1
  matched-degree calibration (`scripts/calibrate_matched_degree.py`,
  `results/processed/matched_degree_calibration.json`) — ER and CM both matched to
  ⟨k⟩=4.533 at n=10000.
- `746b588`, `e58d429`, `74c9744` (2026-07-27): pilot #2 (per-family seed grids, μ̄=0.7 arm,
  a/a_c axis), a delegated 50-trial T2–T4 pilot, and a matplotlib-version reproducibility fix
  for the comparison figure.
- `68adadb` (2026-07-27, pilot #3): seed grids relocated using D-012's
  $a_c(\bar\mu)=a_c(0)(1-\bar\mu)^{r/(r-1)}$ anchored on each family's own measured μ=0
  crossing (rather than guessed), 200 trials/cell. First read: D-012 reproduces on ER
  (ratios 0.93/1.00/1.09 at μ̄=0/0.4/0.7); CM departs monotonically (1.00/1.87/4.16). ER still
  under-resolved (1–2 interior points).
- `301d560` (2026-07-27, pilot #4): per-curve linear ER grids, 500 trials/cell, Wilson-propagated
  crossing intervals, explicit structural-floor flag. All six curves (ER/CM × μ̄∈{0,0.4,0.7})
  clear ≥3 interior points for the first time. Ratios: ER 1.000/0.983/1.092, CM
  1.000/1.839/4.636 (the 4.636 flagged BELOW r=2). K(n) finite-size inflation: 1.49 (n=1000) →
  1.289 [1.280,1.298] (n=10000). The μ̄=0.4 CM point (ratio 1.839, clear of the floor) is the
  one clean departure point at this stage — three points cannot rule out a kink (Task Z
  caution, `okf/next-actions.md` C2).
- `d9edf19` (2026-07-29, pilot #5): the Antigravity session for this pilot **timed out**
  (`.agy/poster-pilot5/stderr.txt`: `Error: timeout waiting for response`) before analysing
  its own six sweeps — mirrored in the pre-catch-up `okf/status.md`/`next-actions.md` as
  "Pilot #5 is HALF-FINISHED." **This same commit closes it**: it commits the six pending raws
  (μ̄∈{0.1,0.2,0.3} × ER/CM, 500 trials/cell) and the re-derived 12-curve analysis. Result:
  ER tracks D-012 flat across the whole range (ratios 0.987/0.976/0.978/0.983/1.092 at
  μ̄=0.1/0.2/0.3/0.4/0.7); CM departs **monotonically** (1.128/1.248/1.514/1.839 at
  μ̄=0.1/0.2/0.3/0.4). Five points in one direction settle what three points could not.
  μ̄=0.7 stays EXCLUDED on CM (predicted 0.92 seeds, below r=2).

## Verified in this catch-up, not just read from the commit message
Per the S-058 lesson ("a present raw file does not mean a task is closed"; a script's success
message does not prove a file was written), this catch-up independently checked:
- `results/processed/poster_comparison.json` mtime (2026-08-02, later updated again by S-062)
  and its `metadata.source_raws` list against the raw files it claims — consistent at the
  `d9edf19` state (verified via `git show d9edf19 --stat`, not just its message).
- `results/figures/scaling_law_departure.png` **exists** with mtime 2026-07-29 13:03, matching
  `d9edf19`'s claim that the previously-missing figure was generated, not merely queued.

## Known, explicitly-named limitations (carried forward, not resolved here)
- **Not `/verify`-gated.** These are Antigravity-driven pilots (`.agy/poster-pilot{2..5}.md`),
  self-checked via byte-identity reproduction of the delegated agent's reported SHA-256
  against a local rerun — not a blind reviewer→critic→auditor pass. No `src/` change is
  involved in this arc, so the constitution's baseline-isolation/full-`/verify` requirement
  does not strictly apply, but the empirical claims above have accordingly never been
  independently reviewed.
- **Engine asymmetry** (named explicitly in `d9edf19`'s own commit body, not discovered later):
  every ER curve ran on the C++ engine, every CM curve on Python (`runner.py` has no
  configuration-model path in C++). §5.4 licenses statistical cross-engine agreement but the
  headline comparison is an unstated cross-implementation one as of this commit. **Closed in
  S-062** via an explicit disclosure in `okf/poster/poster.tex`, not by re-running on matching
  engines.
- Not committed: `okf/poster/betterposter-template-landscape.pptx` (39MB, gitignored) and the
  superseded `_part`/`_chunk` raw intermediates from earlier chunked runs.

## Files changed (across this arc, cumulative)
`okf/poster/poster.tex` (new), `okf/poster/Better_Poster_Latex_Template.pdf` (new),
`scripts/calibrate_matched_degree.py` (new), `results/processed/matched_degree_calibration.json`
(new), `configs/poster_{er,cm}_mu{0,10,20,30,40,70}.json` (new), `results/poster_{er,cm}_mu*_raw.json`
(new, 12 files), `results/processed/poster_comparison.json`, `results/figures/poster_comparison.png`,
`results/figures/scaling_law_departure.png` (new), `scripts/analyze_poster_comparison.py`,
`scripts/plot_poster_comparison.py`, `scripts/plot_scaling_law_departure.py` (new).

## [Files Changed · Validation Status · New Decisions]
- **Files:** see above; full detail in the cited commits (`9f3cc17`…`d9edf19`).
- **Validation:** No `src/` or `cpp/src/` change in this arc — §5.4 cross-validation N/A.
  Results are self-checked (byte-identity reruns) by the delegated Antigravity sessions, **not**
  blind-`/verify`-gated. Treat as strong evidence, not an audited result.
- **New Decisions:** None. This entry does not introduce a new `d-0NN` — it backfills the
  session record for decisions and results that were already implicitly authorized under D-038.
