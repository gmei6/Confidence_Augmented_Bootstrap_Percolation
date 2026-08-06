# Walkthrough — item 3b pre-print verification gate (S-066, 2026-08-04)

Input document for the blind reviewer → critic → auditor gate. Scope: the three
analysis/figure pipelines behind the poster's load-bearing empirical claims,
which until now were **self-checked only** (delegated-agent snapshots and an
orchestrator-run acceptance script — no blind review). Nothing in `src/` or
`cpp/` is under review here; every `src/`/`cpp/` dependency already carries its
own AUDIT PASS (C1 `6c5491a`, C3a `8956d75`, C3b-obs `0179110`, girg-cpp-port
merge `a2b2596` / D-045).

## The three pipelines and their claims

### A. Poster comparison (hero figure + d012 departure)
- Analysis: `scripts/analyze_poster_comparison.py` →
  `results/processed/poster_comparison.json`
- Figures: `scripts/plot_poster_comparison.py` →
  `results/figures/poster_comparison.png` (+ `_legend.png`) — deliberately
  still exactly 9 curves (3 families × μ̄∈{0,0.4,0.7});
  `scripts/plot_scaling_law_departure.py` → `scaling_law_departure.png`.
- Claims on the poster:
  1. D-012 `a_c(μ)=a_c(0)(1-μ̄)²` reproduces on ER flat across μ̄ (ratios
     0.987/0.976/0.978/0.983/1.092 at 0.1/0.2/0.3/0.4/0.7).
  2. CM departs monotonically (1.128/1.248/1.514/1.839 at 0.1–0.4; 0.7
     excluded, predicted crossing below the r=2 floor).
  3. **Q6: geometry barely moves ignition** — GIRG zero-fear crossing 11.41 vs
     CM 10.22 (~11.7%), vs ER 313.6 (~30× from heterogeneity alone); GIRG's
     D-012 **departure ratio** at μ̄=0.4 is 1.783 ≈ CM's 1.839 (the
     `d012_table.ratio` field: measured crossing ÷ [family's own μ̄=0 anchor ×
     the ER-derived (1-μ̄)² decay]. This is NOT D-040's own-anchor percentage
     metric — that is `measured_ratio_to_mu0` = 0.642 for GIRG at μ̄=0.4 — and
     earlier okf prose calling 1.783 an "own-anchor ratio" conflated the two;
     terminology corrected here, okf live-state correction queued for wrapup).
- History: delivered `2024c23` (2026-08-02, UNGATED — checked by a delegated
  agent against pre-delegation snapshots after an API-error death); extended
  today (`d25f9f2`) with 5 new GIRG mu points (0.1/0.2/0.3/0.5/0.6) and a new
  `check_family_compatibility` fail-loud guard.

### B. famcompare (fear-multiplier ratio, "Fear is an amplifier with a dial")
- Analysis: `scripts/analyze_famcompare.py` →
  `results/processed/famcompare_analysis.json`
- Figure: `scripts/plot_famcompare_ratio.py` →
  `results/figures/famcompare_ratio.png` (DPI 300 as of `d25f9f2`)
- Claims (D-042, S-064): on the fully matched ⟨k⟩=4.5336 ensemble, ER ≥26×
  (censored), power-law (CM) 6.6×, GIRG 8.27× at μ̄=0.7; GIRG and CM
  INTERLEAVE — geometry does not measurably change fear's amplification in
  either direction. (The earlier "geometry damps" reading was an ensemble
  artifact — CM was calibrated to ⟨k⟩=4.0 — retracted in D-042.)
- History: CM rebase + ER extensions S-064 (self-checked); girg μ̄=0.5/0.6
  extension cells merged today (`d25f9f2`) from the new poster arms.

### C. Fear × Structure (percentage decrease, D-040 reframe)
- Analysis: `scripts/analyze_poster_fear_structure.py` →
  `results/processed/poster_fear_structure.json` (reads pipeline A's output —
  no raw access of its own)
