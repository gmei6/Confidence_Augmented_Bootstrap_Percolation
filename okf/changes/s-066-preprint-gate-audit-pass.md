---
type: Session Change
title: "S-066 — Pre-print verification gate: AUDIT PASS"
mutability: append-only
timestamp: 2026-08-06T08:15:00-04:00
tags: [poster, verify-gate, provenance, famcompare, comparison-2]
---

# S-066 — Pre-print verification gate (item 3b / P5): AUDIT PASS

Session span: 2026-08-04 (reviewer rounds, wrapped uncommitted) + 2026-08-06
(critic rounds, auditor, closeout). Full gate record:
`walkthrough-s066-preprint-gate.md` (committed `d90493f`).

## What was gated

The three analysis/figure pipelines behind the poster's load-bearing claims —
poster-comparison (hero + D-012 departure), famcompare (fear-multiplier,
D-042 interleave), fear-structure (percentage-decrease, D-040) — all
previously self-checked only. No `src/`/`cpp/` in scope (each dependency
carries its own prior AUDIT PASS).

## Gate arc

- **Reviewer rounds 1–3 (2026-08-04):** two MATERIAL fixes (config-provenance
  guard in pipeline A; ER tail raws certified) → round-3 SIGN-OFF. Fixes
  committed 2026-08-06 as `c7140e9`.
- **Critic round 1 (2026-08-06, blind, Opus): CRITIC FAIL, 4 MATERIALs** —
  M-1 stale `scaling_law_departure.png` (pre-densification, 2/8 points
  missing); M-2 stale Overleaf bundle + `~/Downloads` zip (superseded
  famcompare/fear-structure panels, old poster.tex); M-3 famcompare had NO
  provenance certification (three silent cross-family splices demonstrated
  on the matched ensemble); M-4 pipeline-A guard didn't bind the μ̄ slot and
  `realized_mu_bar` echoed spec input under a measurement name. All fixed →
  `e2ae0f5` (+ bundle rebuilt outside the tree, hash-verified).
- **Critic round 2: CRITIC FAIL, all round-1 fixes verified real, new M-5** —
  pilot raws (50/100 trials) certifiable as production twins; μ̄=0 pilot
  substitution silently turned Q6's +11.7% into +1.3%. Fixed with a relative
  (family key tuple) + absolute (`EXPECTED_TRIALS_PER_CELL=500`) trials pin,
  plus A-1 (dead CM-rebase fallback → accurate fail-loud raise), A-2 (raw-n
  bound to slot-n), A-6 (`metadata.provenance_certification` emitted by both
  pipelines) → `724068f`.
- **Critic round 3: CRITIC PASS.** Pre-fix control reproduced M-5 at
  `e2ae0f5`; exhaustive smuggle sweep — only the 26 canonical production
  raws can pass pipeline-A's gates; all 24 crossings + 24 D-012 ratios
  independently recomputed exact; 30-attack ledger, all held.
- **Auditor (blind): AUDIT PASS**, 26/26 evidence rows held (§5.6 stamp-only
  reproduction, §5.4 disclosure + engine lineage exact, fix commits contain
  their fixes, guards non-vacuous, no lessons trap violated, nothing
  dropped between rounds). One mandatory record correction, applied: the
  critic's "interleave tie at μ̄=0.5" was wrong — CM 4.263158 > GIRG
  4.200000, no exact tie at any n; clean alternation STRENGTHENS D-042.

## What the PASS licenses

Comparison 2 (Q6: geometry barely moves ignition, +11.7% vs ~30×), the
famcompare interleave (D-042), and the percentage-decrease panel (D-040) are
now citable as VERIFIED results on the printed poster. Item 3b closed; P5's
gate component closed.

Conditions carried (all disclosed in the walkthrough): GIRG μ̄=0.1
fear-structure point is direction-only (CI straddles zero); the poster's
engine-split disclosure sentence must survive future edits; ER μ̄=0.7 has
three P=0.5 crossings and the leftmost is used (1.092 vs ~1.139, no claim
flips, undisclosed on poster); `NEAR_FLOOR_RATIO=2.2` tuned-but-disclosed;
`runner.py` metadata gap remains the root cause of guard complexity —
queued as its own gated `src/` change.

## Commits

- `c7140e9` reviewer-round fixes (provenance guard, honest docstrings,
  300 DPI q4 map, poster.tex engine disclosure)
- `e2ae0f5` critic round-1 fixes (famcompare guard, μ̄-slot binding, honest
  realized_mu_bar, departure figure regen)
- `724068f` critic round-2 fixes (pilot rejection, n-slot binding,
  fail-loud CM rebase, certification metadata)
- `d90493f` the gate record itself

Also outside the tree: `.agy/poster-overleaf-zip/` staging + zip rebuilt
from current figures/poster.tex; `~/Downloads/twocascade-poster-overleaf.zip`
overwritten; all md5-verified (M-2).

## Terminology correction (queued S-064, applied this wrapup)

The 1.783 GIRG figure at μ̄=0.4 is the **D-012 departure ratio** (measured
crossing ÷ [family's own μ̄=0 anchor × (1−μ̄)²]) — NOT an "own-anchor ratio";
the own-anchor percentage metric (D-040 `measured_ratio_to_mu0`) is 0.642
there. okf live-state prose corrected accordingly.

## Hygiene queue added from gate advisories (post-print)

Per-cell trials check (`len(failed_fractions)==500`); a consumer for
`reliable`; dead-code cleanup left by A-1 (`CM_LEGACY_N10000_PATH`,
`CM_EXTENSION_SKIP`, tautological REBASED branches, stale `-> None`
annotation); stale comments (poster.tex DPI note + hero provenance refs,
`plot_famcompare_ratio.py` censoring comment, contradictory GIRG μ̄=0.1
presenter notes); famcompare bootstrap per-cell seeding; ER μ̄=0.7
crossing-estimator disclosure; hero PNG pair not byte-stable across
matplotlib builds (content-stable, disclosed).

## Process note

Gate run per Gary's explicit split: mechanical work on Sonnet (commit
agent), judgment stages on Opus (3 critics + auditor, each spawned blind
and fresh). Every poster number survived all five independent passes
unchanged — the gate hardened certification, it never moved a result.

Tooling note (why this file's first write was re-done): `append_okf.py`
reads stdin only when NO content argument is given; a piped invocation that
passed `-` as the content argument wrote a literal dash instead of the
document. The file was overwritten with the intended content in the same
session, before the wrapup commit was finalized (amended, unpushed).