- Figure: `scripts/plot_poster_fear_structure.py` → `poster_fear_structure.png`
- Claim shape (D-040): each family's measured percentage decrease in a_c(μ̄)
  against ITS OWN μ̄=0 anchor — the (1-μ̄)² curve appears only as a dashed
  ER-only reference. GIRG curve now 7-point: +3.7/+14.7/+22.9/+35.8/+45.2/
  +54.1/+62.2 % at μ̄=0.1..0.7 (crossings 10.99→4.31; only 0.7 near_floor).

## Data provenance

- Raw inputs, all runner-stamped (config, seed, commit hash, timestamp):
  - `results/poster_{er,cm}_mu{0..70}_raw.json` — ER on cpp engine, CM on
    python (pilot arcs, commits through `d9edf19`; mu50/60 at `d795035`,
    committed `b0e9ed1`).
  - `results/poster_girg_mu{0,40,70}_raw.json` — python engine (`2024c23` arc).
  - `results/poster_girg_mu{10,20,30,50,60}_raw.json` — **cpp engine**, run
    today from configs committed first (`f30aef1`), raws committed `0e739a1`.
    Independent verification already on record (subagent report, S-066): stamps
    correct, 500 trials/cell, 12/12/12/10/10 cells, all curves strictly
    monotone, no BKL n>65536 warning. Two DISTINCT interior-point counts exist
    and both are on record: the run-verifier counted cells with 0<P<1
    (12/12/11/10/10 per arm); the analysis artifact's own
    `curves_summary[...].interior_point_count` (the field feeding the
    `reliable` flag, threshold ≥3) is 8–9 for every girg arm. An earlier
    draft of this document wrote "10–12 interior points" citing the first
    count where the second was meant — corrected per reviewer finding.
  - `results/famcompare_*_raw.json` + `results/famcompare_er_*_ext_raw.json` —
    S-064 ensemble.
- Engine mix inside the GIRG family (0/0.4/0.7 python; 0.1/0.2/0.3/0.5/0.6
  cpp) is deliberate, D-045-backed, and disclosed on the poster (caption
  sentence updated today). §5.4 statistical parity for the C++ GIRG path was
  the girg-cpp-port gate's subject (AUDIT PASS, `a2b2596`).

## Regeneration commands (all read from disk; none re-run simulations)

```
arch -arm64 python3 scripts/analyze_poster_comparison.py
arch -arm64 python3 scripts/analyze_poster_fear_structure.py
arch -arm64 python3 scripts/plot_poster_fear_structure.py
arch -arm64 python3 scripts/analyze_famcompare.py
arch -arm64 python3 scripts/plot_famcompare_ratio.py
arch -arm64 python3 scripts/plot_poster_comparison.py
arch -arm64 python3 scripts/plot_scaling_law_departure.py
arch -arm64 python3 scripts/plot_q4_mumap.py
```

## Self-checks already performed (NOT blind — that is why this gate exists)

1. Acceptance script (orchestrator-run, `ACCEPT PASS` 18/18): blast radius,
   src/configs/tests byte-identity vs snapshot, 8-point girg d012 grid,
   engine recording, 7-point fear-structure curve, famcompare by_mu coverage,
   point-estimate immobility, figure existence + 300 DPI.
2. Field-level diff of the `d25f9f2` regeneration vs pre-wiring snapshot:
   the ONLY pre-existing values that moved are bootstrap `ci_lo`/`ci_hi`
   (~1–3%) and one `bootstrap_drop_fraction` (1e-4) in girg/ER-matched —
   consistent with a shared bootstrap RNG stream re-indexing when cells are
   added (CM, processed before girg, is byte-identical). Point estimates
   everywhere unmoved.
3. The five new arms' run verification (see provenance above).

## Reviewer round 1 disposition (2026-08-04, this gate)

A first blind reviewer returned 4 MATERIAL + 3 ADVISORY findings (no poster
number falsified; every headline value re-verified against artifacts). Fixes
applied before this round:
- Guard blind spot (raws persist no graph params, so metadata-only checks
  cannot distinguish families in a matched ensemble): new
  `check_family_config_provenance` in `analyze_poster_comparison.py` binds
  each member to its committed config (`configs/<key>.json` must exist,
  declare the spec's raw as `output.raw_filepath`, and share one
  `pinned_params.graph` block family-wide). The durable fix — persisting
  graph/fear blocks in raw metadata via `runner.py` — is a `src/` change
  QUEUED as hygiene (needs isolation + its own gate), deliberately not
  rushed into this print cycle.
- `weights` added to `check_family_compatibility`'s key tuple.
- famcompare girg-extension docstring rewritten: the w_min/alpha_g/tau
  compatibility claim is a MANUAL config comparison, not a
  `validate_pinned_compat` output.
- This document's two prose errors corrected in place (interior-point count
  definition; "own-anchor" vs D-012 departure-ratio terminology — see the
  marked passages above).
Advisories on record, deliberately not acted on this round: GIRG μ̄=0.1
fear-structure point's CI straddles zero (+3.7% [-1.0, 8.4] — treat the low
end of that curve as direction-only); `NEAR_FLOOR_RATIO = 2.2` is a
disclosed-but-tuned threshold (principled criterion queued for future grids).

## Reviewer round 2 disposition (2026-08-04)

Round-2 blind reviewer verified all round-1 fixes real and reproduced every
poster number live from the committed raws/configs. One new MATERIAL finding
+ one advisory, both fixed before round 3:
- MATERIAL: `check_family_config_provenance` bound only the spec-key's
  primary config, leaving the two ER tail-extension raws
  (`poster_er_mu{40,70}_tails_raw.json`, which feed the 0.983/1.092 D-012
  ratios) certified by no config — and ER's null graph block made the
  family-identity check vacuous there. FIXED: the guard now iterates every
  raw path in every spec, derives each raw's own config from its basename
  (`results/<name>_raw.json` → `configs/<name>.json`), requires existence +
  exact `output.raw_filepath` binding + family-wide graph-block identity.
  Verified positively (both ER multi-raw specs bind) and negatively (a girg
  raw smuggled into the ER family raises ValueError).
- ADVISORY: stale "girg jumps 0.4 → 0.7" comment in
  `plot_famcompare_ratio.py` replaced with the current full-grid statement.

## Reviewer round 3 (2026-08-04): SIGN-OFF

Fresh blind reviewer verified the round-2 fix positively (all 26 raw paths
across 24 specs bind to basename-derived configs; both ER tail configs exist
with exact raw_filepath declarations) and negatively (smuggled cross-family
raw raises), reproduced every headline number verbatim end-to-end, swept the
edits for new defects (none), and returned:
"REVIEWER SIGN-OFF: no blocking or material issues."

## Critic round 1 (2026-08-06): CRITIC FAIL → fix round applied

Blind critic (fresh, Opus, fed this walkthrough at `c7140e9`) returned
**CRITIC FAIL** — four MATERIAL findings, nine advisories. **No poster number
was falsified**: every headline value reproduced exactly from the committed
raws/configs (ER D-012 ratios, CM departure, GIRG 11.41 / CM 10.22 / ER
313.57 crossings, famcompare 26.32×/6.63×/8.27×, fear-structure 7-point
percentages). The MATERIALs were stale artifacts and demonstrated
silent-wrong-data paths:

- **M-1** `results/figures/scaling_law_departure.png` stale (pre-densification;
  missing μ̄=0.5/0.6 points, 2 of 8 per family — §5.6 regeneration broken).
- **M-2** the Overleaf print bundle (`.agy/poster-overleaf-zip/` staging + zip
  + the `~/Downloads` copy) carried pre-`d25f9f2` `famcompare_ratio.png` and
  `poster_fear_structure.png` (superseded gap/4-point GIRG curves) and a
  pre-`c7140e9` `poster.tex`.
- **M-3** `analyze_famcompare.py` had NO family-provenance certification — the
  round-1 fix landed only in pipeline A. Critic demonstrated three silent
  cross-family splices on the matched ensemble (CM raw → girg family; bounded
  ER ext → matched ER; girg raw → CM slot), covering every raw behind the
  Fear-Amplifies panel. `merge_extension_cells` reports were also never
  inspected by any caller (mismatch = print, never fatal).
- **M-4** pipeline A's guard bound raw↔config but not the μ̄ slot (a
  same-family raw in the wrong μ̄ slot passed silently; demonstrated mu50→mu30
  moving the departure ratio 1.574→1.118), and `realized_mu_bar` was an echo:
  no raw persists `realized_fear`, so the fallback republished `spec["mu"]`
  under a measurement name for all 24 curves.

**Fix round (Gary-approved 2026-08-06), all four MATERIALs closed:**

- M-1: `plot_scaling_law_departure.py` re-run; regenerated PNG (8 points per
  family, both new CM below-floor points inside the floor band) committed.
- M-2: staging refreshed from `results/figures/` + `okf/poster/poster.tex`,
  zip rebuilt (`zip -FS`), `~/Downloads` copy overwritten; all five
  poster-referenced images + poster.tex verified md5-identical to their
  current sources inside the zip.
- M-3: `check_config_provenance` ported into `analyze_famcompare.py` — one
  group per merged CURVE (not per family: famcompare legitimately mixes
  ensembles across n — CM q4-4.0 at n=4000/20000 vs matched-4.5336 at
  n=10000; girg's w_min is per-n), each raw bound to its basename-derived
  config (exists + exact `output.raw_filepath` + `pinned_params.graph.type`
  matches the family; None for ER whose configs carry `graph: null`) and
  group-wide graph-block identity. Ext-raw paths hoisted to module constants
  (`GIRG_EXT_PATHS`, `ER_MATCHED_EXT_PATH`, `ER_BOUNDED_EXT_PATH`) shared by
  the merge calls and the provenance groups so the certified list cannot
  drift from the merged list. Extension reports now FATAL on pinned-param
  mismatch, and on missing/incomplete expected μ̄ cells when the ext raw is
  present (wholly absent raws stay a recorded, tolerated skip). The
  ER-matched↔bounded null-graph twin case is covered by this missing-cell
  raise (seed_size 279 vs 2 filters to empty).
- M-4: pipeline A guard now also requires each config's
  `sweep.mean_fear_grid == [spec.mu]`, plus a cell-level check that every raw
  cell's `mean_fear` equals the spec slot's μ̄; `realized_mu_bar` is now
  `null` when no `realized_fear` data exists (currently all raws — runner.py
  gap, hygiene-queued) instead of echoing the spec.

**Verification of the fix round:** both pipelines re-run clean; regenerated
`famcompare_analysis.json` field-diff vs committed = {git_commit, timestamp}
only; regenerated `poster_comparison.json` field-diff = 24× `realized_mu_bar`
→ null + git_commit only (committed). Negative tests: all five attack
replays now raise (CM raw in girg group; girg raw in CM matched group;
bounded-ext-in-matched fatal via missing-μ̄; pipeline-A mu50-in-mu30 slot;
pipeline-A cross-family regression).

**Critic advisories on record, deliberately not acted on this round** (stale
LaTeX/py comments and disclosure notes, no claim flipped): stale "regenerate
at ≥300 DPI" comment in poster.tex (figures are already 299.999 dpi); stale
hero provenance commit refs (poster.tex:74-76); near-floor prose
contradiction between `analyze_poster_fear_structure.py`,
`plot_poster_fear_structure.py`, and poster.tex:265; ER μ̄=0.7 has three
P=0.5 crossings and `interpolate_crossing` implicitly takes the leftmost
(1.092 vs ~1.139 rightmost, ~4% undisclosed estimator sensitivity; no claim
flips — both read "ER flat"); the two pipelines' differing p-tolerance
(exact repr vs rel 1e-4 — ER's protection against a p-rounding twin is
incidental); stale censoring comment in `plot_famcompare_ratio.py:24-26`;
contradictory presenter notes on GIRG μ̄=0.1 multiplier (poster.tex:217 vs
:228 — 0.80× [0.35, 1.75], below the no-effect line); walkthrough's own
top-out band understated (actual 0.942–1.000, one arm saturates); CI-movement
range in self-check #2 actually −2.9%…+4.2% (non-panel n).

## Critic round 2 (2026-08-06): CRITIC FAIL → second fix round applied

Fresh blind critic at `e2ae0f5` verified **all four round-1 MATERIAL fixes
real by replay** (M-1 byte-stable 8-point regen; M-2 hash-verified across
staging/zip/~/Downloads; M-3 all three splices raise + new attacks held,
incl. certified-vs-loaded drift trace and the `note=="merged"` bypass hunt;
M-4 both binding levels verified independently, `realized_mu_bar` honest,
headline numbers exact at HEAD). One **new MATERIAL**:

- **M-5**: a *pilot* raw substituted for its production twin passed BOTH
  pipeline-A guards silently — pilots (7 exist: girg mu0/40/70 at 100
  trials, cm/er mu50/60 at 50) share every checked pinned key, their own
  committed config, the same graph block, and the same mean_fear cells;
  only `trials_per_cell` and the seed grid differ, and nothing inspected
  either. Demonstrated: girg-mu0-pilot substitution turns Q6's "+11.7%"
  into "+1.3%" with `reliable=True` and no warning. famcompare was already
  protected (`EXPECTED_TRIALS=500`).

**Fix round 2 (same Gary approval), M-5 + three cheap advisories closed:**

- M-5: `trials_per_cell` added to `check_family_compatibility`'s key tuple
  AND an absolute per-raw pin `EXPECTED_TRIALS_PER_CELL = 500` (mirroring
  famcompare; the relative check alone cannot reject an all-pilot family).
  Replay: all three pilot substitutions now raise before any output write.
- A-1: the dead CM-rebase fallback (unreachable since the fatal
  extension-report check; mislabelled missing raws as pinned-param
  mismatches) replaced with an immediate, accurately-worded raise.
  Verified: forced rebase failure raises "CM rebase against the matched
  poster_cm arms failed (missing/incomplete raw or pinned-param mismatch)".
- A-2: `build_family` now binds each raw's metadata `n` to its slot's `n`
  (and `build_cm_matched_n10000` pins its anchor to n=10000). Verified:
  n=20000 raw in the n=4000 slot raises.
- A-6: both pipelines now emit `metadata.provenance_certification` in their
  output artifacts (checks performed + configs/groups bound), so a guarded
  run is distinguishable from an unguarded one. All three processed
  artifacts regenerated; field deltas vs `e2ae0f5` are metadata-only
  (stamps + the new certification block); every headline number re-verified
  exact. This also refreshes `poster_fear_structure.json`'s stale
  `source_analysis_commit` (round-2 advisory A-5).

Round-2 advisories on record, not acted: `poster_comparison.png`/`_legend.png`
regenerate content-identically but not byte-identically in this environment
(renderer-build antialiasing, 56/4.7M pixels within ±1px — committed pair
came from a different matplotlib build; §5.6 byte-exactness holds for the
other four figures); ER null-graph configs remain mutually indistinguishable
by graph block alone (protection is the seed-size filter + missing-μ̄ raise,
confirmed empirically).

## Critic round 3 (2026-08-06): CRITIC PASS

Fresh blind critic at `724068f`. **No MATERIAL finding stands.** Verified by
replay, with a pre-fix control at `e2ae0f5` reproducing the M-5 acceptance
(Q6 +11.66% → +1.33% silently) before confirming the fix rejects it:

- M-5 HELD: all seven pilot substitutions + the all-pilot family raise
  before any write; chunk/part intermediates blocked (no committed config);
  doctored-spec bypasses impossible (pin runs per raw path before family
  bucketing). **Exhaustive smuggle sweep: of every `results/*_raw.json`,
  only the 26 canonical production raws can pass all pipeline-A gates.**
- A-1 HELD (4 forced-failure replays, accurate messages; q4 fallback
  unreachable), A-2 HELD (3 n-slot replays), A-6 PRESENT and truthful
  (each certification claim mapped 1:1 to enforcing code; famcompare's
  understates rather than overstates).
- M-1/M-2 re-confirmed at HEAD; M-3/M-4 regression suites all still raise.
- Headline numbers exact via BOTH the pipelines and an independent
  reimplementation (own reader + interpolator): all 24 crossings and all
  24 D-012 ratios to the last printed digit; D-042 interleave confirmed on
  the full grid (CM>GIRG at 0.1/0.3/0.5, GIRG>CM at 0.2/0.4/0.6/0.7 —
  CORRECTED per the auditor: the critic's "tie 0.5" was wrong, committed
  values are CM 4.263158 vs GIRG 4.200000; no exact tie exists at any n;
  the clean alternation mildly STRENGTHENS the interleave claim).

Round-3 advisories on record (none acted this round; hygiene-queued):
trials pin trusts metadata not per-cell counts (add
`len(failed_fractions)==500` in the cell loop); a multi-raw spec truncated
to its tails raw alone still runs (self-flagged `reliable=False`, but
nothing consumes `reliable`; measured: tails raws are not load-bearing on
any point estimate — dropping them leaves ratios bit-identical); stale
docstring + now-dead `CM_LEGACY_N10000_PATH`/`CM_EXTENSION_SKIP` and
tautological `status=="REBASED"` branches left by the A-1 fix; stale
`-> None` annotation on `check_family_config_provenance`; famcompare's
certification block records group paths even if a listed raw is absent
(all 26 exist today); certification is informational, not enforced
downstream (`analyze_poster_fear_structure.py` reads only `git_commit`);
girg famcompare curve mixes engines within one series (disclosed,
D-045-gated, `engine` not in PINNED_COMPAT_KEYS).

**CORRECTION to the round-2 record above (critic round 3, A7-7):** the
figure-regen advisory's numbers were wrong as recorded — measured at HEAD,
`poster_comparison.png` differs in 76,892/4.7M pixels (max channel delta
216) and `_legend.png` regenerates at 277×1633 vs the committed 279×1633
(text-metric/layout, not antialiasing). The conclusion stands (content
verified identical by crop comparison, DPI 299.9994 both; committed pair
from a different matplotlib build) — only the magnitude was misstated.

## Known open caveats the gate should weigh (not hide)

- Four of the five new arms top out at P(systemic)=0.94–0.98 at their largest
  seed (grid-range note; crossings sit mid-grid).
- famcompare's ER μ̄≥0.5 arms share RNG streams with earlier cells in specific
  collision patterns documented in `scripts/analyze_famcompare.py`'s docstring.
- The famcompare bootstrap is not per-cell seeded (hygiene item queued).
- `results/` layout: poster raws live at `results/` top level, not
  `results/raw/` (accepted deviation, S-061 record).
- Fear-structure's near_floor flag at μ̄=0.7 (within 2.2× of the r=2 floor).

## Auditor verdict (2026-08-06): AUDIT PASS

Blind auditor at `724068f`, fed this walkthrough. 26-row evidence table, all
HELD: §5.6 reproduction of all three processed artifacts (stamp-only diffs)
and figure regeneration (four byte-stable; the two disclosed
renderer-sensitive ones content-verified); every headline number read from
the COMMITTED artifacts, not console output; §5.4 disclosure verbatim on the
poster and the engine lineage in `engine_resolved` matching it exactly (ER
cpp ×8, CM python ×8, GIRG python at 0/0.4/0.7 + cpp at the five
densification arms); all three fix commits' diffs contain their claimed
fixes; guards fired live and non-vacuous; no lessons-learned trap violated;
no finding quietly dropped between rounds. One mandatory record correction
(the round-3 "tie 0.5" — applied above, marked CORRECTED). Conditions
carried forward, all already disclosed: GIRG μ̄=0.1 fear-structure point is
direction-only (CI straddles zero); the poster's engine-split disclosure
sentence must survive any further poster edit; NEAR_FLOOR_RATIO=2.2 is
tuned-but-disclosed; the runner.py metadata gap stays a properly-gated
future `src/` change; ER μ̄=0.7's leftmost-of-three-crossings estimator
sensitivity (1.092 vs ~1.139) is undisclosed on the poster.

## What a PASS licenses

Citing Comparison 2 (Q6 geometry), the famcompare interleave (D-042), and the
percentage-decrease panel as verified results on the printed poster, closing
next-actions item 3b / P5's gate component.
